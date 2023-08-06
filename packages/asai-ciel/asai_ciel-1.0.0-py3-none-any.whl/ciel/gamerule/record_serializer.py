import numpy as np
from ciel.gamerule.chain import emulate
from ciel.gamerule.field import FieldItem


FIELD_ROWS = 13
FIELD_COLS = 6

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
MAX_COLOR = 7

COLORS = [
    ''
    'red',
    'green',
    'blue',
    'yellow',
    'purple',
    'ojama'
]

COLOR_INDEX_MAP = {
    FieldItem.empty: 0,
    FieldItem.red: 1,
    FieldItem.green: 2,
    FieldItem.blue: 3,
    FieldItem.yellow: 4,
    FieldItem.purple: 5,
    FieldItem.ojama: 6
}

MOVE_LIST = [
  {'direction': 'top', 'column': 0},
  {'direction': 'top', 'column': 1},
  {'direction': 'top', 'column': 2},
  {'direction': 'top', 'column': 3},
  {'direction': 'top', 'column': 4},
  {'direction': 'top', 'column': 5},
  {'direction': 'bottom', 'column': 0},
  {'direction': 'bottom', 'column': 1},
  {'direction': 'bottom', 'column': 2},
  {'direction': 'bottom', 'column': 3},
  {'direction': 'bottom', 'column': 4},
  {'direction': 'bottom', 'column': 5},
  {'direction': 'right', 'column': 0},
  {'direction': 'right', 'column': 1},
  {'direction': 'right', 'column': 2},
  {'direction': 'right', 'column': 3},
  {'direction': 'right', 'column': 4},
  {'direction': 'left', 'column': 1},
  {'direction': 'left', 'column': 2},
  {'direction': 'left', 'column': 3},
  {'direction': 'left', 'column': 4},
  {'direction': 'left', 'column': 5},
]


def move_to_index(record):
    for i in range(len(MOVE_LIST)):
        move = MOVE_LIST[i]

        if record['column'] == 0 and record['direction'] == 'left':
            record['column'] = 1

        if (record['column'] == move['column'] and
           record['direction'] == move['direction']):
            return i

    raise RuntimeError('Unexpected record')


def serialize_queue(records):
    result = ''
    for r in records:
        if r['type'] != 'put':
            continue
        pair = list(map(lambda p: COLOR_INDEX_MAP[p], r['pair']))
        result += CHARS[pair[1] * MAX_COLOR + pair[0]]
    return result


def serialize_moves(records):
    result = ''
    field = np.full((6, 15), FieldItem.empty)
    # ぷよの設置のためフィールドの高さを +2 としている

    for r in records:
        if r['type'] == 'put':
            result += CHARS[move_to_index(r)]
            if r['direction'] == 'top':
                field[r['column'], 0] = r['pair'][0]
                field[r['column'], 1] = r['pair'][1]
            elif r['direction'] == 'bottom':
                field[r['column'], 0] = r['pair'][1]
                field[r['column'], 1] = r['pair'][0]
            elif r['direction'] == 'right':
                field[r['column'], 0] = r['pair'][1]
                field[r['column'] + 1, 0] = r['pair'][0]
            elif r['direction'] == 'left':
                field[r['column'], 0] = r['pair'][1]
                field[r['column'] - 1, 0] = r['pair'][0]

            emulate(field)

        if r['type'] == 'ojama':
            for l in r['location']:
                field[l[0], l[1] + 2] = FieldItem.ojama

            str_field = ''
            for i in range(13):
                for j in range(6):
                    str_field += str(COLOR_INDEX_MAP[field[j, i + 2]])
            result += '5'
            result += str_field

    return result + '9'
