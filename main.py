def main() -> None:
    """Main script."""
    try:
        from Input_Parser import Input_Parser
        import arcade
        import sys
        import copy
        from Display import Window
        from ReverseDijkstra import ReverseDijkstra
        from Simulation import Simulation
        if len(sys.argv) != 2:
            raise Exception("No file Specified")
        file = sys.argv[1]
        inp_parser = Input_Parser()
        if inp_parser.parse_input(file):
            input_data = inp_parser.get_input_data()
            if not input_data:
                return
            algo = ReverseDijkstra(input_data)
            dists = algo.process()
            sim = Simulation(inp_parser.get_drone_numbers(),
                             copy.deepcopy(input_data), dists)
            turn_data = sim.simulate_run()
            if turn_data is None:
                print("Graph is unsolvable")
                return
            Window(1280, 720, "Drone System", input_data, turn_data)
            arcade.run()
    except (Exception, KeyboardInterrupt) as e:
        print(e)


if __name__ == "__main__":
    main()
