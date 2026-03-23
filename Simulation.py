from typing import Any, Optional, TypedDict


class DroneState(TypedDict):
    id: int
    location: str
    dist_to_end: float | int
    in_transit: bool
    trans_location: Optional[str]


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
        # Ad is_in_transit key
        self.locations: list[DroneState] = [{"id": i,
                                             "location": self.start,
                                             "dist_to_end":
                                             dist_to_end[self.start],
                                             "in_transit": False,
                                             "trans_location": None}
                                            for i
                                            in range(1, self.drone_num + 1)]
        # print(self.locations)

    def simulate_turn(self) -> str:
        """Simulate one turn."""
        # One turn
        ans = ""
        for drone in self.locations:
            # check neighbor with least dist to end to go to
            # Make sure it has space
            # make sure if it is priority or restricted to handle
            # add a in_connection flag?
            # Current location Data
            drone_id = drone["id"]
            drone_location: str = drone["location"]
            drone_dist = drone["dist_to_end"]
            if drone_location == self.end:
                continue

            # ## CHECK IF DRONE IN TRANSIT???(HERE ?)

            # drone_neighbors: list[dict[str, Any]]
            drone_neighbors = [{"location": key,
                                "dist_to_end": self.dist_to_end[key],
                                "zone_type": self.input_data[key]["zone"]}
                               for key in self.input_data[drone_location]
                               ["connections"].keys()]
            drone_neighbors.sort(key=lambda n:
                                 (0 if n['zone_type'] == 'priority'
                                  else 1, n['dist_to_end']))
            # print("SORTED NEIGHBORS")
            # print(drone_neighbors)
            for neighbor in drone_neighbors:
                # Neighbor data
                nei_location = neighbor["location"]
                nei_dist = neighbor["dist_to_end"]
                nei_type = neighbor["zone_type"]
                nei_capacity = self.input_data[nei_location]["max_drones"]
                nei_load = self.input_data[nei_location]["drone_in_zone"]
                # Invalid neighbor conditions
                # (dist > current dist, blocked nei, max capacity)
                if (nei_type == "blocked" or nei_dist >= drone_dist):
                    continue
                elif nei_type == "restricted":
                    # ## Check if link is full
                    # ## edit is transit and trans location

                    break
                elif nei_load == nei_capacity:
                    continue
                else:
                    ####
                    # STILL NEED TO HANDLE CONNECTIONS AND RESTRICTED ZONES
                    ####
                    # change location / dist of drone and current drone
                    drone["location"] = nei_location
                    drone["dist_to_end"] = nei_dist
                    # change load of neighbor
                    self.input_data[nei_location]["drone_in_zone"] += 1
                    self.input_data[drone_location]["drone_in_zone"] -= 1
                    ans += f"D{drone_id}-{nei_location} "
                    break
        return ans

    def is_completed(self) -> bool:
        """Check if all drones reached the end."""
        for drone in self.locations:
            if drone["location"] != self.end:
                return False
        return True

    def simulate_run(self) -> None:
        """Simulates the whole run."""
        while (not self.is_completed()):
            print(self.simulate_turn())
            self.locations.sort(key=lambda drone: drone['dist_to_end'])
