import numpy as np
import random
import timeit
import time

class Hashing:
    def __init__(self):
        self.zobrist_table = {}
        """Generate a unique 64-bit random number for each (piece, position) combination."""
        pieces = ["b_pawn", "b_knight", "b_bishop", "b_rook", "b_queen", "b_king",
                  "w_pawn", "w_knight", "w_bishop", "w_rook", "w_queen", "w_king"]

        for piece in pieces:
            for y in range(8):
                for x in range(8):# 8x8 board
                    self.zobrist_table[(piece, (y,x))] =  random.randint(-1000000, 10000000000)
                    
    def compute_board_hash(self, piece_name, square_id):
            return self.zobrist_table[(piece_name, square_id)]  
        
def hash(board):
    return board.tobytes()


if __name__ == "__main__":
    hashing = Hashing()
    
to_move = (6,4)
piece = "b_pawn"

# execution_time = timeit.timeit(lambda: hashing.compute_board_hash( piece, (6,7)), number=100000)
# print(f"Execution time: {execution_time} seconds")



    
    





