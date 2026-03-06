from typing import List, Optional
import re

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
        if (hub == "start_hub"):
            if self._start_hub:
                raise Exception("Multiple start hub definition")
            else:
                self._start_hub = content[0]
        elif (hub == "end_hub"):
            if self._end_hub:
                raise Exception("Multiple end hub definition")
            else:
                self._end_hub = content[0]
        elif (hub != "hub"):
            raise Exception("Invalid argument chosen")

    def zone_handling(self, line: str) -> bool:
        """Parses hub data"""
        try:
            content = line.split(":")
            if len(content) != 2:
                raise Exception("Invalid Syntax")
            self.handle_zone_types(content)
            hub_data = re.split(r'\s+(?![^\[]*\])', content[1].strip())
            print(hub_data)
            if len(hub_data) != 3 and len(hub_data) != 4:
                raise Exception("Invalid format: <hub_type>: zone_name x y [optional metadata]")
            zone_name = hub_data[0]
            if "-" in zone_name or " " in zone_name:
                raise Exception("Zone names cannot contain dashes (-) or spaces")
            if zone_name in self._zone_names:
                raise Exception(f"Duplicate zone name: {zone_name}")
            self._zone_names.append(zone_name)
            self._zones_data[zone_name] = {}
            # coord
            if not hub_data[1].strip().isdigit():
                raise Exception("Invalid x corrdinate")
            else:
                x_cord = int(hub_data[1].strip())
            if not hub_data[2].strip().isdigit():
                raise Exception("Invalid y corrdinate")
            else:
                y_cord = int(hub_data[2].strip())
            if (x_cord, y_cord) in self._coordinate_list:
                raise Exception("Duplicate coordinates")
            else:
                self._coordinate_list.append((x_cord, y_cord))
                self._zones_data[zone_name]["coordinates"] = (x_cord, y_cord)
            # Optional metadata
            self._zones_data[zone_name]["color"] = None
            self._zones_data[zone_name]["zone"] = "normal"
            self._zones_data[zone_name]["max_drones"] = 1
            if len(hub_data) == 4:
                meta = hub_data[3]
                if (meta.startswith("[") and meta.endswith("]")
                        and meta.count("[") == 1 and meta.count("]") == 1):
                    meta_list = meta.strip("[]").split()
                else:
                    raise Exception("Invalid format for metadata")
                if len(meta_list) != len(set(meta_list)):
                    #NOT ENOUGH FOR DUPLICATE
                    raise Exception("Duplicate Metadata")
                for data in meta_list:
                    d_l = data.strip().split("=")
                    if len(d_l) != 2:
                        raise Exception("Invalid Metadata")
                    meta_name = d_l[0]
                    if meta_name == "color":
                        # check if valid color
                        ### !!!!!!!!!!!!!!!!!!!!
                        self._zones_data[zone_name]["color"] = d_l[1]
                    elif meta_name == "zone":
                        if d_l[1].strip() in ("normal", "blocked", "restricted", "priority"):
                            self._zones_data[zone_name]["zone"] = d_l[1]
                        else:
                            #zone= normal is giving this error
                            raise Exception("Invalid zone specified in metadata")
                    elif meta_name == "max_drones":
                        if not d_l[1].strip().isdigit():
                            raise Exception ("Invalid metadata value")
                        self._zones_data[zone_name]["max_drones"] = int(d_l[1])
                    else:
                        raise Exception("Invalid metadata")
            return True
        except Exception as e:
            print("Invalid line: ", line)
            print(e)
            return False


    def connection_handling(self, line: str) -> bool:
        pass

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
            ## AT END OF LOOP CHECK THAT START_HUB AND END_HUB WERE SET

    def is_valid(self) -> bool:
        return self._is_valid
