

from concurrent.futures import thread
import time
from turtle import st
from drive import backward, forward, stop, turn_left, turn_right
from mapping import get_scan
from routing import SquareGrid, a_star_search, draw_grid, reconstruct_path
from random import randrange



# scan_grid = get_scan(start[0], start[1])
# print("grid map")
# print(scan_grid)
# consecutive = False
# prevX = 0
# prevY = 0 
# for i in range(len(scan_grid)):
#     if ((scan_grid[i][0] > 0) and (scan_grid[i][1] > 0)):
#         x = int(scan_grid[i][0])
#         y = int(scan_grid[i][1])
#         squareGrid.walls.append((x, y))
#         if(consecutive):
#             slope = (prevY-y)/(prevX-x)
#             increment = 1
#             if(prevX>x):
#                 increment = -1
#             print("slope ", slope, prevX, x, increment)
#             for j in range(prevX, x, increment):
#                 interY = int(prevY + ((j-prevX+1)*slope))
#                 print("inter ", j, interY)
#                 squareGrid.walls.append((j, interY))
#         prevX = x
#         prevY = y
#         consecutive = True
#     else:
#         consecutive = False

# print(squareGrid.walls)
# came_from, cost_so_far = a_star_search(squareGrid, start, goal)

# path=reconstruct_path(came_from, start=start, goal=goal)
# print(path)
# draw_grid(squareGrid, path=path)

power = 10
squareGrid = SquareGrid(50, 50)
start, goal = (25, 0), (45, 48)
current = start

def scan_interpolate( x_carD, y_carD):
    scan_grid = get_scan(x_carD, y_carD)
    print("grid map")
    print(scan_grid)
    consecutive = False
    prevX = 0
    prevY = 0 
    for i in range(len(scan_grid)):
        if ((scan_grid[i][0] > 0) and (scan_grid[i][1] > 0)):
            x = int(scan_grid[i][0])
            y = int(scan_grid[i][1])
            squareGrid.walls.append((x, y))
            if(consecutive and prevX != x):
                slope = (prevY-y)/(prevX-x)
                increment = 1
                if(prevX>x):
                    increment = -1
                print("slope ", slope, prevX, x, increment)
                for j in range(prevX, x, increment):
                    interY = int(prevY + ((j-prevX+1)*slope))
                    print("inter ", j, interY)
                    squareGrid.walls.append((j, interY))
            prevX = x
            prevY = y
            consecutive = True
        else:
            consecutive = False
    print("obstacles")
    print(squareGrid.walls)

def get_next(xOrg, yOrg, xNew, yNew):
    xDist = xNew - xOrg 
    yDist = yNew - yOrg 
    forward = 0
    turnLeft = 0
    turnRight = 0

    if (yOrg < yNew):
        for i in range(yDist):
            forward += 1

    if (xNew > xOrg): 
        for i in range(xDist):
            turnLeft += 1

    if (xNew < xOrg): 
        for i in range(abs(xDist)):
            turnRight += 1

    if (turnRight > turnLeft):
        return turnRight, forward

    if (turnLeft > turnRight):
        return turnLeft, forward

    else:
        return 0, forward

# map the next direction
direction = {0 : forward,
             1 : turn_left,
             2 : turn_right,
             3 : backward
}  

def main():
    power = 20
    squareGrid = SquareGrid(50, 50)
    start, goal = (25, 0), (45, 48)
    current = start
    while current != goal:
        scan_interpolate(current[0], current[1])
        came_from, cost_so_far = a_star_search(squareGrid, current, goal)
        path=reconstruct_path(came_from, start=current, goal=goal)
        print(path)
        draw_grid(squareGrid, path=path)
        for i in range(1, 3):
            direction[randrange(0,3)](power)
            time.sleep(0.3)
            stop()
            current = (path[i][0], path[i][1])

if __name__ == '__main__':
  main()
