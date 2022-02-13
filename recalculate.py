

# def recalculate_axes(current, goal, move):
#     gx = goal[0]
#     gy = goal[1]
#     cx = current[0]
#     cy = current[1]
#     if move == 2:
#         # startX = current[1]
#         # startY = 0
#         goalX = 25 + (gy - cy)
#         goalY = 25 - gx
#     if move == 1:
#         # startX = 50 - current[1]
#         # startY = 0
#         goalX = 25 + (gy - cy) 
#         goalY = gx - 25
#     return (25, 0), (goalX, goalY)

import math

def recalculate_axes_swap(current, goal, move):
    return current, (50 -goal[0], goal[1])

def recalculate_axes_new(current, goal, move):
    angle = 90
        
    if move == 1:
        angle = -90
    newCurrent, newGoal = rotate_around_point_highperf(current, math.radians(angle)), rotate_around_point_highperf(goal, math.radians(angle))
    print(newCurrent,newGoal)
    if move == 2:
        newCurrent = (newCurrent[0], 25+newCurrent[1])
        newGoal = (newGoal[0], 50 + newGoal[1])
    if move == 1:
        newCurrent = (25+newCurrent[0], newCurrent[1])
        newGoal = (50+newGoal[0], newGoal[1])
    return newCurrent, newGoal

def rotate_around_point_highperf(xy, radians, origin=(0, 0)):
    """Rotate a point around a given point.
    
    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    x, y = xy
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = int(offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y)
    qy = int(offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y)

    return qx, qy

def recalculate_axes(current, goal, move):
    gx = goal[0]
    gy = goal[1]
    cx = current[0]
    cy = current[1]

    angle = -90
        
    if move == 1:
        angle = 90

    sin = math.sin(math.radians(angle))
    cos = math.cos(math.radians(angle))

    new_gx = int(gx * cos + gy * sin)
    new_gy = int(gy * cos - gx * sin)
    new_cx = int(cx * cos + cy * sin)
    new_cy = int(cy * cos - cx * sin)

    return (new_cx, new_cy), (new_gx, new_gy)

def main():
    # print("(25, 5), (49, 49), 2 right -> ",  recalculate_axes((25, 5), (49, 49), 2))
    # print("(25, 5), (1, 49) , 1 left -> 1", recalculate_axes((25, 5), (1, 49) , 1))
    # print("(25, 29) ,(45, 48), 2 right -> ",recalculate_axes((25, 29) ,(45, 48), 2))
    # print("(26, 19), (1, 20), 1 left -> ",recalculate_axes((26, 19), (1, 20), 1))

    print("------------------------------")
    print("(25, 5), (49, 49), 2 right -> ",  recalculate_axes_new((25, 5), (49, 49), 2))
    print("(25, 29) ,(45, 48), 2 right -> ",recalculate_axes_new((25, 29) ,(45, 48), 2))
    print("(25, 5), (1, 49) , 1 left -> 1", recalculate_axes_new((25, 5), (1, 49) , 1))
    print("(26, 19), (1, 20), 1 left -> ",recalculate_axes_new((26, 19), (1, 20), 1))

    print("------------------------------")
    print("(25, 5), (49, 49), 2 right -> ",  recalculate_axes_swap((25, 5), (49, 49), 2))
    print("(25, 29) ,(45, 48), 2 right -> ",recalculate_axes_swap((25, 29) ,(45, 48), 2))
    print("(25, 5), (1, 49) , 1 left -> 1", recalculate_axes_swap((25, 5), (1, 49) , 1))
    print("(26, 19), (1, 20), 1 left -> ",recalculate_axes_swap((26, 19), (1, 20), 1))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

