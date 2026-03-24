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
        self.set_location(400, 200)
        self.x = 50
        self.map = map
        self.turn_data = turn_data

        # Animation tracking
        self.current_turn = 0
        self.timer: int | float = 0
        self.turn_duration = 0.7  # seconds per turn
        self.max_turn = max(self.turn_data.keys())

        arcade.set_background_color(arcade.color.CHARCOAL)

    def on_update(self, delta_time: float) -> None:
        """Advance animation timer and turns, stop at last turn."""
        if self.current_turn >= self.max_turn:
            # Stop updating after last turn
            self.timer = self.turn_duration  # clamp to 1
            return

        self.timer += delta_time
        if self.timer >= self.turn_duration:
            self.timer = 0
            self.current_turn += 1
            if self.current_turn > self.max_turn:
                self.current_turn = self.max_turn

    def on_draw(self) -> None:
        """Draws the graph, nodes, and moving drones."""
        SCALE_X = 85
        SCALE_Y = 100
        OFFSET_X = 50
        OFFSET_Y = 360

        self.clear()
        t = self.timer / self.turn_duration  # interpolation factor

        # Get current and previous turns
        current_turn_data = self.turn_data[self.current_turn]
        previous_turn_data = self.turn_data.get(self.current_turn - 1,
                                                current_turn_data)

        # Draw graph lines
        for name, value in self.map.items():
            x1, y1 = value["coordinates"]
            x1 = x1 * SCALE_X + OFFSET_X
            y1 = y1 * SCALE_Y + OFFSET_Y
            for neighbor in value["connections"]:
                x2, y2 = self.map[neighbor]["coordinates"]
                x2 = x2 * SCALE_X + OFFSET_X
                y2 = y2 * SCALE_Y + OFFSET_Y
                arcade.draw_line(x1, y1, x2, y2, arcade.color.GRAY, 4)

        # Draw nodes and counts
        for name, value in self.map.items():
            x, y = value["coordinates"]
            x = x * SCALE_X + OFFSET_X
            y = y * SCALE_Y + OFFSET_Y
            try:
                color = arcade.color.__dict__[value["color"].upper()]
            except Exception:
                color = arcade.color.GRAY
            arcade.draw_circle_filled(x, y, 20, color)

            # Count drones at this node for current turn
            count = 0
            for drone in current_turn_data:
                if drone["in_transit"]:
                    # Simple version: count in trans_location
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

            # Determine start and end positions for interpolation
            if drone_now["in_transit"]:
                start_loc = drone_now["old_location"] or drone_prev["location"]
                end_loc = drone_now["trans_location"] or drone_now["location"]
            else:
                start_loc = drone_prev["location"]
                end_loc = drone_now["location"]

            # Convert to coordinates
            x1, y1 = self.map[start_loc]["coordinates"]
            x2, y2 = self.map[end_loc]["coordinates"]
            x1 = x1 * SCALE_X + OFFSET_X
            y1 = y1 * SCALE_Y + OFFSET_Y
            x2 = x2 * SCALE_X + OFFSET_X
            y2 = y2 * SCALE_Y + OFFSET_Y

            # Interpolate
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t

            # Draw drone
            arcade.draw_circle_filled(x, y, 8, arcade.color.YELLOW)
