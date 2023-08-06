import time
import json
import logging
import click
import tqdm
import numpy as np
import pkg_resources

import ciel.bounds as bounds
import ciel.movie_parser as movie_parser
from ciel.transition.snapshot_graph import SnapshotGraph
from ciel.transition.snapshot import Snapshot
from ciel.video import VideoReader
from ciel.recognizer import (
    ScoreRecognizer, FieldRecognizer,
    GameStateRecognizer, NextRecognizer,
    GameState)
from abyss import ArrayField, Pair, PuyoType


def calc_score(graph):
    try:
        path = graph.find_transitions()
    except Exception:
        return -1

    total_score = 0
    for transition in path:
        snapshot = transition.snapshot
        chain_field = snapshot.field.clone()
        s = chain_field.chain()
        total_score += s.score

        if snapshot.field.is_all_clear():
            total_score += 2100

    return total_score


def convert_puyotype_field(arr):
    r = np.zeros((6, 14), dtype=np.int)
    r[:, 2:][arr == 'empty'] = PuyoType.EMPTY
    r[:, 2:][arr == 'red'] = PuyoType.RED
    r[:, 2:][arr == 'blue'] = PuyoType.BLUE
    r[:, 2:][arr == 'green'] = PuyoType.GREEN
    r[:, 2:][arr == 'yellow'] = PuyoType.YELLOW
    r[:, 2:][arr == 'purple'] = PuyoType.PURPLE
    r[:, 2:][arr == 'ojama'] = PuyoType.OJAMA
    return r


def convert_puyotype_pair(arr):
    r = np.zeros((2, ), dtype=np.int)
    r[arr == 'empty'] = PuyoType.EMPTY
    r[arr == 'red'] = PuyoType.RED
    r[arr == 'blue'] = PuyoType.BLUE
    r[arr == 'green'] = PuyoType.GREEN
    r[arr == 'yellow'] = PuyoType.YELLOW
    r[arr == 'purple'] = PuyoType.PURPLE
    r[arr == 'ojama'] = PuyoType.OJAMA
    return r


@click.command()
@click.argument('movie_path', type=click.Path())
@click.option('--begin', type=str, required=False, default="00:00")
@click.option('--puyo-recognizer-model', type=str, required=False)
@click.option('--score-recognizer-model', type=str, required=False)
def main(movie_path, begin, puyo_recognizer_model, score_recognizer_model):
    """Validate record generation
    \b
    movie_path: path to source video
    """
    # logger = logging.getLogger(__name__)

    if puyo_recognizer_model is None:
        # puyo_recognizer_model = './data/model/cnn12'
        puyo_recognizer_model = pkg_resources.resource_filename('asai-ciel', 'models/cnn')

    if score_recognizer_model is None:
        # puyo_recognizer_model = './data/model/score_template.pickle'
        score_recognizer_model = pkg_resources.resource_filename('asai-ciel', 'models/score_template.pickle')

    score_recognizer = ScoreRecognizer(score_recognizer_model)
    field_recognizer = FieldRecognizer(puyo_recognizer_model)
    next_recognizer = NextRecognizer(puyo_recognizer_model)
    game_state_recognizer = GameStateRecognizer()

    with VideoReader(movie_path) as video_reader:
        screen_bounds = bounds.PuyoScreenBounds(video_reader.width)
        parser = movie_parser.MovieParser(screen_bounds)

        fps = video_reader.fps
        begin_time = list(map(int, begin.split(':')))
        begin_frame = (begin_time[0] * 60 + begin_time[1]) * fps

        match_begin_time = time.time()
        match_begin_position = None
        match_count = 0
        latest_scores = [0, 0]

        for frame, frame_count in video_reader.foreach_frame(
                begin_frame,
                tqdm=tqdm.tqdm):
            puyos = parser.crop_puyo_images(frame, (16, 16))
            nexts = parser.crop_next_images(frame, (16, 16))
            scores = parser.crop_score_images(frame, (13, 17))

            # predict
            predicted_scores = score_recognizer.predict(scores)
            caribrated_puyos = field_recognizer.predict(puyos)
            predicted_nexts = next_recognizer.predict(nexts)
            game_state = game_state_recognizer.predict(
                predicted_scores,
                field_recognizer.get_effect_count())

            for p in range(2):
                if predicted_scores[p].isdigit():
                    latest_scores[p] = int(predicted_scores[p])

            # initialize graph on match starting
            if game_state == GameState.MATCH_START:
                graph = [
                    SnapshotGraph(),
                    SnapshotGraph()
                ]
                match_begin_time = time.time()
                match_begin_position = video_reader.position

            # add node
            if game_state == GameState.MATCHING:
                elapsed = video_reader.position - match_begin_position
                for i in range(2):
                    snapshot = Snapshot(
                        ArrayField.from_array(convert_puyotype_field(
                            caribrated_puyos[i, :, :]).tolist()),
                        [
                            Pair(*convert_puyotype_pair(predicted_nexts[i, 0, :]).tolist()),
                            Pair(*convert_puyotype_pair(predicted_nexts[i, 1, :]).tolist())
                        ],
                        frame=frame_count,
                        time=elapsed.total_seconds())
                    graph[i].append(snapshot)

            if game_state == GameState.MATCH_END:
                match_end_position = video_reader.position
                match_time_length = match_end_position - match_begin_position

                # 試合前の暗転エフェクトや，相手連鎖中の揺れエフェクトによって発生する
                # MATCH_START, MATCH_END の誤判定を無視する
                if match_time_length.total_seconds() < 5:
                    continue

                match_count += 1

                # write score from graph
                def get_player_json(p):
                    total_score = calc_score(graph[p])
                    records = list(map(
                        lambda t: t.to_dict(), graph[p].find_transitions()))
                    return {
                        'player': p,
                        'records': records,
                        'displayed_score': int(latest_scores[p]),
                        'calculated_score': int(total_score),
                        'score_diff': int(latest_scores[p] - total_score)
                    }

                realtime = time.time() - match_begin_time
                print(json.dumps({
                    'match_count': match_count,
                    'time': {
                        'begin': str(match_begin_position),
                        'end': str(match_end_position),
                        'length': str(match_time_length),
                        'length_sec': str(match_time_length.total_seconds())
                    },
                    'debug': {
                        'processing_time': realtime,
                    },
                    'plays': [get_player_json(0), get_player_json(1)]
                }), flush=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARN,
        format='%(asctime)s- %(name)s - %(levelname)s - %(message)s')
    main()
