import cv2
from typing import Any, Tuple


class VideoWriter:
    path: str
    fps: int
    size: Tuple[int, int]
    writer: Any

    def __init__(self, path: str, fps: int, size: Tuple[int, int]):
        self.path = path
        self.fps = fps
        self.size = size

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        self.writer = cv2.VideoWriter(self.path, fourcc, self.fps, self.size)

    def close(self):
        self.writer.release()

    def write(self, frame):
        self.writer.write(frame)
