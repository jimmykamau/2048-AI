import itertools
import math
import random


from BaseAI_3 import BaseAI
 
class PlayerAI(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        max_score = grid.getMaxTile()
        best_move = moves[0]
        best_score = -math.inf
        if len(moves) > 0:
            for move in moves:
                board_copy = grid.clone()
                board_copy.move(move)
                move_score = self.expectimax(board_copy, 7)
                if move_score > best_score:
                    best_score = float(move_score)
                    best_move = moves[moves.index(move)]
        else:
            return None
        return best_move

    def expectimax(self, grid, depth, move=False):
        if depth == 0:
            return self.heuristic(grid)
        
        alpha = self.heuristic(grid)

        if move:
            for available_move in grid.getAvailableMoves():
                grid.move(move)
                alpha = max(alpha, self.expectimax(grid, depth-1))
        else:
            alpha = 0
            zeros = self.getZeros(grid)
            for i, j in zeros:
                c1 = c2 = grid.clone()
                c1.map[i][j] = 2
                c2.map[i][j] = 4
                alpha += (.1*self.expectimax(c1, depth-1, True)/len(zeros)) + (.9*self.expectimax(c2, depth-1, True)/len(zeros))
        return alpha

    def heuristic(self, grid):
        if not grid.canMove():
            return -math.inf
        snake = []
        for i, col in enumerate(zip(*grid.map)):
            snake.extend(reversed(col) if i % 2 == 0 else col)
        m = max(snake)
        heuristic_sum = sum(x/10**n for n, x in enumerate(snake)) - \
            math.pow((grid.map[grid.size-1][0] != m)*abs(grid.map[grid.size-1][0] - m), 2)
        return heuristic_sum
    
    def getZeros(self, grid):
        zeros = []
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] == 0:
                    zeros.append((x, y))
        return zeros 
        