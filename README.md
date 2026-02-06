*This project has been created as part of the 42 curriculum by relaforg*

# Description
The **Fly In** project introduces graph-theory and pathfinding algorithms. The goal is to make a drone fleet goes from the start to end point in a graph environment modelised by hubs and connections. Each hubs and connections may have differents proterties like max_capacity or type. We are asked to find the most efficient sequence of turn to achieve said goal. During a turn, multiple drones may move.

# Instructions
To install all dependencies
```bash
make install
```

To run the program
```bash
make run
```

You are now greeted by a menu where you can browse and select all the maps present in the **maps** folder.

# Ressources
- Wikipedia
- ChatGPT

# Algorithm
I run a Dijkstra algorithm from the goal hub, then reverse the dictionnary and sort each list by cost and priority. That way from any hub I can access in order the best path to follow and the number of steps to reach the goal hub. So for each drone, I retrieve the path list, check if the best is free, if not check if the second-best is, and so on. If an auxilary path is free, before choosing I check if waiting is not smarter. If all paths are occuped, the drone will wait a turn.

# Visual
The visual representation is done with the 42 mlx library. Hubs are represented by white or colored squares, connections by lines and white horizontal rectangle. You can also see if and how many drones are present on a hub or connections. You can see the total number of turn required to solve the map.
- By draging and droping you can move the graph.
- You can double-click on hubs and connections to display more informations on them.
- You can press the left and right arrows to move forward or backward one turn, thus indicating the state of the map.
