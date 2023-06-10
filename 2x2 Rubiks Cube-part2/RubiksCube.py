import Cube as rubiksCube
from time import time
import sys
import heapq

def bfs(moves):
    cubeInit = rubiksCube.cube()
    cubeInit.applyMovesStr(moves)
    open = [cubeInit]
    closed = {}
    count = 0
    while open:
        node = open.pop(0)
        if (node.isSolved(node.stateConfig)):
            return [node.moves, count, cubeInit.stateConfig]
        closed[node.stateConfig] = 1
        
        for m in rubiksCube.movesAvailable:
            if node.isMoveValid(m) is False:
                continue
            child = node.clone()
            child.applyMove(m)
            child.moves.append(m)
            count += 1
            if child.stateConfig not in closed:
                open.append(child)

def getDepth(moves):
    return len(moves)

def dls(node, level):  
    iterations = 0 
    if (node.isSolved(node.stateConfig)):
        return node, iterations
    if (getDepth(node.moves) == level):
        return False, iterations
    
    # closed[node.stateConfig] = 1
    for m in rubiksCube.movesAvailable:
        if node.isMoveValid(m) is False:
            continue
        child = node.clone()
        child.applyMove(m)
        child.moves.append(m)
        iterations += 1
        # if child.stateConfig not in closed:
        result, itr = dls(child, level)
        iterations += itr
        if result is not False:
            return result, iterations
        
    return False, iterations

def ids():
    if (len(sys.argv) > 4):
        print("Cannot accept more than 3 args.")
        return

    shuffleMoves = getArg(2)
    depth = int(getArg(3))

    cubeInit = rubiksCube.cube()
    cubeInit.applyMovesStr(shuffleMoves)
    start = cubeInit
    totalIterations = 0
    for i in range(0,depth):
        state_t = time()
        result, iterations = dls(start, i)
        print("Depth: " + str(i) + " d: " + str(iterations))
        end_t = time()
        totalIterations += iterations
        if result is not False:
            print("IDS found a solution at depth " + str(i))
            print(" ".join(result.moves))
            rubiksCube.printMoves(result.moves, start.stateConfig)
            print(totalIterations)
            print(round(end_t - state_t, 2))
            break

def depthHeuristics(moves, n):
    return getDepth(moves)*n

def a_star(moves):
    cubeInit = rubiksCube.cube()
    cubeInit.applyMovesStr(moves)
    count = 0
    closed = {}
    open = []
    heapq.heappush(open, (0, cubeInit))
    while open:
        node = heapq.heappop(open)
        if (node[1].isSolved(node[1].stateConfig)):
            return [node[1].moves, count, cubeInit.stateConfig]
        closed[node[1].stateConfig] = True
        for m in rubiksCube.movesAvailable:
            if node[1].isMoveValid(m) is False:
                continue
            count += 1
            child = node[1].clone()
            child.applyMove(m)
            child.moves.append(m)
            if child.stateConfig not in closed:
                newCost = depthHeuristics(child.moves, 9) + child.stateCompare(child.stateConfig)
                heapq.heappush(open, (newCost, child))

def a_star_compete(moves, movesWeight):
    cubeInit = rubiksCube.cube()
    cubeInit.applyMovesStr(moves)
    count = 0
    closed = {}
    open = []
    heapq.heappush(open, (0, cubeInit))
    while open:
        node = heapq.heappop(open)
        if (node[1].isSolved(node[1].stateConfig)):
            return [node[1].moves, count, cubeInit.stateConfig]
        closed[node[1].stateConfig] = True
        for m in rubiksCube.movesAvailable:
            if node[1].validMoveFast(m) is False:
                continue
            count += 1
            child = node[1].clone()
            child.applyMove(m)
            child.moves.append(m)
            if child.stateConfig not in closed:
                newCost = depthHeuristics(child.moves, movesWeight) + child.stateCompare(child.stateConfig)
                heapq.heappush(open, (newCost, child))

def printGrid():
    if (len(sys.argv) > 3):
        print("Cannot accept more than 2 args.")
        return

    cubeState = getArg(2)    
    if cubeState != None:
        rubikCube = rubiksCube.cube(cubeState)
        if rubikCube.isStateValid(cubeState) is False:
            return "State Not Valid!"
        print(rubikCube.generateGrid())
    else:
        rubikCube = rubiksCube.cube()
        print(rubikCube.generateGrid())

def getGoalStatus():
    if (len(sys.argv) > 3):
        print("Cannot accept more than 2 args.")
        return

    cubeState = getArg(2)
    if cubeState != None:
        rubikCube = rubiksCube.cube(cubeState)
        if rubikCube.isStateValid(cubeState) is False:
            return "State Not Valid!"
        print(rubikCube.isSolved(cubeState))
    else:
        return "Give cube state"

