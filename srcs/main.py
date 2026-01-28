from map_parser import MapParser, ParsingError
from map_display import MapDisplay
from drone import Drone

if (__name__ == "__main__"):
    parser = MapParser("maps/easy/02_simple_fork.txt")
    try:
        map = parser.extract()
        drones = []
        for d in range(map.nb_drones):
            drones.append(Drone("D" + str(d), map.start.coord))
        display = MapDisplay(map, drones)
        display.run()
    except ParsingError as e:
        print(e)
