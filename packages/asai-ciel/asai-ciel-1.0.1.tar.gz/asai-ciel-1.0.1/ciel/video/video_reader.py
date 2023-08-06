import os
import datetime
import cv2
import numpy as np
from typing import Any, Tuple


class VideoReader:
    """Provides basic video input"""

    path: str
    capture: Any

    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def fps(self) -> int:
        return round(self.capture.get(cv2.CAP_PROP_FPS))

    @property
    def length(self) -> int:
        return round(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def width(self) -> int:
        return round(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self) -> int:
        return round(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def position(self) -> datetime.timedelta:
        return datetime.timedelta(
            seconds=int(self.capture.get(cv2.CAP_PROP_POS_MSEC) / 1000))

    @property
    def size(self) -> Tuple[int, int]:
        return (self.width, self.height)

    def open(self):
        if not os.path.exists(self.path):
            raise RuntimeError(f'File not found {self.path}')

        self.capture = cv2.VideoCapture(self.path)

        if not self.capture.isOpened:
            raise RuntimeError(f'Failed to open {self.path}')

    def close(self):
        self.capture.release()

    def foreach_frame(self, begin_frame=0, end_frame=None, tqdm=None):
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, begin_frame)

        if end_frame is None:
            end_frame = self.length

        progress = None
        if tqdm:
            progress = tqdm(total=end_frame - begin_frame - 1)

        frame_iter = begin_frame

        while self.capture.isOpened():
            ret, frame = self.capture.read()
            if not ret:
                break

            frame_iter += 1

            if end_frame < frame_iter:
                break

            yield np.array(frame), frame_iter

            if progress:
                progress.update(1)
