# type: ignore

import os
import glob
from collections import defaultdict

import cv2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
from sklearn.metrics import confusion_matrix

from IPython.display import display, Image

number_width = 27


class Metrics:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scale = width / 1280.0

    def field(self):
        return [
            {
                'top': int(105 * self.scale),
                'left': int(188 * self.scale),
                'bottom': int(585 * self.scale),
                'right': int(445 * self.scale)
            },
            {
                'top': int(105 * self.scale),
                'left': int(837 * self.scale),
                'bottom': int(585 * self.scale),
                'right': int(1094 * self.scale)
            }
        ]

    def score_bounds_width(self):
        return int(214 * self.scale)

    def score_bounds_height(self):
        return int(35 * self.scale)

    def score(self):
        return [
            {
                'top': int(590 * self.scale),
                'left': int(234 * self.scale),
                'bottom': int(590 * self.scale) + self.score_bounds_height(),
                'right': int(234 * self.scale) + self.score_bounds_width()
            },
            {
                'top': int(590 * self.scale),
                'left': int(833 * self.scale),
                'bottom': int(590 * self.scale) + self.score_bounds_height(),
                'right': int(833 * self.scale) + self.score_bounds_width()
            }
        ]

    def puyo_width(self):
        return (self.field()[0]['right'] - self.field()[0]['left']) / 6

    def puyo_height(self):
        return (self.field()[0]['bottom'] - self.field()[0]['top']) / 12

    def number_width(self):
        return int(27 * self.scale)



def display_cv_image(image, format='.png'):
    decoded_bytes = cv2.imencode(format, image)[1].tobytes()
    display(Image(data=decoded_bytes))


def load_all_images(path):
    images = []
    for image_path in glob.glob(os.path.join(path + '**/*.png'), recursive=True):
        source = cv2.imread(image_path)
        source = cv2.resize(source, (16, 16))
        images.append(source)
    return images

def load_images(path, folds, train_fold, num_per_label, labels=None):
    train_X = []
    train_Y = []
    test_X = []
    test_Y = []
    test_urls = []

    label_counter = defaultdict(int)

    for label in os.listdir(path):

        if labels != None and label not in labels:
            continue

        # only folders
        label_path = os.path.join(path, label)
        if not os.path.isdir(label_path):
            continue

        for image_path in sorted(os.listdir(label_path)):

            # ignore .DS_Store
            if not image_path.endswith('.png'):
                continue

            source = cv2.imread(os.path.join(label_path, image_path))

            if label_counter[label] > num_per_label:
                break
            label_counter[label] += 1

            if (train_fold == None) or (label_counter[label] % folds != train_fold):
                train_X.append(source)
                train_Y.append(label)
            else:
                test_X.append(source)
                test_Y.append(label)
                test_urls.append(image_path)

    print(label_counter)

    return train_X, train_Y, test_X, test_Y, test_urls


def calc_accuracy(estimator, make_feature, test_X, test_Y):
    test_X_feat = list(map(lambda x: make_feature(x), test_X))

    predicts = estimator.predict(test_X_feat)
    correct = 0
    for pair in zip(test_Y, predicts):
        if pair[0] == pair[1]:
            correct += 1
    return correct / float(len(predicts))

def get_confusion_matrix(y_true, y_pred):
    labels = sorted(list(set(y_true)))
    cmx_data = confusion_matrix(y_true, y_pred, labels=labels)

    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

    plt.figure(figsize = (14, 12))
    sns.heatmap(df_cmx, annot=True)
    return plt

