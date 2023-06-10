import random
import sys
import time

# different moves
# https://ruwix.com/online-puzzle-simulators/2x2x2-pocket-cube-simulator.php

MOVES = {
    "U": [2,  0,  3,  1, 20, 21,  6,  7,  4,  5, 10, 11, 12, 13, 14, 15,  8,  9, 18, 19, 16, 17, 22, 23],
    "U'": [1,  3,  0,  2,  8,  9,  6,  7, 16, 17, 10, 11, 12, 13, 14, 15, 20, 21, 18, 19,  4,  5, 22, 23],
    "R": [0,  9,  2, 11,  6,  4,  7,  5,  8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19,  3, 21,  1, 23],
    "R'": [0, 22,  2, 20,  5,  7,  4,  6,  8,  1, 10,  3, 12, 9, 14, 11, 16, 17, 18, 19, 15, 21, 13, 23],
    "F": [0,  1, 19, 17,  2,  5,  3,  7, 10,  8, 11,  9, 6,  4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23],
    "F'": [0,  1,  4,  6, 13,  5, 12,  7,  9, 11,  8, 10, 17, 19, 14, 15, 16,  3, 18,  2, 20, 21, 22, 23],
    "D": [0,  1,  2,  3,  4,  5, 10, 11,  8,  9, 18, 19, 14, 12, 15, 13, 16, 17, 22, 23, 20, 21,  6,  7],
    "D'": [0,  1,  2,  3,  4,  5, 22, 23,  8,  9,  6,  7, 13, 15, 12, 14, 16, 17, 10, 11, 20, 21, 18, 19],
    "L": [23,  1, 21,  3,  4,  5,  6,  7,  0,  9,  2, 11, 8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12],
    "L'": [8,  1, 10,  3,  4,  5,  6,  7, 12,  9, 14, 11, 23, 13, 21, 15, 17, 19, 16, 18, 20,  2, 22,  0],
    "B": [5,  7,  2,  3,  4, 15,  6, 14,  8,  9, 10, 11, 12, 13, 16, 18,  1, 17,  0, 19, 22, 20, 23, 21],
    "B'": [18, 16,  2,  3,  4,  0,  6,  1,  8,  9, 10, 11, 12, 13,  7,  5, 14, 17, 15, 19, 21, 23, 20, 22],
}

movesAvailable = [ "U" , "U'", "R", "R'", "F", "F'", "D", "D'", "L", "L'", "B", "B'"]
'''
sticker indices:

      0  1
      2  3
16 17  8  9   4  5  20 21
18 19  10 11  6  7  22 23
      12 13
      14 15

face colors:

    0
  4 2 1 5
    3

movesAvailable:
[ U , U', R , R', F , F', D , D', L , L', B , B']
'''

stickerIndices = {0:" ", 1:" ", 2:" ", 3:0, 4:1, 5:" ", 6:" ", 7:" ", 8: " ", 9: " ", 10:" ", 11:" ",
                 12:" ", 13:" ", 14:2, 15:3, 16:" ", 17:" ", 18:" ", 19:" ", 20:" ", 21:" ", 22:16, 23:17,
                 24:" ", 25:8, 26:9, 27:" ", 28:4, 29:5, 30:" ", 31:20, 32:21, 33:18, 34:19, 35:" ",
                 36:10, 37:11, 38:" ", 39:6, 40:7, 41:" ", 42:22, 43:23, 44:" ", 45:" ", 46:" ", 47:12, 48:13,
                 49:" ", 50:" ", 51:" ", 52:" ", 53:" ", 54:" ", 55:" ", 56:" ", 57:" ", 58:14, 59:15}

class cube:

  def __init__(self, string="WWWW RRRR GGGG YYYY OOOO BBBB"):
    # normalize stickers relative to a fixed corner
    self.initialState = string
    self.stateConfig = string.replace(" ", "")
    self.goalState = "WWWW RRRR GGGG YYYY OOOO BBBB"
    return

  def isStateValid(self, string):
    if(len(string) > 29): 
      return False
    elif (len(string.split(" ")) != 6):
      print("Invalid spaces input")
      return False
    elif (set(["W", "B", "Y", "R", "O", "G"]) != set(string.replace(" ", ""))): 
      print("Invalid Grid input colors")
      return False

  def norm(self):
    # your code
    return

  def equals(self, cube):
    # your code
    return

  def clone(self):
    # your code
    return
    
  def stateCompare(self, state1, state2):
    if state1 == state2:
      return True
    return False

    # apply a move to a state
  def applyMove(self, move):
    if move not in movesAvailable:
      return "Invalid move"

    initalStatePositions = list(self.stateConfig)
    movePermuatation = MOVES[move]
    afterMove = [initalStatePositions[i] for i in movePermuatation]
    self.stateConfig = ''.join(afterMove)

    # apply a string sequence of moves to a state
  def applyMovesStr(self, alg):
    listOfMoves = alg.split(" ")
    for m in listOfMoves:
      self.applyMove(m)
    return

    # check if state is solved
  def isSolved(self, state):
    goalStateConfig = self.goalState.split(" ")
    currentState = state.replace(" ", "")
    currentStateConfig = [currentState  [i:i+4] for i in range(0, len(currentState), 4)]
    for state in currentStateConfig:
      if state not in goalStateConfig:
        return False
    return True

    # print state of the cube
  def generateGrid(self):
    stateGrid = ""
    for i in range(0, 60):
      if stickerIndices[i] == " ":
        stateGrid += " "
      else:
        stateGrid += self.stateConfig[stickerIndices[i]]

      if i % 11 == 10:
        stateGrid += "\n"
    return stateGrid

  def shuffle(self, n):
    movesSequence = ""
    for i in range(0, n):
      movesSequence += random.choice(movesAvailable) + " "
    print(movesSequence)
    self.applyMovesStr(movesSequence)

