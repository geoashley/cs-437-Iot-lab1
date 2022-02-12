

def recalculate_axes(current, goal, move):
    if move == 2:
        startX = current[1]
        startY = 0
        goalX = goal[1] - current[1]
        goalY = current[0] - goal[0]
        return (startX, startY), (goalX, goalY)
    if move == 1:
        startX = 50 - current[1]
        startY = 0
        goalX = 50 - goal[1] 
        goalY = goal[0] - current[0]
        return (startX, startY), (goalX, goalY)

def main():
    print(recalculate_axes((25, 5), (49, 49), 2))
    print(recalculate_axes((25, 5), (1, 49) , 1))
    print(recalculate_axes((25, 29) ,(45, 48), 1))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

