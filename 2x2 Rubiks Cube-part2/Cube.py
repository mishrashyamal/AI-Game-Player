import random
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

movesAvailable = ["U" , "U'", "R", "R'", "F", "F'", "D", "D'", "L", "L'", "B", "B'"]

complement = {"U": "D'", "U'": "D",
                "L'": "R", "L": "R'",
                "F": "B'", "F'": "B",
                "D'": "U", "D": "U'",
                "R": "L'", "R'": "L",
                "B'": "F", "B": "F'"}

cubeColor = ["W", "R", "B", "Y", "O", "G"]
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
                 49:" ", 50:" ", 51:" ", 52:" ", 53:" ", 54:" ", 55:" ", 56:" ", 57:" ", 58:14, 59:15, 60:" ", 61:" ",
                 62:" ", 63:" ", 64:" ", 65:" ",}

class cube:
  def __init__(self, string="WWWW RRRR GGGG YYYY OOOO BBBB", moves=None):
    self.initialState = string
    self.stateConfig = string.replace(" ", "")
    self.goalState = "WWWW RRRR GGGG YYYY OOOO BBBB"
    if moves is not None:
      self.moves = moves.copy()
    else:
      self.moves = []
    return

  def __lt__(self, other):
    otherState = self.norm(other.stateConfig)

    return self.stateCompare(otherState) > self.stateCompare(self.stateConfig)

  def clone(self):
    return cube(self.stateConfig, moves=list(self.moves))

  def stateCompare(self, state1):
    def colorPosition(color, state):
      return [pos for pos, char in enumerate(state) if char == color]
    
    def diffPos(pos):
      return [pos[i+1]-pos[i] for i in range(len(pos)-1)]
    
    relativeDistance = 0 
    for color in cubeColor:
      pos = colorPosition(color, state1)
      diff = diffPos(pos)
      relativeDistance += sum(diff) - 3

    return relativeDistance

  def norm(self, state):
    opps = {"O": "R", "G": "B", "Y": "W", "R": "O", "B": "G", "W": "Y"}

    posGreen, posYellow, posOrange = state[10], state[12], state[19]
    oppBlue, oppWhite, oppRed = opps[posGreen], opps[posYellow], opps[posOrange]
    
    newState = ""
    for s in state:
      if s == posGreen:
        newState += "G"
      elif s == posYellow:
        newState += "Y"
      elif s == posOrange:
        newState += "O"
      elif s == oppBlue:
        newState += "B"
      elif s == oppWhite:
        newState += "W"
      elif s == oppRed:
        newState += "R"
    return newState

  def isStateValid(self, string):
    if(len(string) > 29): 
      return False
    elif (len(string.split(" ")) != 6):
      print("Invalid spaces input")
      return False
    elif (set(["W", "B", "Y", "R", "O", "G"]) != set(string.replace(" ", ""))): 
      print("Invalid Grid input colors")
      return False

  def getMoveInverse(self, move):
    if len(move) == 1:
      return move + "'"
    else:
      return move[0]

  def isMoveValid(self, move):
    if len(self.moves) <= 1:
      return True
    lastMove = self.moves[-1]
    if complement[move] == lastMove or self.getMoveInverse(move) == lastMove:
      return False
    elif len(move) >=2 and move == lastMove and move == self.moves[-2]:
      return False

    return True 

  def validMoveFast(self, move):
    if len(self.moves) <= 1:
      return True
    lastMove = self.moves[-1]
    if lastMove == move or complement[move] == lastMove or self.getMoveInverse(move) == lastMove:
      return False
    elif len(move) >=2 and move == lastMove and move == self.moves[-2]:
      return False

    return True 

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
    for i in range(0, 66):
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
  moves = list(movesequence)
  printStr = rubikcube.generateGrid()
  for i, m in enumerate(moves):
    rubikcube.applyMove(m)
    if i % 3 == 2:
      print(printStr)
      printStr = rubikcube.generateGrid()
      continue
    cubeGrid = rubikcube.generateGrid()
    printStr = "\n".join(["  ".join(s)
                            for s in zip(printStr.split("\n"), cubeGrid.split("\n"))])
  print(printStr)

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
