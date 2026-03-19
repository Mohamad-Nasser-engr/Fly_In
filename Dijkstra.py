from enum import Enum
from math import inf
from typing import Any, Optional, Set, List
import heapq


class ZoneType(Enum):
    NORMAL = 1
    RESTRICTED = 2
    PRIORITY = 0.9
    BLOCKED = float('inf')


class Dijkstra():
    def __init__(self, input_data: dict[str, Any]):
        self.input_data = input_data
        self.start = [key for key in input_data
                      if input_data[key]["is_start"]][0]
        self.end = [key for key in input_data
                    if input_data[key]["is_end"]][0]
        self.distances: dict[str,
                             float | int] = {key: float(inf)
                                             if not input_data[key]["is_start"]
                                             else 0
                                             for key in input_data}
        self.previous: dict[str, Optional[str]] = {key: None
                                                   for key in input_data}
        self.visited: Set[str] = set()
        self.pq: List[tuple[float | int, str]] = []
        heapq.heappush(self.pq, (0, self.start))
        print(self.start)
        print(self.end)
        print(self.distances)
        print(self.previous)
        print(self.pq)
        print(self.visited)

    def process(self) -> None:
        while (len(self.pq) != 0):
            old_cost, cur_node = heapq.heappop(self.pq)
            if cur_node in self.visited:
                continue
            if (self.input_data[cur_node]["is_end"]):
                break
            self.visited.add(cur_node)
            for neighbor in self.input_data[cur_node]["connections"]:
                zone_type = ZoneType[self.input_data[neighbor]["zone"].upper()]
                if (zone_type == ZoneType.BLOCKED or neighbor in self.visited):
                    continue
                cost = zone_type.value + old_cost
                if cost < self.distances[neighbor]:
                    self.distances[neighbor] = cost
                    self.previous[neighbor] = cur_node
                    heapq.heappush(self.pq,
                                   (self.distances[neighbor], neighbor))
