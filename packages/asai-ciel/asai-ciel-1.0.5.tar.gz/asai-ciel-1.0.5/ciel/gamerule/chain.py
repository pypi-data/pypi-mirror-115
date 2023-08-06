import numpy as np
# from numba import jit
from typing import Any, Tuple
from ciel.gamerule.field import FieldItem


Field = Any


CHAIN_BONUS_TABLE = [
  0,
  8,
  16,
  32,
  64,
  96,
  128,
  160,
  192,
  224,
  256,
  288,
  320,
  352,
  384,
  416,
  448,
  480,
  512
]

CONNECTION_BONUS_TABLE = [
  0,
  2,
  3,
  4,
  5,
  6,
  7,
  10
]

COLOR_BONUS_TABLE = [
  0,
  3,
  6,
  12,
  24
]

OJAMA_RATE = 70


# @jit
def get_region_labels_search(i, j, id, color, ids, field):
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    ids[i, j] = id
    for (dx, dy) in directions:
        di = i + dx
        dj = j + dy
        if (0 <= di and di < field.shape[0]
           and 1 <= dj and dj < field.shape[1]
           and field[di, dj] == color
           and ids[di, dj] == -1):
            get_region_labels_search(di, dj, id, color, ids, field)


# @jit
def get_region_labels(field: Field):
    ids = np.full(field.shape, -1)

    new_id = 0
    for i in range(field.shape[0]):
        for j in range(1, field.shape[1]):
            if (ids[i, j] == -1
               and field[i, j] != int(FieldItem.empty.value)
               and field[i, j] != int(FieldItem.ojama.value)):
                get_region_labels_search(i, j, new_id, field[i, j], ids, field)
                new_id += 1

    return ids


def vanish(chain_source: Field, chain_count=1) -> Tuple[Field, int]:
    vanish_flag = np.full(chain_source.shape, False)
    viewed_flag = np.full(chain_source.shape, False)
    w, h = chain_source.shape
    conn_bonus = 0

    labels = get_region_labels(chain_source)
    label_count = dict(zip(*np.unique(labels, return_counts=True)))

    for i in range(w):
        for j in range(1, h):
            if (viewed_flag[i, j]
               or chain_source[i, j] in [FieldItem.ojama, FieldItem.empty]):
                continue
            positions = labels == labels[i, j]
            connection = label_count[labels[i, j]]
            viewed_flag[positions] = True
            if connection >= 4:
                vanish_flag[positions] = True
                conn_bonus += CONNECTION_BONUS_TABLE[min(connection - 4, 7)]

    num_color = len(np.unique(chain_source[vanish_flag]))
    chain_source[vanish_flag] = FieldItem.empty

    flag_neighbor = np.copy(vanish_flag)
    flag_neighbor[1:w, 0:h] |= vanish_flag[0:w-1, 0:h]
    flag_neighbor[0:w-1, 0:h] |= vanish_flag[1:w, 0:h]
    flag_neighbor[0:w, 1:h] |= vanish_flag[0:w, 0:h-1]
    flag_neighbor[0:w, 0:h-1] |= vanish_flag[0:w, 1:h]

    vanish_ojama_position = flag_neighbor & (chain_source == FieldItem.ojama)
    chain_source[vanish_ojama_position] = FieldItem.empty

    score = 10 * np.sum(vanish_flag) * np.clip(
        conn_bonus
        + CHAIN_BONUS_TABLE[chain_count - 1]
        + COLOR_BONUS_TABLE[num_color - 1], 1, 999)

    return chain_source, int(score)


def fall(chain_source: Field) -> Field:
    for i in range(chain_source.shape[0]):
        stack_head = chain_source.shape[1]
        for j in range(chain_source.shape[1] - 2, -1, -1):
            if (chain_source[i, j] != FieldItem.empty
               and chain_source[i, j + 1] == FieldItem.empty):
                chain_source[i, stack_head - 1] = chain_source[i, j]
                chain_source[i, j] = FieldItem.empty
                stack_head -= 1
            if chain_source[i, j + 1] != FieldItem.empty:
                stack_head = j + 1

    return chain_source


def step(chain_source: Field) -> Field:
    vanish(chain_source)
    fall(chain_source)
    return chain_source


def emulate(source: Field) -> Tuple[Field, int]:
    total_score = 0
    for i in range(20):
        fall(source)
        _, score = vanish(source, i + 1)
        total_score += score
        if score == 0:
            break
    return source, total_score
