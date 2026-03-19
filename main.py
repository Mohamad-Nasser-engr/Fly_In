from Input_Parser import Input_Parser
import arcade
from Display import Window
from Dijkstra import Dijkstra


def main() -> None:
    """Main script."""
    inp_parser = Input_Parser()
    if inp_parser.parse_input("Test.txt"):
        print(inp_parser.get_drone_numbers())
        input_data = inp_parser.get_input_data()
        if not input_data:
            return
        print(input_data)
        algo = Dijkstra(input_data)
        algo.process()
        print("PROCESSED PATH: ")
        print("DISTANCES: ")
        print(algo.distances)
        print("PREVIOUS: ")
        print(algo.previous)
        Window(1280, 720, "Drone System", input_data)
        arcade.run()


if __name__ == "__main__":
    main()
