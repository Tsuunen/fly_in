from map_parser import MapParser, ParsingError

if (__name__ == "__main__"):
    parser = MapParser("maps/easy/01_linear_path.txt")
    try:
        print(parser.extract())
    except ParsingError as e:
        print(e)
