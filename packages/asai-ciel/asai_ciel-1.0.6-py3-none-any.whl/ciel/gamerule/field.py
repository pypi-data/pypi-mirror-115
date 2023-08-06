import enum
# import numpy as np
# import numba
# from typing import Any


class FieldItem(enum.IntEnum):
    empty = 0
    ojama = 1
    red = 2
    blue = 3
    yellow = 4
    green = 5
    purple = 6


# FIELD_ROWS = 13
# FIELD_COLS = 6
# FIELD_SHAPE = (FIELD_COLS, FIELD_ROWS)


# Field = np.ndarray
# Nexts = np.ndarray


# def empty_field() -> Field:
#     return np.full(FIELD_SHAPE, FieldItem.empty, dtype=np.dtype('u8'))


# def from_str(s: str) -> Field:
#     if len(s) != FIELD_ROWS * FIELD_COLS:
#         raise RuntimeError('Invalid shape of string')

#     charmap = {
#         ' ': FieldItem.empty,
#         'o': FieldItem.ojama,
#         'r': FieldItem.red,
#         'g': FieldItem.green,
#         'y': FieldItem.yellow,
#         'b': FieldItem.blue,
#         'p': FieldItem.purple
#     }
#     field = empty_field()
#     for i in range(FIELD_ROWS):
#         for j in range(FIELD_COLS):
#             field[j, i] = charmap[s[i * FIELD_COLS + j]]
#     return field


# def from_str_array(str_field: Any) -> Field:
#     result = empty_field()
#     row_begin = FIELD_ROWS - str_field.shape[1]

#     for i in range(FIELD_ROWS - row_begin):
#         for j in range(FIELD_COLS):
#             result[j, row_begin + i] = FieldItem[str_field[j, i]]
#     return result


# def next_from_str_array(str_nexts: Any) -> Field:
#     result = np.full((2, 2), FieldItem.empty, dtype=np.dtype('u8'))
#     for i in range(2):
#         for j in range(2):
#             result[j, i] = FieldItem[str_nexts[j, i]]
#     return result


# @numba.njit
# def next_same(a: Nexts, b: Nexts) -> bool:
#     return np.array_equal(a, b)


# @numba.njit
# def equals(a: Field, b: Field) -> bool:
#     return np.array_equal(a, b)


# @numba.njit
# def equals_without_fuzzy(a: Field, b: Field) -> bool:
#     return np.array_equal(a[:, 1:], b[:, 1:])


# @numba.njit
# def get_visible_changed(a: Field, b: Field) -> np.ndarray:
#     r = a != b
#     r[:, 0] = False
#     return r


# @numba.njit
# def can_put_fuzzy(f: Field, col: int) -> bool:
#     return (f[col, 0] == FieldItem.empty.value
#             and f[col, 1] != FieldItem.empty.value)


# def is_empty(f: Field, where: np.ndarray) -> bool:
#     return np.all(f[where] == FieldItem.empty.value)


# def is_ojama(f: Field, where: np.ndarray) -> bool:
#     return np.all(f[where] == FieldItem.ojama.value)


# def is_not_ojama(f: Field, where: np.ndarray) -> bool:
#     return np.all(f[where] != FieldItem.ojama.value)


# @numba.njit
# def update(source: Field, col: int, row: int, item: FieldItem):
#     r = np.copy(source)
#     r[col, row] = item
#     return r
