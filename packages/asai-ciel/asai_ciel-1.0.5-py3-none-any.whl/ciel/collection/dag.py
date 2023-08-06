from typing import List, Dict, Tuple
from ciel.collection.bidirectional_multimap import BidirectionalMultiMap


class DAG:
    edges: BidirectionalMultiMap[int]
    weights: Dict[Tuple[int, int], int]

    def __init__(self):
        self.edges = BidirectionalMultiMap()
        self.weights = {}

    def append(self, source: int, destination: int, weight: int):
        if (source, destination) not in self.weights:
            self.edges.add(source, destination)
            self.weights[(source, destination)] = weight

    def topological_order(self):
        result = []

        subgraph = {n: 0 for n in self.edges.entries()}
        for s in self.edges.keys():
            for d in self.edges.forwards(s):
                subgraph[d] += 1

        while 0 < len(subgraph):
            head_nodes = [n for n in subgraph.keys() if subgraph[n] == 0]

            if len(head_nodes) == 0:
                raise RuntimeError('Graph is not DAG')

            for node in head_nodes:
                for forward in self.edges.forwards(node):
                    subgraph[forward] -= 1

            for node in head_nodes:
                subgraph.pop(node)

            result.extend(head_nodes)

        return result

    def find_shortest_path(self, start: int, end: List[int]):
        distances = {n: 2**63 for n in self.edges.entries()}
        distances[start] = 0
        back_path = {}

        for n in self.topological_order():
            for m in self.edges.forwards(n):
                if distances[n] + self.weights[(n, m)] < distances[m]:
                    distances[m] = distances[n] + self.weights[(n, m)]
                    back_path[m] = n

        n = end[0]
        for end_node in end:
            if distances[n] < distances[end_node]:
                n = end_node

        path = [n]
        while n != start:
            n = back_path[n]
            path.append(n)
        path.reverse()

        return path

    def find_backward_neighbor(self, node: int, max_step: int) -> List[int]:
        """Find nodes that can reach from given node in max_step steps,
        using most farthest path
        """
        steps = {n: -2**63 for n in self.edges.entries()}
        steps[node] = 0

        for n in reversed(self.topological_order()):
            for m in self.edges.backwards(n):
                if steps[m] <= steps[n]:
                    steps[m] = steps[n] + 1

        return list(filter(lambda n: 0 <= steps[n] <= max_step, steps))

    def find_longest_path(self, node: int) -> List[int]:
        steps = {n: -2**63 for n in self.edges.entries()}
        steps[node] = 0
        back_path = {}

        for n in self.topological_order():
            for m in self.edges.forwards(n):
                if steps[m] <= steps[n]:
                    steps[m] = steps[n] + 1
                    back_path[m] = n

        end = [n for n in steps.keys() if steps[n] == max(steps.values())][0]
        path = [end]
        while end != node:
            end = back_path[end]
            path.append(end)

        path.reverse()
        return path

