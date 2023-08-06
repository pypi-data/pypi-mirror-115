from enum import Enum, auto


class GameState(Enum):
    UNKNOWN = auto()
    OTHER = auto()
    MATCH_START = auto()
    MATCHING = auto()
    MATCH_END = auto()
    WIN_1P = auto()
    WIN_2P = auto()


WIN_EFFECT_THRESHOLD = 50


class GameStateRecognizer:
    prev_state: GameState

    def __init__(self):
        self.prev_state = GameState.OTHER

    def predict(self, scores, effect_count):
        state = GameState.OTHER

        if (scores[0] + scores[1]).count(' ') <= 14:
            state = GameState.MATCHING
        if (effect_count[0] > WIN_EFFECT_THRESHOLD
           and effect_count[1] < WIN_EFFECT_THRESHOLD):
            state = GameState.WIN_2P
        if (effect_count[1] > WIN_EFFECT_THRESHOLD
           and effect_count[0] < WIN_EFFECT_THRESHOLD):
            state = GameState.WIN_1P

        if ((self.prev_state != GameState.MATCHING and
           self.prev_state != GameState.MATCH_START) and
           state == GameState.MATCHING):
            state = GameState.MATCH_START

        if (self.prev_state == GameState.MATCHING and
           (state == GameState.WIN_1P or state == GameState.WIN_2P)):
            state = GameState.MATCH_END

        self.prev_state = state
        return state