# print the result Grid after applying moves to a state
def printMoves(movesequence, state):
  rubikcube = cube(state)
  moves = movesequence.split(" ")
  for m in moves:
    rubikcube.applyMove(m)
    print(rubikcube.generateGrid() + "\n")

def generateMoves():
  return

def randomWalkBias(moves, n, t):
  result = {"time": None, "iterations": None}
  rubiksCube = cube()
  rubiksCube.applyMovesStr(moves)
  initialGridState = rubiksCube.generateGrid()
  endTime = time.time() + t
  startTime = time.time()
  iterations = 0
  rubiksInitialState = rubiksCube.stateConfig
  closed = {}
  firstMove = movesAvailable[:]
  firstMove.remove(moves[0])
  while time.time() < endTime:
    movesSequence = ""
    for i in range(0,n):
      if i == 0:
        movesSequence += random.choice(firstMove) + " "
      elif i == n-1:
         movesSequence += random.choice(movesAvailable)
      else:
        movesSequence += random.choice(movesAvailable) + " "
      iterations += 1
    newMoves = movesSequence.split(" ")
    if tuple(newMoves) not in closed: 
      rubiksCube.stateConfig = rubiksInitialState
      rubiksCube.applyMovesStr(movesSequence)
      if rubiksCube.isSolved(rubiksCube.stateConfig):
        currenTime = time.time() - startTime
        print(movesSequence)
        print(initialGridState)
        printMoves(movesSequence, rubiksInitialState) 
        result["time"] = str(currenTime)
        result["iterations"] = str(iterations)
        return result
      closed[tuple(newMoves)] = 1
  return result 

def randomWalk(shuffleMoves, n, t):
  result = {"time": None, "iterations": None}
  rubiksCube = cube()
  rubiksCube.applyMovesStr(shuffleMoves)
  initialGridState = rubiksCube.generateGrid()
  endTime = time.time() + t
  startTime = time.time()
  iterations = 0
  rubiksInitialState = rubiksCube.stateConfig
  while time.time() < endTime:
    movesSequence = ""
    rubiksCube.stateConfig = rubiksInitialState
    iterations += 1
    for i in range(0,n):
      newMove = random.choice(movesAvailable)
      movesSequence += newMove + " "
      rubiksCube.applyMove(newMove)
      if rubiksCube.isSolved(rubiksCube.stateConfig):
        currenTime = time.time() - startTime
        print(movesSequence)
        print(initialGridState + "\n")
        printMoves(movesSequence.rstrip(), rubiksInitialState) 
        result["time"] = str(round(currenTime, 2))
        result["iterations"] = str(iterations)
        return result
  return result 
  
def printGrid():
  if (len(sys.argv) > 3):
    print("Cannot accept more than 2 args.")
    return

  cubeState = getArg(2)
  if cubeState != None:
    rubikCube = cube(cubeState)
    if rubikCube.isStateValid(cubeState) is False:
      return "State Not Valid!"
    print(rubikCube.generateGrid())
  else:
    rubikCube = cube()
    print(rubikCube.generateGrid())

def getGoalStatus():
  if (len(sys.argv) > 3):
    print("Cannot accept more than 2 args.")
    return

  cubeState = getArg(2)
  if cubeState != None:
    rubikCube = cube(cubeState)
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
    rubiksCube = cube(cubeState)
    if rubiksCube.isStateValid(cubeState) is False:
      return "State Not Valid!"
    rubiksCube.applyMovesStr(moves)
    print(rubiksCube.generateGrid())
  else:
    rubiksCube = cube()
    rubiksCube.applyMovesStr(moves)
    print(rubiksCube.generateGrid())

def shuffleGrid():
  if (len(sys.argv) > 3):
    print("Cannot accept more than 3 args.")
    return

  shuffleNum = int(getArg(2))
  rubiksCube = cube()
  rubiksCube.shuffle(shuffleNum)
  print(rubiksCube.generateGrid())

def getArg(index):
	return sys.argv[index] if len(sys.argv) > index else None

def doRandomWalk():
  if (len(sys.argv) > 5):
    print("Cannot accept more than 4 args.")
    return

  shuffleMoves = getArg(2)
  movesAllowed = getArg(3)
  timeAllowed = getArg(4)

  result = randomWalk(shuffleMoves, int(movesAllowed), int(timeAllowed))
  if (result["time"] == None):
    print("No solution in the time limit!!")
  else:
    print(result["iterations"])
    print(result["time"])

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
  else:
    print("Enter valid command")