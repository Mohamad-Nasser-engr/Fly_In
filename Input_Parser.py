from typing import List, Optional
import re
from PIL import ImageColor
from typing import Any


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
        self._zones_data: dict[str, Any] = {}
        self._connections: List[List[str]] = []

    def nb_drone_parsing(self, line: str) -> bool:
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
            return True
        except Exception:
            print("Invalid line: ", line)
            print("Drone numbers must be valid positive integer")
            return False

    def handle_zone_types(self, content: List[str]) -> List[bool]:
        """Validates zone type argument"""
        hub = content[0].strip()
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

    def handle_zone_names(self, hub_data: List[str]) -> str:
        """Validates zone names."""
        zone_name = hub_data[0]
        if "-" in zone_name or " " in zone_name:
            raise Exception("Zone names cannot contain dashes (-) or spaces")
        if zone_name in self._zone_names:
            raise Exception(f"Duplicate zone name: {zone_name}")
        self._zone_names.append(zone_name)
        self._zones_data[zone_name] = {}
        return zone_name

    def handle_zone_coord(self, hub_data: List[str], zone_name: str) -> None:
        """Validates zone coordinates"""
        if not hub_data[1].strip().lstrip('-').isdigit():
            raise Exception("Invalid x coordinate")
        else:
            x_cord = int(hub_data[1].strip())
        if not hub_data[2].strip().lstrip('-').isdigit():
            raise Exception("Invalid y coordinate")
        else:
            y_cord = int(hub_data[2].strip())
        if (x_cord, y_cord) in self._coordinate_list:
            raise Exception("Duplicate coordinates")
        else:
            self._coordinate_list.append((x_cord, y_cord))
            self._zones_data[zone_name]["coordinates"] = (x_cord, y_cord)

    def handle_zone_metadata(self, hub_data: List[str],
                             zone_name: str) -> None:
        """Validates zone metadata"""
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
            self._zones_data[zone_name]["color"] = None
            self._zones_data[zone_name]["zone"] = "normal"
            self._zones_data[zone_name]["max_drones"] = 1
            self._zones_data[zone_name]["connections"] = {}
            ###
            if stats[0]:
                self._zones_data[zone_name]["drone_in_zone"] = self._nb_drones
            else:
                self._zones_data[zone_name]["drone_in_zone"] = 0
            ###
            if len(hub_data) == 4:
                self.handle_zone_metadata(hub_data, zone_name)
            if stats[1]:
                self._zones_data[zone_name]["max_drones"] = self._nb_drones
            return True
        except Exception as e:
            print("Invalid line: ", line)
            print(e)
            return False

    def handle_connection_metadata(self, con_data: List[str],
                                   data: List[str]) -> None:
        """Validates connection metadata."""
        meta = con_data[1]
        if (meta.startswith("[") and meta.endswith("]")
                and meta.count("[") == 1 and meta.count("]") == 1):
            meta_list = meta.strip("[]").split()
        else:
            raise Exception("Invalid format for metadata")
        if len(meta_list) > 1:
            raise Exception("Invalid connection metadata")
        d_l = meta_list[0].strip().split("=")
        if len(d_l) != 2:
            raise Exception("Invalid connection metadata")
        if d_l[0] != "max_link_capacity":
            raise Exception("Invalid connection metadata")
        if not d_l[1].strip().isdigit():
            raise Exception("Invalid metadata value")
        self._zones_data[data[0]]["connections"][data[1]] = int(d_l[1])
        self._zones_data[data[1]]["connections"][data[0]] = int(d_l[1])

    def connection_handling(self, line: str) -> bool:
        """Parses connection lines."""
        try:
            content = line.split(":")
            if len(content) != 2:
                raise Exception("Invalid Syntax")
            if content[0].strip() != "connection":
                raise Exception("Invalid argument chosen")
            con_data = re.split(r'\s+(?![^\[]*\])', content[1].strip())
            if len(con_data) != 1 and len(con_data) != 2:
                raise Exception("Format: zone1-zone2 [metadata]")
            data = sorted(con_data[0].strip().split("-"))
            if len(data) != 2:
                raise Exception("Invalid Connection: zone1-zone2")
            if (data[0] not in self._zones_data
                    or data[1] not in self._zones_data):
                raise Exception("Zones must be specified before connection")
            if data[0] == data[1]:
                raise Exception("Cannot make connection on the same zone")
            if data in self._connections:
                raise Exception("Duplicate connection")
            self._zones_data[data[0]]["connections"][data[1]] = 1
            self._zones_data[data[1]]["connections"][data[0]] = 1
            if len(con_data) == 2:
                self.handle_connection_metadata(con_data, data)
            self._connections.append(data)
        except Exception as e:
            print("Invalid line: ", line)
            print(e)
            return False
        return True

    def parse_input(self, input_file: str) -> bool:
        """Parses input file."""
        try:
            with open(input_file, "r") as f:
                is_first_line = True
                for line in f:
                    if not self._is_valid:
                        break
                    line = line.strip()
                    if line == "" or line.startswith("#"):
                        continue
                    if is_first_line:
                        is_first_line = False
                        self._is_valid = self.nb_drone_parsing(line)
                    elif line.startswith("connection"):
                        self._is_valid = self.connection_handling(line)
                    else:
                        self._is_valid = self.zone_handling(line)
                if ((not self._start_hub or not self._end_hub)
                        and self._is_valid):
                    self._is_valid = False
                    print("Start or End hub not specified in input file")
                return self._is_valid
        except Exception:
            print("Invalid input file")
            return False

    def get_drone_numbers(self) -> int:
        """Get drone numbers after parsing"""
        return self._nb_drones

    def get_input_data(self) -> dict[str, Any]:
        """Return parsed data"""
        return self._zones_data
