from enum import Enum
from math import inf
from typing import Any, Optional, Set, List
import heapq


class ZoneType(Enum):
    """Zone Type Enum"""
    NORMAL = 1
    RESTRICTED = 2
    PRIORITY = 0.9
    BLOCKED = float('inf')


class ReverseDijkstra():
    """Class that calculates each zones distance to the end."""
    def __init__(self, input_data: dict[str, Any]):
        """Initializes the class."""
        self.input_data = input_data
        self.start = [key for key in input_data
                      if input_data[key]["is_start"]][0]
        self.end = [key for key in input_data
                    if input_data[key]["is_end"]][0]
        self.dist_to_end: dict[str,
                               float | int] = {key: float(inf)
                                               if not input_data[key]["is_end"]
                                               else 0
                                               for key in input_data}
        self.previous: dict[str, Optional[str]] = {key: None
                                                   for key in input_data}
        self.visited: Set[str] = set()
        self.pq: List[tuple[float | int, str]] = []
        heapq.heappush(self.pq, (0, self.end))

    def process(self) -> dict[str, float | int]:
        """Processes zone distances from the end."""
        while (len(self.pq) != 0):
            old_cost, cur_node = heapq.heappop(self.pq)
            if cur_node in self.visited:
                continue
            self.visited.add(cur_node)
            zone_type = ZoneType[self.input_data[cur_node]["zone"].upper()]
            for neighbor in self.input_data[cur_node]["connections"]:
                nei_type = ZoneType[self.input_data[neighbor]["zone"].upper()]
                if (nei_type == ZoneType.BLOCKED or neighbor in self.visited):
                    continue
                cost = zone_type.value + old_cost
                if cost < self.dist_to_end[neighbor]:
                    self.dist_to_end[neighbor] = cost
                    self.previous[neighbor] = cur_node
                    heapq.heappush(self.pq,
                                   (self.dist_to_end[neighbor], neighbor))
        return self.dist_to_end
