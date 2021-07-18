from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush

import time

def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    queue = []
    checkList = []
    returnList = []
    spaces = {}
    location = initial_position
    cost = (0,None)
    spaces[location] = (cost,None)
    while True:
        checkList = adj(graph,location)
        for j in checkList:
            if j[1] not in spaces:
                spaces[j[1]] = ((j[0]+cost[0],location))
                heappush(queue, ((j[0]+cost[0],location),j[1]))
        if(len(queue) <= 0):
            break
        cost, location = heappop(queue)
        spaces[location] = cost
        if(location == destination):
            break
    if(destination not in spaces):
        return None

    pathLocation = destination
    returnList.append(pathLocation)
    while True:
        returnList.append(spaces[pathLocation][1])
        if(pathLocation == initial_position):
            break
        pathLocation = spaces[pathLocation][1]
    return returnList


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    
    """
    queue = []
    checkList = []
    visitList = {}
    spaces = {}
    location = initial_position
    cost = 0
    spaces[location] = cost
    visitList[location] = cost
    while True:
        checkList = adj(graph,location)
        for j in checkList:
            if j[1] not in visitList:
                visitList[j[1]] = j[0] + cost
                heappush(queue, (j[0] + cost, j[1]))
            elif j[0] + cost < visitList[j[1]]:
                visitList[j[1]] = j[0] + cost
                heappush(queue, (j[0] + cost, j[1]))

        if(len(queue) <= 0):
            break
        cost, location = heappop(queue)
        if location not in spaces:
            spaces[location] = cost
        elif spaces[location] > cost:
            spaces[location] = cost
    return spaces


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
        (I flipped this to be (cost, coordinates))
    
    """
    output = []
    if cell in level['spaces'].keys():
        selfcost = level['spaces'][cell]
    else:
        return None
    for x in range(-1,2):
        for y in range(-1,2):
            if x == 0 and y == 0:
                continue
            next = (cell[0] + x, cell[1] + y)
            if next in level['spaces'].keys():
                cost = level['spaces'][next]
                if x == 0 or y == 0:
                    distance = selfcost * 0.5 + cost * 0.5
                else:
                    distance = selfcost * 0.5 * sqrt(2) + cost * 0.5 * sqrt(2)
                output.append((distance,next))
    return output


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.

    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'my_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
