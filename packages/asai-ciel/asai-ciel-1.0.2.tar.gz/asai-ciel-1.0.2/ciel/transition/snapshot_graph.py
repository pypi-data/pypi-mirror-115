from typing import List, Dict, Tuple, Optional
from ciel.collection.dag import DAG
from ciel.transition.snapshot import Snapshot
from ciel.gamerule.field_transition import (
    Transition,
    get_transitions,
    PutPairTransition,
    OjamaFallTransition)
from abyss import ArrayField, Pair, PuyoType


class SnapshotGraph:
    dag: DAG
    nodes: Dict[int, Snapshot]
    transitions: Dict[Tuple[int, int], Transition]
    head: Optional[int]
    tail: List[int]
    skippable: int
    appended_nodes: List[List[int]]

    def __init__(self, skippable: int = 20, initial_field=None):
        if initial_field is None:
            initial_field = Snapshot(
                ArrayField(),
                [
                    Pair(PuyoType.EMPTY, PuyoType.EMPTY),
                    Pair(PuyoType.EMPTY, PuyoType.EMPTY)
                ],
                frame=0)
        self.dag = DAG()
        self.nodes = {
            0: initial_field
        }
        self.head = 0
        self.tail = [0]
        self.skippable = skippable
        self.appended_nodes = [[0]]
        self.transitions = {}

    def is_duplicated_snapshot(self, snapshot: Snapshot) -> bool:
        for tail_node in self.tail:
            if self.nodes[tail_node].is_same_without_frame(snapshot):
                return True
        return False

    def append(self, snapshot: Snapshot):
        source_nodes = set()
        for tail_nodes in self.appended_nodes[-self.skippable:]:
            for node in tail_nodes:
                source_nodes.add(node)

        # find all transitions and add nodes
        snapshot_node: Dict[Snapshot, int] = {}
        for source in source_nodes:
            for t in get_transitions(self.nodes[source], snapshot):
                if self.is_duplicated_snapshot(t.snapshot):
                    continue

                # add new node if not exists
                if t.snapshot not in snapshot_node:
                    new_node = len(self.nodes)
                    self.nodes[new_node] = t.snapshot
                    snapshot_node[t.snapshot] = new_node

                new_node = snapshot_node[t.snapshot]

                # add edge
                self.dag.append(source, new_node, 0)
                self.transitions[(source, new_node)] = t

        if len(snapshot_node) > 0:
            self.tail = list(snapshot_node.values())
            self.appended_nodes.append(self.tail)

    def find_path(self):
        if len(self.tail) == 0 or self.head is None:
            return []
        for k, v in reversed(sorted(self.nodes.items(), key=lambda kv: kv[1].frame)):
            path = self.dag.find_shortest_path(self.head, [k])
            if len(path) > 0:
                return path
        return []

    def find_transitions(self):
        prev_node = 0
        path = self.find_path()
        for node in path:
            if (prev_node, node) not in self.transitions:
                prev_node = node
                continue
            transition = self.transitions[(prev_node, node)]
            if (isinstance(transition, PutPairTransition)
               or isinstance(transition, OjamaFallTransition)):
                yield transition
            prev_node = node
