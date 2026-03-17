import arcade
from typing import Any


class Window(arcade.Window):
    def __init__(self, width: int, height: int,
                 title: str, map: dict[str, Any]) -> None:
        super().__init__(width, height, title, resizable=True)
        self.set_location(400, 200)
        self.x = 50
        self.map = map
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self) -> None:
        SCALE = 150
        OFFSET_X = 200
        OFFSET_Y = 300
        self.clear()
        for name, value in self.map.items():
            x1, y1 = value["coordinates"]
            x1 = x1 * SCALE + OFFSET_X
            y1 = y1 * SCALE + OFFSET_Y
            for neighbor in value["connections"]:
                x2, y2 = self.map[neighbor]["coordinates"]
                x2 = x2 * SCALE + OFFSET_X
                y2 = y2 * SCALE + OFFSET_Y
                arcade.draw_line(x1, y1, x2, y2, arcade.color.GRAY, 4)
        for name, value in self.map.items():
            x, y = value["coordinates"]
            x = x * SCALE + OFFSET_X
            y = y * SCALE + OFFSET_Y
            try:
                color = arcade.color.__dict__[value["color"].upper()]

            except Exception:
                color = arcade.color.GRAY
            arcade.draw_circle_filled(x, y, 20, color)
            arcade.draw_text(name, x - 20, y + 25, arcade.color.WHITE, 10)
