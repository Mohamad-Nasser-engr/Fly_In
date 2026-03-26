import arcade
from typing import Any
from Simulation import DroneState


class Window(arcade.Window):
    """Display window with smooth drone animation."""

    def __init__(self, width: int, height: int,
                 title: str, map: dict[str, Any],
                 turn_data: dict[int, list[DroneState]]) -> None:
        """Initializes display."""
        super().__init__(width, height, title, resizable=True)
        self.map = map
        self.turn_data = turn_data

        self.current_turn = 0
        self.timer: int | float = 0
        self.turn_duration = 0.7
        self.max_turn = max(self.turn_data.keys())

        arcade.set_background_color(arcade.color.CHARCOAL)

    def on_update(self, delta_time: float) -> None:
        """Advance animation timer and turns, stop at last turn."""
        self.timer += delta_time
        if self.timer >= self.turn_duration:
            if self.current_turn < self.max_turn:
                self.timer = 0
                self.current_turn += 1
            else:
                self.timer = self.turn_duration

    def compute_offsets(self, scale_x: float = 85,
                        scale_y: float = 100) -> tuple[float, float]:
        """Compute offsets to center the graph on the screen."""
        xs = [coord[0] for node in self.map.values()
              for coord in [node["coordinates"]]]
        ys = [coord[1] for node in self.map.values()
              for coord in [node["coordinates"]]]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        graph_width = (max_x - min_x) * scale_x
        graph_height = (max_y - min_y) * scale_y

        offset_x = (self.width - graph_width) / 2 - min_x * scale_x
        offset_y = (self.height - graph_height) / 2 - min_y * scale_y

        return offset_x, offset_y

    def on_draw(self) -> None:
        """Draws the graph, nodes, and moving drones."""
        SCALE_X = 85
        SCALE_Y = 100

        self.clear()
        t = self.timer / self.turn_duration

        OFFSET_X, OFFSET_Y = self.compute_offsets(SCALE_X, SCALE_Y)

        current_turn_data = self.turn_data[self.current_turn]
        previous_turn_data = self.turn_data.get(self.current_turn - 1,
                                                current_turn_data)

        # Draw Connections
        for name, value in self.map.items():
            x1, y1 = value["coordinates"]
            x1 = x1 * SCALE_X + OFFSET_X
            y1 = y1 * SCALE_Y + OFFSET_Y
            for neighbor in value["connections"]:
                x2, y2 = self.map[neighbor]["coordinates"]
                x2 = x2 * SCALE_X + OFFSET_X
                y2 = y2 * SCALE_Y + OFFSET_Y
                arcade.draw_line(x1, y1, x2, y2, arcade.color.GRAY, 4)

        # Draw Zones
        for name, value in self.map.items():
            x, y = value["coordinates"]
            x = x * SCALE_X + OFFSET_X
            y = y * SCALE_Y + OFFSET_Y
            try:
                if value["color"].upper() == "RAINBOW":
                    import colorsys
                    num_slices = 100
                    for i in range(num_slices):
                        hue = i / num_slices
                        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
                        colors = (int(r*255), int(g*255), int(b*255))

                        start_angle = i * 360 / num_slices
                        end_angle = (i+1) * 360 / num_slices
                        arcade.draw_arc_filled(x, y, 20 * 2, 20 * 2, colors,
                                               start_angle, end_angle)
                elif value["color"].upper() == "DARKRED":
                    color = arcade.color.DARK_RED
                else:
                    color = arcade.color.__dict__[value["color"].upper()]
            except Exception:
                color = arcade.color.GRAY
            if value["color"].upper() != "RAINBOW":
                arcade.draw_circle_filled(x, y, 20, color)

            # Count drones at this zone for current turn
            count = 0
            for drone in current_turn_data:
                if drone["in_transit"]:
                    if drone["trans_location"] == name:
                        count += 1
                else:
                    if drone["location"] == name:
                        count += 1
            arcade.draw_text(str(count), x, y,
                             arcade.color.WHITE, 12,
                             anchor_x="center", anchor_y="center")

            arcade.draw_text(name, x - 20, y + 25, arcade.color.WHITE, 7.25)

        # Draw moving drones smoothly
        for i in range(len(current_turn_data)):
            drone_now = current_turn_data[i]
            drone_prev = previous_turn_data[i]

            if drone_now["in_transit"]:
                start_loc = drone_now["old_location"]
                end_loc = drone_now["trans_location"]
                if not end_loc or not start_loc:
                    continue
                x1, y1 = self.map[start_loc]["coordinates"]
                x2, y2 = self.map[end_loc]["coordinates"]
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                x1 = x1 * SCALE_X + OFFSET_X
                y1 = y1 * SCALE_Y + OFFSET_Y
                end_x = mid_x * SCALE_X + OFFSET_X
                end_y = mid_y * SCALE_Y + OFFSET_Y
                x = x1 + (end_x - x1) * t
                y = y1 + (end_y - y1) * t

            elif drone_prev["in_transit"]:
                old_loc = drone_prev["old_location"]
                transit_loc = drone_prev["trans_location"]
                end_loc = drone_now["location"]
                if old_loc and transit_loc:
                    x1, y1 = self.map[old_loc]["coordinates"]
                    x2, y2 = self.map[transit_loc]["coordinates"]
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    start_x = mid_x * SCALE_X + OFFSET_X
                    start_y = mid_y * SCALE_Y + OFFSET_Y
                    end_x, end_y = self.map[end_loc]["coordinates"]
                    end_x = end_x * SCALE_X + OFFSET_X
                    end_y = end_y * SCALE_Y + OFFSET_Y
                    x = start_x + (end_x - start_x) * t
                    y = start_y + (end_y - start_y) * t

            else:
                start_loc = drone_prev["location"]
                end_loc = drone_now["location"]
                x1, y1 = self.map[start_loc]["coordinates"]
                x2, y2 = self.map[end_loc]["coordinates"]
                x1 = x1 * SCALE_X + OFFSET_X
                y1 = y1 * SCALE_Y + OFFSET_Y
                x2 = x2 * SCALE_X + OFFSET_X
                y2 = y2 * SCALE_Y + OFFSET_Y
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t

            if (self.current_turn == self.max_turn
                    and self.timer >= self.turn_duration):
                continue

            arcade.draw_circle_filled(x, y, 8, arcade.color.YELLOW)
            arcade.draw_text(str(drone_now["id"]), x, y,
                             arcade.color.BLACK, 7,
                             anchor_x="center", anchor_y="center")
