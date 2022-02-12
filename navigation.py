

from mapping import get_scan
from routing import SquareGrid, a_star_search, draw_grid, reconstruct_path

squareGrid = SquareGrid(50, 50)
start, goal = (25, 0), (45, 48)
scan_grid = get_scan(start[0], start[1])
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
        if(consecutive):
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

print(squareGrid.walls)
came_from, cost_so_far = a_star_search(squareGrid, start, goal)

path=reconstruct_path(came_from, start=start, goal=goal)
print(path)
draw_grid(squareGrid, path=path)
