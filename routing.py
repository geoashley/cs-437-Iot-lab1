
from __future__ import annotations
from cmath import sqrt
from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional
T = TypeVar('T')

Location = TypeVar('Location')
class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass

import heapq

# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " A "
    if 'goal' in style and id == style['goal']:   r = " Z "
    if id in graph.walls: r = "###"
    return r

def draw_grid(graph, **style):
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)

# data from main article
DIAGRAM1_WALLS = [from_id_width(id, width=30) for id in [21,22,51,52,81,82,93,94,111,112,123,124,133,134,141,142,153,154,163,164,171,172,173,174,175,183,184,193,194,201,202,203,204,205,213,214,223,224,243,244,253,254,273,274,283,284,303,304,313,314,333,334,343,344,373,374,403,404,433,434]]

GridLocation = Tuple[int, int]

class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []
    
    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: Dict[GridLocation, float] = {}
    
    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)

diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}

squareGrid = SquareGrid(10, 10)
squareGrid.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


# thanks to @m1sp <Jaiden Mispy> for this simpler version of
# reconstruct_path that doesn't have duplicate entries

def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:

    current: Location = goal
    path: List[Location] = []
    while current != start: # note: this will fail if no path found
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def heuristic(a: GridLocation, b: GridLocation) -> float:
    import math
    (x1, y1) = a
    (x2, y2) = b
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            #new_cost = cost_so_far[current] + graph.cost(current, next)
            if(next[0]==current[0]):
                cost = 1
            else:
                cost = 2
            new_cost = cost_so_far[current] + cost

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

class SquareGridNeighborOrder(SquareGrid):
    def neighbors(self, id):
        (x, y) = id
        neighbors = [(x + dx, y + dy) for (dx, dy) in self.NEIGHBOR_ORDER]
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return list(results)

# start, goal = (1, 4), (8, 3)
# came_from, cost_so_far = a_star_search(diagram4, start, goal)
# draw_grid(diagram4, point_to=came_from, start=start, goal=goal)
# print()
# draw_grid(diagram4, path=reconstruct_path(came_from, start=start, goal=goal))

# start, goal = (1, 4), (8, 3)
# came_from, cost_so_far = a_star_search(diagram4, start, goal)
# draw_grid(diagram4, number=cost_so_far, start=start, goal=goal)
 

# print(range(squareGrid.height))
# print(range(squareGrid.width))
# start, goal = (1, 4), (8, 3)
# print(squareGrid.walls)
# came_from, cost_so_far = a_star_search(squareGrid, start, goal)
# #draw_grid(squareGrid, point_to=came_from, start=start, goal=goal)
# #print(came_from)
# path=reconstruct_path(came_from, start=start, goal=goal)
# print(path)
# draw_grid(squareGrid, path=path)

#start, goal = (1, 4), (8, 3)
#came_from, cost_so_far = a_star_search(squareGrid, start, goal)
#draw_grid(squareGrid, number=cost_so_far, start=start, goal=goal)

start, goal = (25, 0), (49, 49)
current = start
squareGrid = SquareGrid(50, 50)
squareGrid.walls = [(25, 35),(25, 34),(25, 33),  (23, 33), (25, 36), (24, 35), (20, 34), (23, 32), (22, 33), (21, 33)]
came_from, cost_so_far = a_star_search(squareGrid, current, goal)
path=reconstruct_path(came_from, start=current, goal=goal)
print(path)
draw_grid(squareGrid, path=path)