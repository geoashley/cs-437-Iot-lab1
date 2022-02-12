

from concurrent.futures import thread
import math
import time
from detect import stop_sign_detection
from drive import backward, forward, stop, turn_left, turn_right
from mapping import get_scan
from recalculate import recalculate_axes
from routing import SquareGrid, a_star_search, draw_grid, reconstruct_path
import globalvars
import threading




def scan_interpolate( x_carD, y_carD):
    scan_grid = get_scan(x_carD, y_carD)
    #print("grid map")
    #print(scan_grid)
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

def get_going(xOrg, yOrg, xNew, yNew):
    if (yOrg < yNew): #forward
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
    global squareGrid
    globalvars.init()

    thread_1 = threading.Thread(target=stop_sign_detection)
    thread_1.start()

    # thread_2 = threading.Thread(target=stop_sign_detected)
    # thread_2.start()

    power = 1
    start, goal = (25, 0), (45, 28)
    current = start
    while current != goal:
        squareGrid = SquareGrid(50, 50)
        scan_interpolate(current[0], current[1])
        came_from, cost_so_far = a_star_search(squareGrid, current, goal)
        path=reconstruct_path(came_from, start=current, goal=goal)
      #  print(path)
        draw_grid(squareGrid, path=path)
        no_steps = len(path) if len(path)<20 else 20
        for i in range(1, no_steps):
            next_move = get_going(current[0], current[1], path[i][0], path[i][1])
            direction[next_move](power)
            if(next_move==1 or next_move ==2):
                print("recalculate")
                print(current, goal, next_move)
                start, goal = recalculate_axes(current, goal, next_move)
                print(start, goal)
                time.sleep(0.7)
                current = start
                break
            else:
                time.sleep(0.1)
                current = (path[i][0], path[i][1])
  
            check_stop_sign()
            
        stop()
    globalvars.goal_reached = True
    print("Goal reached !")  
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
