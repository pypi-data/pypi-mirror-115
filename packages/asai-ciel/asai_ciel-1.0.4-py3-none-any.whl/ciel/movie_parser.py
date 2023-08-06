import cv2
import numpy as np
from typing import Tuple, Optional
from ciel.bounds import PuyoScreenBounds


class MovieParser:
    bounds: PuyoScreenBounds

    def __init__(self, bounds: PuyoScreenBounds):
        self.bounds = bounds

    def crop_puyo_images(self, image, size: Optional[Tuple[int, int]] = None):
        if size is None:
            size = (
                self.bounds.field_puyo.width,
                self.bounds.field_puyo.height)

        puyo_images = np.zeros((2, 6, 12, size[1], size[0], 3))

        for k in range(2):
            for i in range(6):
                for j in range(12):
                    puyo_bound = self.bounds.get_field_puyo(k, i, j)
                    puyo_image = image[puyo_bound.slice]
                    puyo_image = cv2.resize(puyo_image, size)
                    puyo_images[k, i, j, :, :, :] = puyo_image
        return puyo_images

    def crop_next_images(self, image, size: Optional[Tuple[int, int]] = None):
        if size is None:
            size = (
                self.bounds.field_puyo.width,
                self.bounds.field_puyo.height)

        puyo_images = np.zeros((2, 2, 2, size[1], size[0], 3))

        for k in range(2):
            for i in range(2):
                for j in range(2):
                    puyo_bound = self.bounds.get_next_puyo(k, i, j)
                    puyo_image = image[puyo_bound.slice]
                    puyo_image = cv2.resize(puyo_image, size)
                    puyo_images[k, i, j, :, :, :] = puyo_image
        return puyo_images

    def crop_score_images(self, image, size: Optional[Tuple[int, int]] = None):
        if size is None:
            size = (
                self.bounds.score_number.width,
                self.bounds.score_number.height)

        number_images = np.zeros((2, 8, size[1], size[0], 3))

        for player_index in range(2):
            for i in range(8):
                digit_bound = self.bounds.get_score_number(player_index, i)
                number_image = image[digit_bound.slice]
                number_image = cv2.resize(number_image, size)
                number_images[player_index, i, :, :, :] = number_image

        return number_images

    def parse_image(self, image):
        return {
            'puyos': self.crop_puyo_images(image),
            'nexts': self.crop_next_images(image),
            'scores': self.crop_score_images(image)
        }
