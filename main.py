from Input_Parser import Input_Parser


def main():
    """Main script."""
    inp_parser = Input_Parser()
    inp_parser.parse_input("01_linear_path.txt")
    print(inp_parser.get_drone_numbers())
    print(inp_parser.get_input_data())


if __name__ == "__main__":
    main()