def open_video(source_path='../data/raw/_-B7lIF-I2u8c.mp4'):
    capture = cv2.VideoCapture(source_path)

    return {
        'capture': capture,
        'fps': round(capture.get(cv2.CAP_PROP_FPS)),
        'length': capture.get(cv2.CAP_PROP_FRAME_COUNT),
        'size': (
            int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
    }

def foreach_video_frame(capture, begin_frame=0, end_frame=None, tqdm=None):
    length = capture.get(cv2.CAP_PROP_FRAME_COUNT)

    capture.set(cv2.CAP_PROP_POS_FRAMES, begin_frame)

    if end_frame is None:
        end_frame = length

    progress = None
    if tqdm:
        progress = tqdm(total=end_frame - begin_frame - 1)

    frame_iter = begin_frame

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        frame_iter += 1

        if end_frame < frame_iter:
            break

        yield np.array(frame), frame_iter

        if progress:
            progress.update(1)

    capture.release()

def crop_puyo_images(image, field_bounds):
    width = (field_bounds[0]['right'] - field_bounds[0]['left']) / 6
    height = (field_bounds[0]['bottom'] - field_bounds[0]['top']) / 12

    for k in range(2):
        for j in range(12):
            puyo_top = int(height * j) + field_bounds[k]['top']
            for i in range(6):
                puyo_left = int(width * i) + field_bounds[k]['left']
                cropped = image[
                    puyo_top:puyo_top + int(width), # TODO: 逆では？
                    puyo_left:puyo_left + int(height)
                ]

                yield cropped

def crop_score_images(image, metrics):
    number_images = [[], []]

    for player_index in range(2):
        top = metrics.score()[player_index]['top']
        left = metrics.score()[player_index]['left']
        bottom = metrics.score()[player_index]['bottom']
        right = metrics.score()[player_index]['right']
        score_image = np.copy(image[top:bottom, left:right])

        for i in range(8):
            l = int((metrics.score_bounds_width() / 8) * i)
            number_image = score_image[:, l:l + metrics.number_width()]
            resized_number_image = cv2.resize(number_image, (13, 17))
            number_images[player_index].append(resized_number_image)

    return number_images

def make_movie(predict, filename, begin, end, predict_score=None, predict_state=None, tqdm=None, caribrate=None, history_size=1, source=None):
    capture = open_video(source)

    metrics = Metrics(capture['size'][0], capture['size'][1])

    fourcc = cv2.VideoWriter_fourcc(*'H264')
    video = cv2.VideoWriter(filename, fourcc, capture['fps'], capture['size'])

    color = {
        'red': [0, 0, 255],
        'blue': [255, 0, 0],
        'green': [0, 255, 0],
        'yellow': [0, 255, 255],
        'purple': [255, 0, 255],
        'ojama': [255, 255, 255],
        'empty': [0, 0, 0]
    }

    width = metrics.puyo_width()
    height = metrics.puyo_height()
    predicted_history = np.full((2, 12, 6, history_size), 'empty', dtype='U8')

    if end != None:
        end = capture['fps'] * 60 * end

    for image, _ in foreach_video_frame(capture['capture'], capture['fps'] * 60 * begin, end, tqdm):
        puyos = list(crop_puyo_images(image, metrics.field()))
        scores = crop_score_images(image, metrics)

        if predict != None:
            predicted = predict(puyos).reshape(2, 12, 6)

            predicted_history = np.roll(predicted_history, 1, axis=3)
            predicted_history[:, :, :, 0] = predicted

            for k in range(2):
                for i in range(12):
                    for j in range(6):
                        puyo_top = int(height * i) + metrics.field()[k]['top']
                        puyo_left = int(width * j) + metrics.field()[k]['left']

                        if caribrate != None:
                            caribrated = caribrate(predicted_history[k, i, j, :])
                        else:
                            caribrated = predicted_history[k, i, j, 0]

                        if caribrated in color:
                            image[
                                puyo_top + 5:puyo_top + int(width) - 5,
                                puyo_left + 5:puyo_left + int(height) - 5
                            ] = color[caribrated]

        predicted_scores = ['', '']
        if predict_score != None:
            for k in range(2):
                for i in range(8):
                    predicted_scores[k] += predict_score(scores[k][i])
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, predicted_scores[k], (metrics.score()[k]['right'], metrics.score()[k]['bottom']), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        if predict_state != None:
            predicted_state = predict_state(predicted_history, predicted_scores)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, predicted_state, (0, 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        video.write(image)

    video.release()


def parse_movie(predict, filename, begin, end, predict_score=None, predict_state=None, tqdm=None, caribrate=None, history_size=1, source=None):
    capture = open_video(source)

    metrics = Metrics(capture['size'][0], capture['size'][1])

    width = metrics.puyo_width()
    height = metrics.puyo_height()
    predicted_history = np.full((2, 12, 6, history_size), 'empty', dtype='U8')

    if end != None:
        end = capture['fps'] * 60 * end

    for image, frame_count in foreach_video_frame(capture['capture'], capture['fps'] * 60 * begin, end, tqdm):
        puyos = list(crop_puyo_images(image, metrics.field()))
        scores = crop_score_images(image, metrics)
        predicted_fields = [
            np.full((12, 6), 'empty', dtype='U8'),
            np.full((12, 6), 'empty', dtype='U8')
        ]

        if predict != None:
            predicted = predict(puyos).reshape(2, 12, 6)

            predicted_history = np.roll(predicted_history, 1, axis=3)
            predicted_history[:, :, :, 0] = predicted

            for k in range(2):
                for i in range(12):
                    for j in range(6):
                        puyo_top = int(height * i) + metrics.field()[k]['top']
                        puyo_left = int(width * j) + metrics.field()[k]['left']

                        if caribrate != None:
                            caribrated = caribrate(predicted_history[k, i, j, :])
                        else:
                            caribrated = predicted_history[k, i, j, 0]

                        predicted_fields[k][i, j] = caribrated


        predicted_scores = ['', '']
        if predict_score != None:
            for k in range(2):
                for i in range(8):
                    predicted_scores[k] += predict_score(scores[k][i])

        if predict_state != None:
            predicted_state = predict_state(predicted_history, predicted_scores)

        yield {
            'seconds': int(frame_count / capture['fps']),
            'fields': predicted_fields,
            'scores': predicted_scores,
            'state': predicted_state
        }

