import copy
import numpy as np
from typing import Optional, List
from colorama import Back, Style
from abyss import ArrayField, Pair, PuyoType


# TODO: 画像認識の結果を表すクラスと snapshot_graph のノードを表すクラスを分離する
# snapshot_graph のノードには 13 段目の推論結果が含まれるはず
class Snapshot:
    frame: Optional[int]
    time: Optional[float]
    field: ArrayField
    nexts: List[Pair]  # ネクストは 0 が child，1 が axis

    def __init__(
            self,
            field: ArrayField,
            nexts: List[Pair],
            frame: Optional[int] = None,
            time: Optional[float] = None):
        self.frame = frame
        self.time = time
        self.field = field
        self.nexts = nexts

    def __eq__(self, other):
        if not isinstance(other, Snapshot):
            return False
        return self.is_same_without_frame(other) and self.frame == other.frame

    def __hash__(self):
        # FIXME: may slow
        return hash((
            np.array(self.field.to_array()).tostring(),
            self.nexts[0][0],
            self.nexts[1][0],
            self.nexts[0][1],
            self.nexts[1][1],
            self.frame,
            self.time))

    def __copy__(self):
        # args are copied in costructor
        return Snapshot(
            copy.copy(self.field),
            copy.copy(self.nexts),
            self.frame,
            self.time
        )

    def __deepcopy__(self, memo):
        return self.__copy__()

    def update_field(self, col, row, value):
        self.field.set(col, row, value)

    def is_same_without_frame(self, other: 'Snapshot'):
        return self.field == other.field and self.nexts == other.nexts

    def is_same_without_frame_and_fuzzy(self, other: 'Snapshot'):
        return (self.field.equals_without_fuzzy(other.field)
                and self.nexts == other.nexts)

    def print(self, message=None, capitalize=None):
        print(f'==== frame: {self.frame}, message: {message}')

        colorama_colors = {
            PuyoType.RED: Back.RED,
            PuyoType.BLUE: Back.BLUE,
            PuyoType.GREEN: Back.GREEN,
            PuyoType.YELLOW: Back.YELLOW,
            PuyoType.PURPLE: Back.MAGENTA,
            PuyoType.OJAMA: Back.WHITE,
            PuyoType.EMPTY: Back.RESET
        }

        print('NEXT:')
        for i in range(2):
            for j in range(2):
                c = colorama_colors[self.nexts[i][j]]
                if self.nexts[i][j] == PuyoType.EMPTY:
                    print('__', end='')
                else:
                    # name = self.nexts[i, j].name[0]
                    print(c + '__', end='')
            print(Style.RESET_ALL, end=',')
        print('')

        print('FIELD:')
        for i in range(14):
            for j in range(6):
                c = colorama_colors[self.field.get(j, i)]
                if self.field.get(j, i) == PuyoType.EMPTY:
                    if capitalize is not None and capitalize[j, i]:
                        print('..', end='')
                    else:
                        print('__', end='')
                else:
                    # name = self.field[j, i].name[0].upper()
                    if self.field.get(j, i) == PuyoType.PURPLE:
                        print(c + '**', end='')
                    else:
                        print(c + '__', end='')
                print(Style.RESET_ALL, end='')
            print('')
