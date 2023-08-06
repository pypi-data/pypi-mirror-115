from typing import Any
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten, Conv2D


class CNNPuyoClassifier():
    COLOR_INDICES = [
        'red',
        'blue',
        'green',
        'yellow',
        'purple',
        'ojama',
        'empty',
        'effect'
    ]

    model: Any

    def __init__(self, model):
        self.model = model

    @classmethod
    def _make_model(self, input_shape):
        output_dim = len(self.COLOR_INDICES)
        inputs = keras.Input(shape=input_shape, name='input')
        conv1 = Conv2D(36, 3, activation='relu')(inputs)
        flatten = Flatten()(conv1)
        d1 = Dense(64, activation='relu')(flatten)
        d2 = Dense(output_dim, activation='sigmoid')(d1)
        return keras.Model(inputs=inputs, outputs=d2, name='cnn_model')

    @classmethod
    def load(Self, path: str) -> 'CNNPuyoClassifier':
        model = keras.models.load_model(path)
        return CNNPuyoClassifier(model)

    @classmethod
    def train(Self, train_X, train_Y, test_X, test_Y, epochs=30):
        model = Self._make_model((12, 12, 3))
        model.compile(
            optimizer=keras.optimizers.Adam(lr=0.00001),
            loss='categorical_crossentropy',
            metrics=['acc'])

        train_dataset = tf.data.Dataset \
            .from_tensor_slices((train_X, train_Y)) \
            .shuffle(10000).batch(32)
        test_dataset = tf.data.Dataset \
            .from_tensor_slices((test_X, test_Y)) \
            .batch(32)

        model.fit(
            train_dataset,
            validation_data=test_dataset,
            shuffle=True,
            epochs=epochs)

        return CNNPuyoClassifier(model)

    def make_feature(self, images):
        puyos_feature = images.reshape((-1, 16, 16, 3))
        return puyos_feature.astype(np.float32)[:, 2:-2, 2:-2, :] / 255

    def save(self, path: str):
        self.model.save(path)

    def predict(self, images):
        feat = self.make_feature(images)
        # https://github.com/keras-team/keras/issues/13118
        output = self.model.predict_on_batch(np.array(feat))
        predict_indices = np.argmax(output, axis=1)
        predicts = list(map(lambda x: self.COLOR_INDICES[x], predict_indices))
        return np.squeeze(np.array(predicts))
