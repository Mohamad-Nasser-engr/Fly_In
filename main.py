from Input_Parser import Input_Parser
import arcade
from Display import Window


def main() -> None:
    """Main script."""
    inp_parser = Input_Parser()
    if inp_parser.parse_input("01_linear_path.txt"):
        print(inp_parser.get_drone_numbers())
        input_data = inp_parser.get_input_data()
        if not input_data:
            return
        print(input_data)
        Window(1280, 720, "Drone System", input_data)
        arcade.run()


if __name__ == "__main__":
    main()
