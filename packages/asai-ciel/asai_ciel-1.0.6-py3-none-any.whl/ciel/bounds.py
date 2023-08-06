from dataclasses import dataclass


@dataclass
class Bound:
    top: int
    bottom: int
    left: int
    right: int
    width: int
    height: int

    @staticmethod
    def of(t, b, l, r):
        return Bound(
            t,
            b,
            l,
            r,
            r - l,
            b - t)

    @staticmethod
    def of_size(t, l, w, h):
        return Bound(
            t,
            t + h,
            l,
            l + w,
            w,
            h)

    @property
    def slice(self):
        return slice(self.top, self.bottom), slice(self.left, self.right)


@dataclass
class Size:
    width: int
    height: int


class PuyoScreenBounds:
    def __init__(self, width):
        self.scale = width / 1280.0

        self.fields = [
            Bound.of(
                int(105 * self.scale),
                int(585 * self.scale),
                int(186 * self.scale),
                int(447 * self.scale)),
            Bound.of(
                int(105 * self.scale),
                int(585 * self.scale),
                int(834 * self.scale),
                int(1096 * self.scale)),
        ]

        self.scores = [
            Bound.of_size(
                int(590 * self.scale),
                int(234 * self.scale),
                int(214 * self.scale),
                int(35 * self.scale)),
            Bound.of_size(
                int(590 * self.scale),
                int(833 * self.scale),
                int(214 * self.scale),
                int(35 * self.scale))
        ]

        self.nexts = [
            [
                [
                    Bound.of_size(
                        int(109 * self.scale),
                        int(480 * self.scale),
                        int(44 * self.scale),
                        int(40 * self.scale)),
                    Bound.of_size(
                        int((109 + 40) * self.scale),
                        int(480 * self.scale),
                        int(44 * self.scale),
                        int(40 * self.scale))
                ],
                [
                    Bound.of_size(
                        int(195 * self.scale),
                        int(513 * self.scale),
                        int(36 * self.scale),
                        int(32 * self.scale)),
                    Bound.of_size(
                        int((195 + 34) * self.scale),
                        int(513 * self.scale),
                        int(36 * self.scale),
                        int(32 * self.scale))
                ]
            ],
            [
                [
                    Bound.of_size(
                        int(109 * self.scale),
                        int(757 * self.scale),
                        int(44 * self.scale),
                        int(40 * self.scale)),
                    Bound.of_size(
                        int((109 + 40) * self.scale),
                        int(757 * self.scale),
                        int(44 * self.scale),
                        int(40 * self.scale)),
                ],
                [
                    Bound.of_size(
                        int(195 * self.scale),
                        int(731 * self.scale),
                        int(36 * self.scale),
                        int(32 * self.scale)),
                    Bound.of_size(
                        int((195 + 34) * self.scale),
                        int(731 * self.scale),
                        int(36 * self.scale),
                        int(32 * self.scale))
                ]
            ]
        ]

        self.score_number = Size(
            int(27 * self.scale),
            int(35 * self.scale))

        self.field_puyo = Size(
            int((self.fields[0].right - self.fields[0].left) / 6),
            int((self.fields[0].bottom - self.fields[0].top) / 12))

    def get_field_puyo(self, player: int, row: int, col: int) -> Bound:
        return Bound.of_size(
            self.fields[player].top + int(col * self.field_puyo.height),
            self.fields[player].left + int(row * self.field_puyo.width),
            self.field_puyo.width,
            self.field_puyo.height)

    def get_next_puyo(self, player: int, pair: int, puyo: int) -> Bound:
        return self.nexts[player][pair][puyo]

    def get_score_number(self, player: int, digit: int) -> Bound:
        # score_number.width == 27 だが，
        # self.scores[player].width / 8 == 26.75 と微妙に異なる．
        # left を求める時 score_number.width * digit とするとこの差が顕著に現れるので，
        # あえて後者の数値を用いている．
        return Bound.of_size(
            self.scores[player].top,
            self.scores[player].left
            + int((self.scores[player].width / 8) * digit),
            self.score_number.width,
            self.score_number.height)
