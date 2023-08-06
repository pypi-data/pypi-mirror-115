import numpy as np
from collections import deque
from typing import Any, List, Dict, Deque
from ciel.collection.counting_queue import CountingQueue
import ciel.classifier.cnn_puyo_classifier as cnn


class FieldRecognizer:
    NUM_PLAYERS = 2
    FIELD_WIDTH = 6
    FIELD_HEIGHT = 12

    classifier: Any

    history_size: int
    batch_size: int
    prediction_queue: Dict[int, CountingQueue[str]]
    effect_count_queue: List[Deque[int]]

    def __init__(self, path: str,
                 calibration_span: int = 5):
        self.history_size = calibration_span
        self.prediction_queue = {}
        self.batch_size = (self.NUM_PLAYERS *
                           self.FIELD_WIDTH * self.FIELD_HEIGHT)
        self.effect_count_queue = [
            deque([0] * calibration_span),
            deque([0] * calibration_span)
        ]

        for i in range(self.batch_size):
            self.prediction_queue[i] = CountingQueue(length=calibration_span)

        self.classifier = cnn.CNNPuyoClassifier.load(path)

    def predict(self, images):
        predicted = self.classifier.predict(images)

        calibrated = np.full((self.batch_size, ), '', dtype='U8')
        for i in range(self.batch_size):
            if predicted[i] != 'effect':
                self.prediction_queue[i].add(predicted[i])
            calibrated[i] = self.prediction_queue[i].mode()

        # TODO: このへんのマジックナンバなんとかする
        calibrated = calibrated.reshape(2, 6, 12)
        predicted = predicted.reshape(2, 6, 12)

        # count effects
        for i in range(2):
            effect_count = np.sum(predicted[i, :, :] == 'effect')
            self.effect_count_queue[i].append(effect_count)
            self.effect_count_queue[i].popleft()

        # remove floating puyos
        for i in range(2):
            for j in range(6):
                for k in range(11):
                    if (calibrated[i, j, 10 - k] != 'empty' and
                       calibrated[i, j, 11 - k] == 'empty'):
                        calibrated[i, j, 10 - k] = 'empty'

        return calibrated

    def get_effect_count(self):
        return [
            sum(self.effect_count_queue[0]) / self.history_size,
            sum(self.effect_count_queue[1]) / self.history_size
        ]
