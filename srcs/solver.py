from typing import Dict, List, TypeAlias
from reverse_cost_bfs import Path
from map import Map
from drone import Drone
from copy import deepcopy

State: TypeAlias = Dict[str, List[Drone]]


class Solver:
    def __init__(self, map: Map, paths: Dict[str, List[Path]]) -> None:
        self.map = map
        self.paths = paths
        self.drones = []
        for i in range(self.map.nb_drones):
            self.drones.append(Drone(f"D{i + 1}", self.map.start.name))

    def _is_path_valid(self, state: State, path: Path) -> bool:
        if (path.src.name == self.map.end.name or
                len(state[path.src.name]) < path.src.max_drones):
            return (True)
        return (False)

    def run(self) -> List[State]:
        states: List[State] = []
        states.append({h.name: [] for h in self.map.hubs})
        states[0][self.map.start.name] = list(self.drones)
        tmp_state: State = states[0]
        while (len(tmp_state.get(self.map.end.name, [])) < self.map.nb_drones):
            for idx, drone in enumerate(self.drones):
                for path in self.paths[drone.location]:
                    if (self._is_path_valid(tmp_state, path)):
                        tmp_state[drone.location].remove(drone)
                        drone.location = path.src.name
                        tmp_state[path.src.name].append(drone)
                        break
            states.append(deepcopy(tmp_state))
        return (states)
