import numpy as np
from typing import Any, Dict
from ciel.collection.counting_queue import CountingQueue
import ciel.classifier.cnn_puyo_classifier as cnn


class NextRecognizer:
    NUM_PLAYERS = 2
    NUM_NEXT = 2

    classifier: Any

    history_size: int
    prediction_queue: Dict[int, CountingQueue[str]]

    def __init__(self, path: str,
                 calibration_span: int = 5):
        self.history_size = calibration_span
        self.prediction_queue = {}
        self.batch_size = self.NUM_PLAYERS * self.NUM_NEXT * 2

        for i in range(self.batch_size):
            self.prediction_queue[i] = CountingQueue(length=calibration_span)

        self.classifier = cnn.CNNPuyoClassifier.load(path)

    def predict(self, images):
        predicted = self.classifier.predict(images)

        calibrated = np.full((self.batch_size, ), '', dtype='U8')
        for i in range(self.batch_size):
            if predicted[i] not in ['effect', 'ojama', 'empty']:
                self.prediction_queue[i].add(predicted[i])
            mode = self.prediction_queue[i].mode()
            if mode is not None:
                calibrated[i] = mode
            else:
                calibrated[i] = 'empty'

        return calibrated.reshape((self.NUM_PLAYERS, self.NUM_NEXT, 2))
