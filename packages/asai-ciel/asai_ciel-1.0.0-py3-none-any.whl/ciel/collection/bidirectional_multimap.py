from typing import Dict, List, TypeVar, Generic

T = TypeVar('T')


class BidirectionalMultiMap(Generic[T]):
    _forward: Dict[T, List[T]]
    _backward: Dict[T, List[T]]

    def __init__(self):
        self._forward = {}
        self._backward = {}

    def __getitem__(self, key: T) -> List[T]:
        return self.forwards(key)

    def add(self, key: T, value: T):
        if key not in self._forward:
            self._forward[key] = []
        self._forward[key].append(value)

        if value not in self._backward:
            self._backward[value] = []
        self._backward[value].append(key)

    def forwards(self, key: T) -> List[T]:
        if key not in self._forward:
            return []
        return self._forward[key]

    def backwards(self, key: T) -> List[T]:
        if key not in self._backward:
            return []
        return self._backward[key]

    def keys(self):
        return self._forward.keys()

    def values(self):
        return self._backward.keys()

    def entries(self):
        return set([
            *self._forward.keys(),
            *self._backward.keys()
        ])
