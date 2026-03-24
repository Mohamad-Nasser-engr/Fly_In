from Input_Parser import Input_Parser
import arcade
import copy
from Display import Window
from ReverseDijkstra import ReverseDijkstra
from Simulation import Simulation


def main() -> None:
    """Main script."""
    inp_parser = Input_Parser()
    if inp_parser.parse_input("Test.txt"):
        input_data = inp_parser.get_input_data()
        if not input_data:
            return
        algo = ReverseDijkstra(input_data)
        dists = algo.process()
        sim = Simulation(inp_parser.get_drone_numbers(),
                         copy.deepcopy(input_data), dists)
        turn_data = sim.simulate_run()
        Window(1280, 720, "Drone System", input_data, turn_data)
        arcade.run()


if __name__ == "__main__":
    main()
