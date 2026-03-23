from Input_Parser import Input_Parser
import arcade
from Display import Window
from ReverseDijkstra import ReverseDijkstra
from Simulation import Simulation


def main() -> None:
    """Main script."""
    inp_parser = Input_Parser()
    if inp_parser.parse_input("Test.txt"):
        # print(inp_parser.get_drone_numbers())
        input_data = inp_parser.get_input_data()
        if not input_data:
            return
        print(input_data)
        algo = ReverseDijkstra(input_data)
        # print("OUTPUT:")
        dists = algo.process()
        # print(dists)
        # print("PROCESSED PATH: ")
        # print("DISTANCES: ")
        # print(algo.dist_to_end)
        # print("PREVIOUS: ")
        # print(algo.previous)
        sim = Simulation(inp_parser.get_drone_numbers(), input_data, dists)
        sim.simulate_run()
        Window(1280, 720, "Drone System", input_data)
        arcade.run()


if __name__ == "__main__":
    main()
