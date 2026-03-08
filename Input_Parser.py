from typing import List, Optional
import re
from PIL import ImageColor


class Input_Parser():
    """Input parsing class."""
    def __init__(self) -> None:
        """Initializes parser."""
        self._is_valid: bool = True
        self._nb_drones: int = -1
        self._start_hub: Optional[str] = None
        self._end_hub: Optional[str] = None
        self._zone_names: List[str] = []
        self._coordinate_list: List[tuple[int, int]] = []
        self._zones_data: dict = {}

    def get_drone_numbers(self, line: str) -> bool:
        """Get drone numbers"""
        try:
            content = line.split(":")
            if len(content) != 2 or content[0] != "nb_drones":
                print("Invalid line: ", line)
                print("Expected format: nb_drones: <positive integer>")
                return False
            if not content[1].strip().isdigit():
                if (content[1].strip().startswith("+")
                        and not content[1].strip()[1:].isdigit()):
                    raise Exception()
                elif not content[1].strip().startswith("+"):
                    raise Exception()
            self._nb_drones = int(content[1])
            print(self._nb_drones)
            return True
        except Exception:
            print("Invalid line: ", line)
            print("Drone numbers must be valid positive integer")
            return False

    def handle_zone_types(self, content: List[str]):
        """Validates zone type argument"""
        hub = content[0]
        is_start = False
        is_end = False
        if (hub == "start_hub"):
            if self._start_hub:
                raise Exception("Multiple start hub definition")
            else:
                is_start = True
                self._start_hub = content[0]
        elif (hub == "end_hub"):
            if self._end_hub:
                raise Exception("Multiple end hub definition")
            else:
                is_end = True
                self._end_hub = content[0]
        elif (hub != "hub"):
            raise Exception("Invalid argument chosen")
        return [is_start, is_end]

    def handle_zone_names(self, hub_data) -> str:
        zone_name = hub_data[0]
        if "-" in zone_name or " " in zone_name:
            raise Exception("Zone names cannot contain dashes (-) or spaces")
        if zone_name in self._zone_names:
            raise Exception(f"Duplicate zone name: {zone_name}")
        self._zone_names.append(zone_name)
        self._zones_data[zone_name] = {}
        return zone_name

    def handle_zone_coord(self, hub_data, zone_name):
        if not hub_data[1].strip().isdigit():
            raise Exception("Invalid x coordinate")
        else:
            x_cord = int(hub_data[1].strip())
        if not hub_data[2].strip().isdigit():
            raise Exception("Invalid y coordinate")
        else:
            y_cord = int(hub_data[2].strip())
        if (x_cord, y_cord) in self._coordinate_list:
            raise Exception("Duplicate coordinates")
        else:
            self._coordinate_list.append((x_cord, y_cord))
            self._zones_data[zone_name]["coordinates"] = (x_cord, y_cord)

    def handle_zone_metadata(self, hub_data, zone_name):
        meta = hub_data[3]
        if (meta.startswith("[") and meta.endswith("]")
                and meta.count("[") == 1 and meta.count("]") == 1):
            meta_list = meta.strip("[]").split()
        else:
            raise Exception("Invalid format for metadata")
        data_list = []
        for data in meta_list:
            d_l = data.strip().split("=")
            if len(d_l) != 2:
                raise Exception("Invalid Metadata")
            meta_name = d_l[0]
            if meta_name in data_list:
                raise Exception("Duplicate metadata")
            else:
                data_list.append(meta_name)
            if meta_name == "color":
                try:
                    ImageColor.getcolor(d_l[1], "RGB")
                except Exception:
                    raise Exception("Invalid color chosen")
                self._zones_data[zone_name]["color"] = d_l[1]
            elif meta_name == "zone":
                if d_l[1].strip() in ("normal", "blocked",
                                      "restricted", "priority"):
                    if d_l[1].strip() == "blocked":
                        is_start = self._zones_data[zone_name]["is_start"]
                        is_end = self._zones_data[zone_name]["is_end"]
                        if is_start or is_end:
                            raise Exception("Start/end zones can't be blocked")
                    self._zones_data[zone_name]["zone"] = d_l[1]
                else:
                    raise Exception("Invalid zone specified in metadata")
            elif meta_name == "max_drones":
                if not d_l[1].strip().isdigit():
                    raise Exception("Invalid metadata value")
                self._zones_data[zone_name]["max_drones"] = int(d_l[1])
            else:
                raise Exception("Invalid metadata")

    def zone_handling(self, line: str) -> bool:
        """Parses hub data"""
        try:
            content = line.split(":")
            if len(content) != 2:
                raise Exception("Invalid Syntax")
            stats = self.handle_zone_types(content)
            hub_data = re.split(r'\s+(?![^\[]*\])', content[1].strip())
            if len(hub_data) != 3 and len(hub_data) != 4:
                raise Exception("Zone format: <type>: name x y [metadata]")
            zone_name = self.handle_zone_names(hub_data)
            self._zones_data[zone_name]["is_start"] = stats[0]
            self._zones_data[zone_name]["is_end"] = stats[1]
            self.handle_zone_coord(hub_data, zone_name)
            # Optional metadata
            self._zones_data[zone_name]["color"] = None
            self._zones_data[zone_name]["zone"] = "normal"
            self._zones_data[zone_name]["max_drones"] = 1
            if len(hub_data) == 4:
                self.handle_zone_metadata(hub_data, zone_name)
            return True
        except Exception as e:
            print("Invalid line: ", line)
            print(e)
            return False

    def connection_handling(self, line: str) -> bool:
        return True

    def parse_input(self, input_file: str) -> bool:
        """Parses input file."""
        with open(input_file, "r") as f:
            is_first_line = True
            for line in f:
                if not self._is_valid:
                    break
                line = line.strip()
                # Skips empty and commented lines
                if line == "" or line.startswith("#"):
                    continue
                # get drone numbers
                if is_first_line:
                    is_first_line = False
                    self._is_valid = self.get_drone_numbers(line)
                # Other cases
                elif line.startswith("connection"):
                    self._is_valid = self.connection_handling(line)
                else:
                    self._is_valid = self.zone_handling(line)
            if (not self._start_hub or not self._end_hub) and self._is_valid:
                self._is_valid = False
                print("Start or End hub not specified in input file")
            print(self._zones_data)

    def is_valid(self) -> bool:
        return self._is_valid
