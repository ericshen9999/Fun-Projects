from heapq import heappop, heappush
import math
def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """
    #Variables
    boxes = {}
    path = [] #(x,y)
    boxesF = {} #(distance_goal, (previous_box(x1,x2,y1,y2), location(x,y)))
    boxesB = {} #(distance_goal, (previous_box(x1,x2,y1,y2), location(x,y)))
    queue = [] #(distance_goal, distance_start, box(x1,x2,y1,y2), location(x,y), direction)
    box_pop = None #box(x1,x2,y1,y2)
    
    #Iterate
    for i in mesh['boxes']:
        #If source_point is in box
        if source_point[0] > i[0] and source_point[0] < i[1] and source_point[1] > i[2] and source_point[1] < i[3]:
            #Intialize
            start_box = i
            boxesF[i] = (0,(None,None))
            #temp[i] = 0
            heappush(queue,(0, 0, i, source_point, 'forward'))

        #If destination_point is in box
        if destination_point[0] > i[0] and destination_point[0] < i[1] and destination_point[1] > i[2] and destination_point[1] < i[3]:
            #Intialize
            destination_box = i
            boxesB[i] = (0,(None, None))
            heappush(queue,(0, 0, i, destination_point, 'backwards'))
    
    #Iterate
    while queue:
        #Pop (distance_goal, distance_start, box(x1,x2,y1,y2), location(x,y))
        (other, distance_pop, box_pop, position_pop, direction) = heappop(queue)
        #If 
        if direction == "forward" and box_pop in boxesB:
            box_pop_copy = box_pop
            position_pop_copy = position_pop
            while boxesF[box_pop_copy][1][0] and boxesF[box_pop_copy][1][1]:
                path.append(position_pop_copy)
                position_pop_copy = boxesF[box_pop_copy][1][1]
                box_pop_copy = boxesF[box_pop_copy][1][0]

            path.append(position_pop_copy)
            path.append(source_point)
            path = path[::-1]
            
            while boxesB[box_pop][1][0] and boxesB[box_pop][1][1]:
                path.append(position_pop)
                position_pop = boxesB[box_pop][1][1]
                box_pop = boxesB[box_pop][1][0]

            path.append(position_pop)
            path.append(destination_point)
            break

        elif direction == "backwards" and box_pop in boxesF:
            box_pop_copy = box_pop
            position_pop_copy = position_pop
            while boxesF[box_pop_copy][1][0] and boxesF[box_pop_copy][1][1]:
                path.append(position_pop_copy)
                position_pop_copy = boxesF[box_pop_copy][1][1]
                box_pop_copy = boxesF[box_pop_copy][1][0]

            path.append(position_pop_copy)
            path.append(source_point)
            path = path[::-1]
            
            while boxesB[box_pop][1][0] and boxesB[box_pop][1][1]:
                path.append(position_pop)
                position_pop = boxesB[box_pop][1][1]
                box_pop = boxesB[box_pop][1][0]

            path.append(position_pop)
            path.append(destination_point)
            break

        #Iterate
        for j in mesh['adj'][box_pop]:
            #New location
            if direction == "forward":
                if j not in boxesF:
                    distance_new, position_new = find_closest(j, position_pop, box_pop, destination_point)
                    distance_end = find_distance(position_new, destination_point)
                    boxesF[j] = (distance_pop + distance_new - distance_end, (box_pop, position_new))
                    heappush(queue, (distance_pop + distance_new - distance_end, distance_pop + distance_new, j, position_new, "forward"))
            else:
                if j not in boxesB:
                    distance_new, position_new = find_closest(j, position_pop, box_pop, source_point)
                    distance_end = find_distance(position_new, source_point)
                    boxesB[j] = (distance_pop + distance_new - distance_end, (box_pop, position_new))
                    heappush(queue, (distance_pop + distance_new - distance_end, distance_pop + distance_new, j, position_new, "backwards"))
        #Error catching
        if box_pop not in boxesF and box_pop not in boxesB:
            return None, None
    #Search for Path

    if (len(path) == 0):
        print("Path not Found!")
        return [], {}

    boxes.update(boxesF)
    boxes.update(boxesB)

    #return path, temp.keys()
    return path, boxes.keys()

def find_closest(box1, curPos, box_pop, dest_point):
    output = []
    #find where 2 boxes touch [Not Done Yet]
    if box_pop[0] >= box1[0] and box_pop[0] <= box1[1]:
        if box_pop[2] == box1[3]:
            heappush(output,(find_distance((box_pop[0],box_pop[2]),curPos) + find_distance((box_pop[0],box_pop[2]),dest_point), (box_pop[0],box_pop[2])))
        if box_pop[3] == box1[2]:
            heappush(output,(find_distance((box_pop[0],box_pop[3]),curPos) + find_distance((box_pop[0],box_pop[3]),dest_point), (box_pop[0],box_pop[3])))
    if box_pop[1] >= box1[0] and box_pop[1] <= box1[1]:
        if box_pop[2] == box1[3]:
            heappush(output,(find_distance((box_pop[1],box_pop[2]),curPos) + find_distance((box_pop[1],box_pop[2]),dest_point), (box_pop[1],box_pop[2])))
        if box_pop[3] == box1[2]:
            heappush(output,(find_distance((box_pop[1],box_pop[3]),curPos) + find_distance((box_pop[1],box_pop[3]),dest_point), (box_pop[1],box_pop[3])))
    if box_pop[2] >= box1[2] and box_pop[2] <= box1[3]:
        if box_pop[0] == box1[1]:
            heappush(output,(find_distance((box_pop[0],box_pop[2]),curPos) + find_distance((box_pop[0],box_pop[2]),dest_point), (box_pop[0],box_pop[2])))
        if box_pop[1] == box1[0]:
            heappush(output,(find_distance((box_pop[1],box_pop[2]),curPos) + find_distance((box_pop[1],box_pop[2]),dest_point), (box_pop[1],box_pop[2])))
    if box_pop[3] >= box1[2] and box_pop[3] <= box1[3]:
        if box_pop[0] == box1[1]:
            heappush(output,(find_distance((box_pop[0],box_pop[3]),curPos) + find_distance((box_pop[0],box_pop[3]),dest_point), (box_pop[0],box_pop[3])))
        if box_pop[1] == box1[0]:
            heappush(output,(find_distance((box_pop[1],box_pop[3]),curPos) + find_distance((box_pop[1],box_pop[3]),dest_point), (box_pop[1],box_pop[3])))

    if box1[0] >= box_pop[0] and box1[0] <= box_pop[1]:
        if box_pop[2] == box1[3]:
            heappush(output,(find_distance((box1[0],box1[3]),curPos) + find_distance((box1[0],box1[3]),dest_point), (box1[0],box1[3])))
        if box_pop[3] == box1[2]:
            heappush(output,(find_distance((box1[0],box1[2]),curPos) + find_distance((box1[0],box1[2]),dest_point), (box1[0],box1[2])))
    if box1[1] >= box_pop[0] and box1[1] <= box_pop[1]:
        if box_pop[2] == box1[3]:
            heappush(output,(find_distance((box1[1],box1[3]),curPos) + find_distance((box1[1],box1[3]),dest_point), (box1[1],box1[3])))
        if box_pop[3] == box1[2]:
            heappush(output,(find_distance((box1[1],box1[2]),curPos) + find_distance((box1[1],box1[2]),dest_point), (box1[1],box1[2])))
    if box1[2] >= box_pop[2] and box1[2] <= box_pop[3]:
        if box_pop[0] == box1[1]:
            heappush(output,(find_distance((box1[1],box1[2]),curPos) + find_distance((box1[1],box1[2]),dest_point), (box1[1],box1[2])))
        if box_pop[1] == box1[0]:
            heappush(output,(find_distance((box1[0],box1[2]),curPos) + find_distance((box1[0],box1[2]),dest_point), (box1[0],box1[2])))
    if box1[3] >= box_pop[2] and box1[3] <= box_pop[3]:
        if box_pop[0] == box1[1]:
            heappush(output,(find_distance((box1[1],box1[3]),curPos) + find_distance((box1[1],box1[3]),dest_point), (box1[1],box1[3])))
        if box_pop[1] == box1[0]:
            heappush(output,(find_distance((box1[0],box1[3]),curPos) + find_distance((box1[0],box1[3]),dest_point), (box1[0],box1[3])))

    return heappop(output)

def find_distance(point1, point2):
    return math.sqrt(abs(point1[0] - point2[0]) ** 2 + abs(point1[1] - point2[1]) ** 2)