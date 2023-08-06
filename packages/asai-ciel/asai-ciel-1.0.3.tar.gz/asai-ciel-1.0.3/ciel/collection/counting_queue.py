from collections import defaultdict
from typing import Dict, List, Optional, TypeVar, Generic

T = TypeVar('T')


class CountingQueue(Generic[T]):
    data: List[Optional[T]]
    length: int
    last: int
    count: Dict[T, int]
    max_value: Optional[T]

    def __init__(self, length):
        self.length = length
        self.data = [None] * length
        self.count = defaultdict(int)
        self.last = 0
        self.max_value = None

    def add(self, value: T):
        prev_value = self.data[self.last]

        if prev_value is not None:
            self.count[prev_value] -= 1
        self.data[self.last] = value
        self.count[value] += 1

        if (self.max_value is None
           or self.count[self.max_value] <= self.count[value]):
            self.max_value = value

        self.last = (self.last + 1) % self.length

    def mode(self):
        return self.max_value