def executeMoves():
    if (len(sys.argv) > 4):
        print("Cannot accept more than 3 args.")
        return

    moves = getArg(2)
    cubeState = getArg(3)
    if cubeState is not None:
        rubikCube = rubiksCube.cube(cubeState)
        if rubikCube.isStateValid(cubeState) is False:
            return "State Not Valid!"
        rubikCube.applyMovesStr(moves)
        print(rubikCube.generateGrid())
    else:
        rubikCube = rubiksCube.cube()
        rubikCube.applyMovesStr(moves)
        print(rubikCube.generateGrid())

def shuffleGrid():
    if (len(sys.argv) > 3):
        print("Cannot accept more than 3 args.")
        return

    shuffleNum = int(getArg(2))
    rubikCube = rubiksCube.cube()
    rubikCube.shuffle(shuffleNum)
    print(rubikCube.generateGrid())

def doRandomWalk():
    if (len(sys.argv) > 5):
        print("Cannot accept more than 4 args.")
        return

    shuffleMoves = getArg(2)
    movesAllowed = getArg(3)
    timeAllowed = getArg(4)

    result = rubiksCube.randomWalk(shuffleMoves, int(movesAllowed), int(timeAllowed))
    if (result["time"] == None):
        print("No solution in the time limit!!")
    else:
        print(result["iterations"])
        print(result["time"])

def doBFS():
    if (len(sys.argv) > 3):
        print("Cannot accept more than 3 args.")
        return

    shuffleMoves = getArg(2) 
    state_t = time()
    result = bfs(shuffleMoves)
    end_t = time()
    print(" ".join(result[0]))
    rubiksCube.printMoves(result[0], result[2])
    print(result[1])
    print(round(end_t - state_t, 2))

def doDLS():
    if (len(sys.argv) > 4):
        print("Cannot accept more than 3 args.")
        return

    shuffleMoves = getArg(2)
    depth = int(getArg(3))

    cubeInit = rubiksCube.cube()
    cubeInit.applyMovesStr(shuffleMoves)
    start = cubeInit
    
    state_t = time()
    result, iterations = dls(start, depth)
    end_t = time()
    if result is not False:
        print(" ".join(result.moves))
        rubiksCube.printMoves(result.moves, start.stateConfig)
        print(iterations)
    print(round(end_t - state_t, 2))

def runCompetition():
    if (len(sys.argv) > 3):
        print("Cannot accept more than 3 args.")
        return

    shuffleMoves = getArg(2) 
    movesCount = shuffleMoves.split(" ")
    movesWeight = 1 if len(movesCount) > 8 else 9

    state_t = time()
    result = a_star_compete(shuffleMoves, movesWeight)
    end_t = time()
    print(" ".join(result[0]))
    rubiksCube.printMoves(result[0], result[2])
    print(result[1])
    print(round(end_t - state_t, 4))

def doAstar():
    if (len(sys.argv) > 3):
        print("Cannot accept more than 3 args.")
        return

    shuffleMoves = getArg(2) 
    
    state_t = time()
    result = a_star(shuffleMoves)
    end_t = time()
    print(" ".join(result[0]))
    rubiksCube.printMoves(result[0], result[2])
    print(result[1])
    print(round(end_t - state_t, 2))

def doNorm():
    if (len(sys.argv) > 3):
        print("Cannot accept more than 3 args.")
        return
    
    state = getArg(2) 
    cubeInit = rubiksCube.cube(state)
    cubeInit.stateConfig = cubeInit.norm(cubeInit.stateConfig)
    print(cubeInit.generateGrid())

def getArg(index):
    return sys.argv[index] if len(sys.argv) > index else None

if __name__ == '__main__':
    commandMethod = getArg(1)

    if (commandMethod == "print"):
        printGrid()
    elif (commandMethod == "goal"):
        getGoalStatus()
    elif (commandMethod == "applyMovesStr"):
        executeMoves()
    elif (commandMethod == "shuffle"):
        shuffleGrid()
    elif (commandMethod == "random"):
        doRandomWalk()
    elif (commandMethod == "bfs"):
        doBFS()
    elif (commandMethod == "dls"):
        doDLS()
    elif (commandMethod == "ids"):
        ids()
    elif (commandMethod == "astar"):
        doAstar()
    elif (commandMethod == "norm"):
        doNorm()
    elif (commandMethod == "competition"):
        runCompetition()
    else:
        print("Enter valid command")
