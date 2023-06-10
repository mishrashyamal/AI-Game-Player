import math
import random
import game

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of moves:
        moves = state.generateMoves()

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]

class RandomAgent(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        moves = state.generateMoves()

        if state.game_over() or len(moves) == 0:
            return

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        
        response = random.randrange(len(moves))
        return moves[response]

class MinimaxAgent(game.Player):
    def __init__(self, depth):
        self.depth = depth
        super().__init__()

    def choose_move(self, state):
        moves = state.generateMoves()
        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))

        if state.game_over() or len(moves) == 0:
            return

        if state.nextPlayerToMove == 0:
            maxEval = -math.inf 
            finalMove = 0
            for i, action in enumerate(moves):
                newState = state.applyMoveCloning(action)
                eval = self.minimax(newState, self.depth)
                if eval > maxEval:
                    finalMove = i
                    maxEval = eval
            return moves[finalMove]

        else:
            minEval = math.inf 
            finalMove = 0
            for i, action in enumerate(moves):
                newState = state.applyMoveCloning(action)
                eval = self.minimax(newState, self.depth)
                if eval < minEval:
                    finalMove = i
                    minEval = eval
            return moves[finalMove]
        
    def minimax(self, state, depth):
        if depth == 0 or state.game_over():
            return state.score()

        if state.nextPlayerToMove == 0:
            maxEval = -math.inf 
            moves = state.generateMoves()
            for action in moves: 
                newState = state.applyMoveCloning(action)
                eval = self.minimax(newState, depth-1)
                maxEval = max(eval, maxEval)
            return maxEval 
        
        else:
            minEval = math.inf 
            moves = state.generateMoves()
            for action in moves: 
                newState = state.applyMoveCloning(action)
                eval = self.minimax(newState, depth-1)
                minEval = min(eval, minEval)
            return minEval 

class AlphaBeta(game.Player):
    def __init__(self, depth):
        self.depth = depth
        super().__init__()

    def choose_move(self, state):
        moves = state.generateMoves()
        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))

        if state.game_over() or len(moves) == 0:
            return

        if state.nextPlayerToMove == 0:
            maxEval = -math.inf 
            finalMove = 0
            for i, action in enumerate(moves):
                newState = state.applyMoveCloning(action)
                eval = self.minimaxPrunning(newState, -math.inf, math.inf, self.depth)
                if eval > maxEval:
                    finalMove = i
                    maxEval = eval
            return moves[finalMove]

        else:
            minEval = math.inf 
            finalMove = 0
            for i, action in enumerate(moves):
                newState = state.applyMoveCloning(action)
                eval = self.minimaxPrunning(newState, -math.inf, math.inf, self.depth)
                if eval < minEval:
                    finalMove = i
                    minEval = eval
            return moves[finalMove]

    def minimaxPrunning(self, state, alpha, beta, depth):
        if depth == 0 or state.game_over():
            return state.score()

        if state.nextPlayerToMove == 0:
            maxEval = -math.inf 
            moves = state.generateMoves()
            for action in moves: 
                newState = state.applyMoveCloning(action)
                eval = self.minimaxPrunning(newState, alpha, beta, depth-1)
                maxEval = max(eval, maxEval)
                alpha = max(eval, alpha)
                if alpha >= beta:
                    break
            return maxEval 
        
        else:
            minEval = math.inf 
            moves = state.generateMoves()
            for action in moves: 
                newState = state.applyMoveCloning(action)
                eval = self.minimaxPrunning(newState, alpha, beta, depth-1)
                minEval = min(eval, minEval)
                beta = min(eval, beta)
                if alpha >= beta:
                    break
            return minEval