from random import randint
from BaseAI_3 import BaseAI
 
class PlayerAI(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        return moves[1] if moves else None