

def recalculate_axes(current, goal, move):
    gx = goal[0]
    gy = goal[1]
    cx = current[0]
    cy = current[1]
    if move == 2:
        # startX = current[1]
        # startY = 0
        goalX = 25 + (gy - cy)
        goalY = 25 - gx
    if move == 1:
        # startX = 50 - current[1]
        # startY = 0
        goalX = 25 + (gy - cy) 
        goalY = gx - 25
    return (25, 0), (goalX, goalY)

def main():
    print("(25, 5), (49, 49), 2 right -> ",  recalculate_axes((25, 5), (49, 49), 2))
    print("(25, 5), (1, 49) , 1 left -> 1", recalculate_axes((25, 5), (1, 49) , 1))
    print("(25, 29) ,(45, 48), 2 right -> ",recalculate_axes((25, 29) ,(45, 48), 2))
    print("(26, 19), (1, 20), 1 left -> ",recalculate_axes((26, 19), (1, 20), 1))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

