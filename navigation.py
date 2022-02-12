

from mapping import get_scan
from routing import SquareGrid, a_star_search, draw_grid, reconstruct_path




squareGrid = SquareGrid(10, 10)
#squareGrid.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
start, goal = (5, 0), (8, 9)
scan_grid = get_scan(start[0], start[1])
print("grid map")
print(scan_grid)
prev = 0
for i in range(len(scan_grid)):
    if ((scan_grid[i][0] > 0) and (scan_grid[i][1] > 0)):
        squareGrid.walls.append((scan_grid[i][0], scan_grid[i][1]))
print(squareGrid.walls)
came_from, cost_so_far = a_star_search(squareGrid, start, goal)
#draw_grid(squareGrid, point_to=came_from, start=start, goal=goal)
#print(came_from)
path=reconstruct_path(came_from, start=start, goal=goal)
print(path)
draw_grid(squareGrid, path=path)
