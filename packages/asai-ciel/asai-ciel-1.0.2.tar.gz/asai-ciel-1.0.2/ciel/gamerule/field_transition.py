import copy
from dataclasses import dataclass
from logging import getLogger
from typing import List, Tuple
import numpy as np

from abyss import Pair, Field, PuyoType
from ciel.transition.snapshot import Snapshot


@dataclass
class Transition():
    snapshot: Snapshot

    def to_pretty_string(self):
        return 'nodef'

    def to_dict(self):
        return None


@dataclass
class InitializeTransition(Transition):
    def to_pretty_string(self):
        return 'INITIALIZE'

    def to_dict(self):
        return None


@dataclass
class PutPairTransition(Transition):
    direction: str
    column: int
    pair: Pair
    is_fuzzy: bool = False

    def to_pretty_string(self):
        if not self.is_fuzzy:
            return f'PUT {self.column + 1}-{self.direction}'
        else:
            return f'PUT {self.column + 1}-{self.direction} (fuzzy)'

    def to_dict(self):
        return {
            'type': 'put',
            'column': int(self.column),
            'direction': self.direction,
            'pair': [self.pair[0], self.pair[1]],
            'time': self.snapshot.time
        }


@dataclass
class OjamaFallTransition(Transition):
    location: List[Tuple[int, int]]

    def to_pretty_string(self):
        return 'OJAMA ' + str(self.location)

    def to_dict(self):
        return {
            'type': 'ojama',
            'location': self.location,
            'time': self.snapshot.time
        }


@dataclass
class ChainStepTransition(Transition):
    def to_pretty_string(self):
        return 'CHAIN STEP'

    def to_dict(self):
        return None


def can_put_fuzzy(f: Field, col: int) -> bool:
    return (f.get(col, 1) == PuyoType.EMPTY
            and f.get(col, 2) != PuyoType.EMPTY)


def get_visible_changed(a: Field, b: Field) -> np.ndarray:
    r = np.array(a.to_array()) != np.array(b.to_array())
    r[:, :2] = False
    return r


def is_ojama(f: Field, where: np.ndarray) -> bool:
    return np.all(np.array(f.to_array())[where] == PuyoType.OJAMA)


def is_not_ojama(f: Field, where: np.ndarray) -> bool:
    return np.all(np.array(f.to_array())[where] != PuyoType.OJAMA)


def is_empty(f: Field, where: np.ndarray) -> bool:
    return np.all(np.array(f.to_array())[where] == PuyoType.EMPTY)


def enumerate_complete_fuzzy(destination: Snapshot, pair: Pair):
    dest_field = destination.field
    row_size = 6
    result = []

    # put vertically
    for i in range(row_size):
        if can_put_fuzzy(dest_field, i):
            cloned_field = destination.field.clone()
            cloned_field.set(i, 1, pair[0])
            cloned_field.set(i, 0, pair[1])
            cloned_dest = Snapshot(
                field=cloned_field,
                nexts=destination.nexts,
                frame=destination.frame,
                time=destination.time)
            result.append(PutPairTransition(
                snapshot=cloned_dest,
                column=i,
                direction='bottom',
                pair=pair,
                is_fuzzy=True))

            cloned_field = copy.copy(destination.field)
            cloned_field.set(i, 1, pair[1])
            cloned_field.set(i, 0, pair[0])
            cloned_dest = Snapshot(
                field=cloned_field,
                nexts=destination.nexts,
                frame=destination.frame,
                time=destination.time)
            result.append(PutPairTransition(
                snapshot=cloned_dest,
                column=i,
                direction='top',
                pair=pair,
                is_fuzzy=True))

    # put horizontally
    for i in range(row_size - 1):
        if (can_put_fuzzy(dest_field, i)
           and can_put_fuzzy(dest_field, i + 1)):

            cloned_field = copy.copy(destination.field)
            cloned_field.set(i, 1, pair[0])
            cloned_field.set(i + 1, 1, pair[1])
            cloned_dest = Snapshot(
                field=cloned_field,
                nexts=destination.nexts,
                frame=destination.frame,
                time=destination.time)
            result.append(PutPairTransition(
                snapshot=cloned_dest,
                column=i + 1,
                direction='left',
                pair=pair,
                is_fuzzy=True))

            cloned_field = copy.copy(destination.field)
            cloned_field.set(i, 1, pair[1])
            cloned_field.set(i + 1, 1, pair[0])
            cloned_dest = Snapshot(
                field=cloned_field,
                nexts=destination.nexts,
                frame=destination.frame,
                time=destination.time)
            result.append(PutPairTransition(
                snapshot=cloned_dest,
                column=i,
                direction='right',
                pair=pair,
                is_fuzzy=True))

    return result


