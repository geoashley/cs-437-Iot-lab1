import time
from typing import List
from detect import stop_sign_detection
from drive import backward, forward, get_distance_at_no_wait, stop, turn_left, turn_right
from mapping import get_scan
from recalculate import recalculate_axes, recalculate_axes_new, recalculate_axes_swap
from routing import GridLocation, SquareGrid, a_star_search, draw_grid, reconstruct_path
import globalvars
import threading

def scan_interpolate( x_carD, y_carD, squareGrid):
    scan_grid = get_scan(x_carD, y_carD)
    print("grid map")
    print(scan_grid)
    consecutive = False
    prevX = 0
    prevY = 0 
    for i in range(len(scan_grid)):
        x = int(scan_grid[i][0])
        y = int(scan_grid[i][1])

        if ((x, y)!=(x_carD, y_carD) ):
            squareGrid.walls.append((x, y))
            squareGrid.walls.append((x, y-1))
            squareGrid.walls.append((x, y-2))
            if(consecutive and prevX != x):
                slope = (prevY-y)/(prevX-x)
                increment = 1
                if(prevX>x):
                    increment = -1
              #  print("slope ", slope, prevX, x, increment)
                for j in range(prevX, x, increment):
                    interY = int(prevY + ((j-prevX+1)*slope))
               #     print("inter ", j, interY)
                    squareGrid.walls.append((j, interY))
            prevX = x
            prevY = y
            consecutive = True
        else:
            consecutive = False
    print("obstacles")
    print(squareGrid.walls)

def get_new_orientation( next_move, orientation):
    if next_move == 1:
        orientation -= 1
        if orientation <0:
            orientation = 3
    if next_move == 2:
        orientation += 1
        if orientation > 3:
            orientation = 0
    return orientation



def get_going(xOrg, yOrg, xNew, yNew, orientation):
    print("get going ", xOrg, yOrg, xNew, yNew)
    if orientation == 0: #north
        if (yOrg < yNew): #forward
            print("forward")
            return 0
            
        if (xNew < xOrg): #left
            print("Left")
            return 1
        if (xNew > xOrg): #right
            print("right")
            return 2
        else:
            print("backward")
            return 3
    if orientation == 1: #east
        if (xOrg < xNew): #forward
            print("forward")
            return 0
            
        if (yNew > yOrg): #left
            print("Left")
            return 1
        if (yNew < yOrg): #right
            print("right")
            return 2
        else:
            print("backward")
            return 3
    if orientation == 2:#south
        if (yOrg > yNew): #forward
            print("forward")
            return 0
            
        if (xNew > xOrg): #left
            print("Left")
            return 1
        if (xNew < xOrg): #right
            print("right")
            return 2
        else:
            print("backward")
            return 3
    if orientation == 3:#west
        if (xOrg > xNew): #forward
            print("forward")
            return 0
            
        if (yNew < yOrg): #left
            print("Left")
            return 1
        if (yNew > yOrg): #right
            print("right")
            return 2
        else:
            print("backward")
            return 3


# map the next direction
direction = {0 : forward,
             1 : turn_left,
             2 : turn_right,
             3 : backward
}  

def check_stop_sign():
    if globalvars.stop_sign_found == True:
        stop()
        time.sleep(2)
        globalvars.stop_sign_found = False

def main():
    #squareGrid
    orientation = 0
    globalvars.init()

    thread_1 = threading.Thread(target=stop_sign_detection)
    thread_1.start()

    power = 1
    start, goal = (25, 0), (49, 49)
    current = start
    squareGrid = SquareGrid(50, 50)
    while current != goal:
        squareGrid.walls = []
        scan_interpolate(current[0], current[1], squareGrid)
        came_from, cost_so_far = a_star_search(squareGrid, current, goal)
        path=reconstruct_path(came_from, start=current, goal=goal)
        print(path)
        draw_grid(squareGrid, path=path)
        no_steps = len(path) if len(path)<20 else 20
        for i in range(1, no_steps):
            next_move = get_going(current[0], current[1], path[i][0], path[i][1], orientation)
            orientation = get_new_orientation(next_move, orientation)

            print("next movee ", next_move)
            print("orientation ", orientation)

            direction[next_move](power)
            if(next_move==1 or next_move ==2):
                # print(current, goal, next_move)
                # start, goal = recalculate_axes_swap(current, goal, next_move)
                # print(start, goal)
                print("taking a turn")
                time.sleep(1.2)
                print("moving a bit")
                stop()
                direction[0](10)
                time.sleep(0.6 )
                current = (path[i][0], path[i][1])

                # current = start
                break
            else:
                check_stop_sign()
                dist = get_distance_at_no_wait(0)
                print("foward US dist ", dist)
                if dist > 0 and dist < 10:
                    break
                time.sleep(0.01 )
                current = (path[i][0], path[i][1])
            
        stop()
    globalvars.goal_reached = True
    print("Goal reached !")  
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
