import math
import random

from BaseAI_3 import BaseAI


class PlayerAI(BaseAI):
    
    def __init__(self):
        self.last_move = None

    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        max_score = grid.getMaxTile()
        best_move = moves[0]
        best_score = -math.inf
        # if self.last_move == 2 and 3 in moves:
        #     self.last_move = 3
        #     return moves[moves.index(3)]
        # elif self.last_move == 0 and 1 in moves:
        #     self.last_move = 1
        #     return moves[moves.index(1)]
        # elif 1 in moves and 3 in moves:
        #     self.last_move = random.choice([1, 3])
        #     return moves[moves.index(self.last_move)]
        # elif 1 in moves:
        #     self.last_move = 1
        #     return moves[moves.index(1)]
        # elif 3 in moves:
        #     self.last_move = 3
        #     return moves[moves.index(3)]
        # else:
        #     self.last_move = moves[0]
        #     return moves[0]
        
        if len(moves) > 0:
            for move in moves:
                board_copy = grid.clone()
                move_score = self.minimax(
                    board_copy, 2, False, moves)
                if move_score > best_score:
                    best_score = float(move_score)
                    best_move = moves[moves.index(move)]
        else:
            return None
        print(best_score)
        return best_move

    def gravitateScore(self, grid):
        score = 0
        if 1 in grid.getAvailableMoves():
            score += 1
        if 3 in grid.getAvailableMoves():
            score += 1
        return score

    def getMaxTilePosition(self, grid):
        lat, lon = 0, 0
        maxTile = 0
        currentMaxTile = 0
        for x in range(grid.size):
            for y in range(grid.size):
                maxTile = max(maxTile, grid.map[x][y])
                if maxTile > currentMaxTile:
                    currentMaxTile = maxTile
                    lat, lon = y, x
        return lat, lon

    def minimax(self, grid, depth, maximizingPlayer, available_moves):
        if depth == 0:
            return self.heuristic(grid)
        elif len(available_moves) == 0:
            return 0

        if maximizingPlayer:
            bestValue = -math.inf
            for move in available_moves:
                new_grid = grid.clone()
                new_grid.move(move)
                val = self.minimax(
                    new_grid, depth - 1, False, new_grid.getAvailableMoves())
                if val > bestValue:
                    bestValue = val
            return bestValue
        else:
            bestValue = math.inf
            for move in available_moves:
                new_grid = grid.clone()
                new_grid.move(move)
                val = self.minimax(
                    new_grid, depth - 1, True, new_grid.getAvailableMoves())
                if val < bestValue:
                    bestValue = val
            return bestValue

    def heuristic(self, grid):
        actual_score = grid.getMaxTile()
        numberOfEmptyCells = len(grid.getAvailableCells())
        clusteringScore = self.calculateClusteringScore(grid, actual_score)
        smoothness_score = self.measureBoardSmoothness(grid)
        gravity_score = self.gravitateScore(grid)
        max_tile_x, max_tile_y = self.getMaxTilePosition(grid)
        max_tile_edge_distance = self.getMaxTileDistanceFromEdge(
            grid, [max_tile_x, max_tile_y]
        )
        score = float(max_tile_edge_distance)
        return gravity_score

    def calculateClusteringScore(self, grid, max_tile):
        max_x, max_y = self.getMaxTilePosition(grid)
        horizontal_score = 0
        vertical_score = 0
        for x in range(grid.size):
            horizontal_score += grid.getCellValue([x, max_y])
        for y in range(grid.size):
            vertical_score += grid.getCellValue([max_x, y])
        return horizontal_score + vertical_score

    def getMaxTileDistanceFromEdge(self, grid, max_tile_position):
        x_distance = (max_tile_position[0] - 0)**2
        y_distance = (max_tile_position[1] - 0)**2
        return float(math.sqrt(x_distance + y_distance))

    def measureBoardSmoothness(self, grid):
        smoothness = 0
        for y in range(grid.size-1):
            if grid.map[0][y+1] < grid.map[0][y]:
                smoothness += 1
        for x in range(grid.size-1):
            if grid.map[x+1][0] < grid.map[x][0]:
                smoothness += 1
        return smoothness