def get_transitions(source: Snapshot,
                    destination: Snapshot) -> List[Transition]:
    """Detects a transition between two snapshots

    source, destination の間で発生した transition を返します．
    ファジーなどの理由で複数の transition が考えられる場合を考慮します．

    制限： 4 連続同じツモを 2 連続ファジー設置した場合が考慮できない．
    """
    logger = getLogger(__name__)

    source_field = source.field
    dest_field = destination.field
    changed = get_visible_changed(source_field, dest_field)
    num_changed = np.count_nonzero(changed)

    next_changed = not (
        source.nexts[0] == destination.nexts[0]
        and source.nexts[1] == destination.nexts[1])

    # TODO: Snapshot を immutable class にしたい
    destination = copy.deepcopy(destination)

    if (num_changed == 0
       and source.nexts[0][0] == PuyoType.EMPTY
       and source.nexts[0][1] == PuyoType.EMPTY):
        # 初期値からの遷移
        logger.debug('Detect initialize transition')
        return [InitializeTransition(snapshot=destination)]

    # chain
    chained_source_field = source.field.clone()
    source_chain_result = chained_source_field.chain()
    has_chain = source_chain_result.chain > 0

    # copy previous node fuzzy area
    for i in range(6):
        if (chained_source_field.get(i, 1) != PuyoType.EMPTY
           and destination.field.get(i, 2) != PuyoType.EMPTY):
            # どうせ 14 段目は落ちてこないのでコピーしない
            # destination.update_field(i, 0, source.field.get(i, 0))
            destination.update_field(i, 1, source.field.get(i, 1))

    # 連鎖中は操作できないので，ChainStepTransition が最優先で判定される
    if (has_chain and not next_changed):

        # chain stepped
        if chained_source_field == destination.field:
            logger.debug('Detect chain-step transition')
            return [
                ChainStepTransition(snapshot=destination)
            ]

        # chain stepped (ignoring fallen ojama from fuzzy area)
        # see: https://github.com/haripo/puyo-recognizer/issues/1
        chained_diff = (np.array(chained_source_field.to_array())
                        != np.array(destination.field.to_array()))
        if is_ojama(destination.field, where=chained_diff):
            logger.debug('Detect chain-step transition with ojama error')
            return [
                ChainStepTransition(snapshot=destination)
            ]

    if num_changed == 0:
        if next_changed and source.nexts[1] == destination.nexts[0]:
            logger.debug('Complete fuzzy transitions')
            return enumerate_complete_fuzzy(
                destination,
                source.nexts[0])
        elif source.nexts[0] == source.nexts[1]:
            # 3 連続で同じツモがきて，1 つめをファジーした場合
            logger.debug('Complete fuzzy transitions with same pairs')
            return enumerate_complete_fuzzy(
                destination,
                source.nexts[0])
        else:
            logger.debug('No changed')
            return []

    # {OjamaFall, PutPair}Transition cannot be happen while chain
    if has_chain:
        logger.debug('Invalid chain')
        return []

    # ojama fallen
    is_source_changed_empty = is_empty(source_field, where=changed)
    if (is_source_changed_empty
       and is_ojama(dest_field, where=changed)
       and not next_changed):
        location = list(map(
            lambda p: (int(p[0]), int(p[1])),
            zip(*np.where(changed))))
        logger.debug('Detect ojama-fall transition')
        return [OjamaFallTransition(snapshot=destination, location=location)]
        # NOTE: いったんおじゃまぷよのファジーは無視している．

    # puyo put
    if (is_source_changed_empty
       and is_not_ojama(dest_field, where=changed)):
        changed_row = np.where(np.count_nonzero(changed, axis=0))[0]
        changed_col = np.where(np.count_nonzero(changed, axis=1))[0]

        if source.nexts[1] != destination.nexts[0]:
            logger.debug('Invalid nexts')
            return []

        if num_changed == 2:
            # puyo put normally
            if len(changed_col) == 1:
                # TODO: above, below, left right の判定をリファクタリング
                above_puyo = dest_field.get(changed_col[0], np.min(changed_row))
                below_puyo = dest_field.get(changed_col[0], np.max(changed_row))

                if (above_puyo == source.nexts[0][0]
                   and below_puyo == source.nexts[0][1]):
                    # 下が軸ぷよ
                    logger.debug('Detect put-pair')
                    return [PutPairTransition(
                        snapshot=destination,
                        column=changed_col[0],
                        direction='top',
                        pair=source.nexts[0],
                        is_fuzzy=False)]
                if (below_puyo == source.nexts[0][0]
                   and above_puyo == source.nexts[0][1]):
                    # 上が軸ぷよ
                    logger.debug('Detect put-pair')
                    return [PutPairTransition(
                        snapshot=destination,
                        column=changed_col[0],
                        direction='bottom',
                        pair=source.nexts[0],
                        is_fuzzy=False)]
            elif abs(changed_col[0] - changed_col[1]) == 1:
                # assert len(changed_row) == 1
                left_col = np.min(changed_col)
                left_puyo = np.array(dest_field.to_array())[left_col, :][changed[left_col, :]]
                right_col = np.max(changed_col)
                right_puyo = np.array(dest_field.to_array())[right_col, :][changed[right_col, :]]
                if (right_puyo == source.nexts[0][0]
                   and left_puyo == source.nexts[0][1]):
                    logger.debug('Detect put-pair')
                    return [PutPairTransition(
                        snapshot=destination,
                        column=left_col,
                        direction='right',
                        pair=source.nexts[0],
                        is_fuzzy=False)]
                if (left_puyo == source.nexts[0][0]
                   and right_puyo == source.nexts[0][1]):
                    logger.debug('Detect put-pair')
                    return [PutPairTransition(
                        snapshot=destination,
                        column=right_col,
                        direction='left',
                        pair=source.nexts[0],
                        is_fuzzy=False)]

        # puyo put with fuzzy
        if num_changed == 1:
            fuzzy_transition: List[Transition] = []
            changed_index = np.where(changed)
            if dest_field.get(changed_index[0][0], changed_index[1][0]) == source.nexts[0][0]:
                c = source.nexts[0][1]
            else:
                c = source.nexts[0][0]

            col_left = changed_col[0] - 1
            col_right = changed_col[0] + 1

            if (changed_col[0] != 0
               and destination.field.get(col_left, 2) != PuyoType.EMPTY):

                cloned_dest = Snapshot(
                    field=destination.field.clone().set(col_left, 1, c),
                    nexts=destination.nexts,
                    frame=destination.frame,
                    time=destination.time)

                if c == source.nexts[0][0]:
                    fuzzy_transition.append(PutPairTransition(
                        snapshot=cloned_dest,
                        column=changed_col[0],
                        direction='left',
                        pair=source.nexts[0],
                        is_fuzzy=True))
                else:
                    fuzzy_transition.append(PutPairTransition(
                        snapshot=cloned_dest,
                        column=changed_col[0],
                        direction='right',
                        pair=source.nexts[0],
                        is_fuzzy=True))

            if (changed_col[0] != 5
               and destination.field.get(col_right, 2) != PuyoType.EMPTY):

                cloned_dest = Snapshot(
                    field=destination.field.clone().set(col_right, 1, c),
                    nexts=destination.nexts,
                    frame=destination.frame,
                    time=destination.time)

                if c == source.nexts[0][0]:
                    fuzzy_transition.append(PutPairTransition(
                        snapshot=cloned_dest,
                        column=changed_col[0],
                        direction='right',
                        pair=source.nexts[0],
                        is_fuzzy=True))
                else:
                    fuzzy_transition.append(PutPairTransition(
                        snapshot=cloned_dest,
                        column=changed_col[0],
                        direction='left',
                        pair=source.nexts[0],
                        is_fuzzy=True))

            # put fuzzy vertically
            if np.sum(changed[:, 2]) == 1:
                cloned_field = copy.copy(destination.field)
                cloned_field.set(changed_col[0], 1, c)
                cloned_dest = Snapshot(
                    field=cloned_field,
                    nexts=destination.nexts,
                    frame=destination.frame,
                    time=destination.time)

                if c == source.nexts[0][0]:
                    fuzzy_transition.append(PutPairTransition(
                        snapshot=cloned_dest,
                        column=changed_col[0],
                        direction='top',
                        pair=source.nexts[0],
                        is_fuzzy=True))
                else:
                    fuzzy_transition.append(PutPairTransition(
                        snapshot=cloned_dest,
                        column=changed_col[0],
                        direction='bottom',
                        pair=source.nexts[0],
                        is_fuzzy=True))

            logger.debug('Detect put-pair with fuzzy')
            return fuzzy_transition

    logger.debug('Invalid transition')
    return []
