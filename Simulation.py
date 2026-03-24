from typing import Any, Optional, TypedDict
import copy


class DroneState(TypedDict):
    id: int
    location: str
    dist_to_end: float | int
    in_transit: bool
    trans_location: Optional[str]
    old_location: Optional[str]


class Simulation():
    """Simulation class."""
    def __init__(self, drone_num: int, input_data: dict[str, Any],
                 dist_to_end: dict[str, float | int]) -> None:
        """Initializes simulator."""
        self.drone_num = drone_num
        self.input_data = input_data
        self.dist_to_end = dist_to_end
        self.start = [key for key in input_data
                      if input_data[key]["is_start"]][0]
        self.end = [key for key in input_data
                    if input_data[key]["is_end"]][0]
        self.locations: list[DroneState] = [{"id": i,
                                             "location": self.start,
                                             "dist_to_end":
                                             dist_to_end[self.start],
                                             "in_transit": False,
                                             "trans_location": None,
                                             "old_location": None}
                                            for i
                                            in range(1, self.drone_num + 1)]

    def simulate_turn(self) -> str:
        """Simulate one turn."""
        ans = ""
        for drone in self.locations:
            drone_id = drone["id"]
            if drone["in_transit"]:
                next_loc = drone["trans_location"]
                old_loc = drone["old_location"]
                if old_loc is None or next_loc is None:
                    return "INVALID TRANSIT"
                drone["in_transit"] = False
                drone["location"] = next_loc
                drone["trans_location"] = None
                drone["dist_to_end"] = self.dist_to_end[next_loc]
                self.input_data[next_loc]["drone_in_zone"] += 1
                link2 = self.input_data[old_loc]["connections"][next_loc]
                link2["drone_in_link"] -= 1
                ans += f"D{drone_id}-{next_loc} "
                continue
            drone_loc: str = drone["location"]
            drone_dist = drone["dist_to_end"]
            if drone_loc == self.end:
                continue

            drone_neighbors = [{"location": key,
                                "dist_to_end": self.dist_to_end[key],
                                "zone_type": self.input_data[key]["zone"]}
                               for key in self.input_data[drone_loc]
                               ["connections"].keys()]
            drone_neighbors.sort(key=lambda n:
                                 (0 if n['zone_type'] == 'priority'
                                  else 1, n['dist_to_end']))

            for neighbor in drone_neighbors:
                nei_loc = neighbor["location"]
                nei_dist = neighbor["dist_to_end"]
                nei_type = neighbor["zone_type"]
                nei_capacity = self.input_data[nei_loc]["max_drones"]
                nei_load = self.input_data[nei_loc]["drone_in_zone"]
                if (nei_type == "blocked" or nei_dist >= drone_dist):
                    continue
                elif nei_type == "restricted":
                    link = self.input_data[drone_loc]["connections"][nei_loc]
                    link_load = link["drone_in_link"]
                    link_capacity = link["max_link"]
                    if link_capacity == link_load:
                        continue
                    # this statement should be edited
                    # to see if after 2 turns its available?
                    if nei_load == nei_capacity:
                        continue
                    drone["old_location"] = drone_loc
                    drone["trans_location"] = nei_loc
                    drone["in_transit"] = True
                    self.input_data[drone_loc]["drone_in_zone"] -= 1
                    link3 = self.input_data[drone_loc]["connections"][nei_loc]
                    link3["drone_in_link"] += 1
                    ans += f"D{drone_id}-{drone_loc}-{nei_loc} "
                    break
                elif nei_load == nei_capacity:
                    continue
                else:
                    drone["location"] = nei_loc
                    drone["old_location"] = drone_loc
                    drone["dist_to_end"] = nei_dist
                    self.input_data[nei_loc]["drone_in_zone"] += 1
                    self.input_data[drone_loc]["drone_in_zone"] -= 1
                    ans += f"D{drone_id}-{nei_loc} "
                    break
        return ans

    def is_completed(self) -> bool:
        """Check if all drones reached the end."""
        for drone in self.locations:
            if drone["location"] != self.end:
                return False
        return True

    def simulate_run(self) -> dict[int, list[DroneState]]:
        """Simulates the whole run."""
        i = 0
        turns_data = {0: copy.deepcopy(self.locations)}
        while (not self.is_completed()):
            print(self.simulate_turn())
            i += 1
            self.locations.sort(key=lambda drone:
                                (drone['dist_to_end'],
                                 0 if drone['in_transit'] else 1))
            turns_data[i] = copy.deepcopy(self.locations)
        # print(i)
        return turns_data
