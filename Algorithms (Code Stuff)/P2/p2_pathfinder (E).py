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
    path = [] #(x,y)
    boxes = {} #(distance_goal, (previous_box(x1,x2,y1,y2), location(x,y)))
    temp = {} #Irrelevent
    queue = [] #(distance_goal, distance_start, box(x1,x2,y1,y2), location(x,y))
    destination_box = None #box(x1,x2,y1,y2)
    box_pop = None #box(x1,x2,y1,y2)
    
    print("Start")
    print(source_point)
    print("End")
    print(destination_point)
    
    #Iterate
    for i in mesh['boxes']:
        #If source_point is in box
        if source_point[0] > i[0] and source_point[0] < i[1] and source_point[1] > i[2] and source_point[1] < i[3]:
            #Intialize
            boxes[i] = (0,(None,None))
            #temp[i] = 0
            queue = [(0, 0, i, source_point)]

            print("Start Box")
            print(i)
        #If destination_point is in box
        if destination_point[0] > i[0] and destination_point[0] < i[1] and destination_point[1] > i[2] and destination_point[1] < i[3]:
            #Intialize
            destination_box = i

            print("End Box")
            print(i)
    
    print("Queue")

    #Iterate
    while queue:
        #Pop (distance_goal, distance_start, box(x1,x2,y1,y2), location(x,y))
        (other, distance_pop, box_pop, position_pop) = heappop(queue)
        #If end
        if box_pop == destination_box:
            #Add ending path
            path.append(destination_point)
            path.append(position_pop)
            #temp[box_pop] = 0
            break
        #Iterate
        for j in mesh['adj'][box_pop]:
            #New location
            if j not in boxes:
                distance_new, position_new = find_closest(j, position_pop, box_pop)
                distance_end = find_distance(position_new, destination_point)
                boxes[j] = (distance_pop + distance_new - distance_end, (box_pop, position_new))
                heappush(queue, (distance_pop + distance_new, distance_pop + distance_new - distance_end, j, position_new))
        #Error catching
        if box_pop not in boxes:
            return None, None
    #Search for Path
    check_box = destination_box

    print("Boxes")

    #Iterate
    if check_box not in boxes:
        print("Error: Path not found")
        return [], {}
    while True:

        print(check_box)

        #Check previous box
        check_box = boxes[check_box][1][0]
        if check_box == None or boxes[check_box][1][1] == None:
            break
        #Add to path
        path.append(boxes[check_box][1][1])
        #temp[check_box] = 0
    #Add start location
    path.append(source_point)
    
    print("Path")
    print(path)

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


    #if box1[0] >= box_pop[0] and box1[0] <= box_pop[1]:
    #if box1[1] >= box_pop[0] and box1[1] <= box_pop[1]:
    #if box1[0] >= box_pop[2] and box1[0] <= box_pop[3]:
    #if box1[1] >= box_pop[2] and box1[1] <= box_pop[3]:

    #(distance, location(x,y))
    #output.append((find_distance((box1[0],box1[2]),curPos), (box1[0],box1[2])))
    #output.append((find_distance((box1[1],box1[2]),curPos), (box1[1],box1[2])))
    #output.append((find_distance((box1[0],box1[3]),curPos), (box1[0],box1[3])))
    #output.append((find_distance((box1[1],box1[3]),curPos), (box1[1],box1[3])))
    #output.sort()

    return heappop(output)

def find_distance(point1, point2):
    return math.sqrt(abs(point1[0] - point2[0]) ** 2 + abs(point1[1] - point2[1]) ** 2)