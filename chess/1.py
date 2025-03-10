import tkinter
import numpy as np
import time
import math
from copy import deepcopy
from random import randint
import hashlib

subor = open("text.txt", "w", encoding="utf8")


class View:
    def __init__(self):
        self.board = np.empty((8, 8), dtype='U10')
        self.square_size = 125
        
        self.clicked = False
        self.white_can_castle_left = True
        self.white_can_castle_right = True
        self.black_can_castle_left = True
        self.black_can_castle_right = True

        self.white_pieces_pos = [(y,x) for x in range(8) for y in range(6,8)]
        self.white_pawns_pos = [(6,x) for x in range(8)]
        self.white_rooks_pos = [(7,0), (7,7)]
        self.white_knights_pos = [(7,1), (7,6)]
        self.white_bishops_pos = [(7,2), (7,5)]
        self.white_queen_pos = [(7,3)]
        self.white_king_pos = [(7,4)]
        self.black_pieces_pos = [(y,x) for x in range(8) for y in range(0,2)]
        self.black_pawns_pos = [(1,x) for x in range(8)]
        self.black_rooks_pos = [(0,0), (0,7)]
        self.black_knights_pos = [(0,1), (0,6)]
        self.black_bishops_pos = [(0,2), (0,5)]
        self.black_queen_pos = [(0,3)]
        self.black_king_pos = [(0,4)]
        
        self.black_check = False
        self.white_check = False
        
        
        
        self.Update_Array()

        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=self.square_size * 8, height=self.square_size * 8)
        self.canvas.pack()
        
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        self.load_images()
        self.Draw_Board()
        self.Update_Board()
        
    def load_images(self):
        self.white_pawn = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/white-pawn.png")
        self.white_knight = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/white-knight.png")
        self.white_rook = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/white-rook.png")
        self.white_bishop = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/white-bishop.png")
        self.white_queen = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/white-queen.png")
        self.white_king = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/white-king.png")
        
        self.black_pawn = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/black-pawn.png")
        self.black_knight = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/black-knight.png")
        self.black_rook = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/black-rook.png")
        self.black_bishop = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/black-bishop.png")
        self.black_queen = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/black-queen.png")
        self.black_king = tkinter.PhotoImage(file="/Users/lukaskocman/programy/chess/pieces-basic-png/black-king.png")
        
    def Update_Board(self):
        self.Detect_pawn_promotions()
        self.Update_Array()
        
        self.canvas.delete("ball")
        
        self.Update_colour_all_positions()
        
        
        piece_type_dic = {       
            "w_pawn": self.white_pawn,
            "w_rook": self.white_rook,
            "w_knight": self.white_knight,
            "w_bishop": self.white_bishop,
            "w_queen": self.white_queen,
            "w_king": self.white_king,
            
            "b_pawn": self.black_pawn,
            "b_rook": self.black_rook,
            "b_knight": self.black_knight,
            "b_bishop": self.black_bishop,
            "b_queen": self.black_queen,
            "b_king": self.black_king
        }
        
        
        
        for i, piece in enumerate(self.board.flatten()):
            if piece != "":
                y = i // self.board.shape[0]
                x = i - y * self.board.shape[0]
                
                self.canvas.create_image(x * self.square_size+self.square_size/2,
                                        y * self.square_size+self.square_size/2,
                                        image=piece_type_dic[piece],
                                        tags = (f"({x},{y})", "ball"))
        self.canvas.update()
   
    def Detect_pawn_promotions(self):
        for i, coord in enumerate(self.white_pawns_pos):
            if coord[0] == 0:
                self.white_queen_pos.append(coord)
                del self.white_pawns_pos[i]
                
        for i, coord in enumerate(self.black_pawns_pos):
            if coord[0] == 7:
                self.black_queen_pos.append(coord)
                del self.black_pawns_pos[i]
   
    def Update_colour_all_positions(self):
        self.white_pieces_pos = []
        self.white_pieces_pos.extend(
            self.white_pawns_pos + self.white_rooks_pos + self.white_bishops_pos + 
            self.white_knights_pos + self.white_queen_pos + self.white_king_pos
        )        

        self.black_pieces_pos = []
        self.black_pieces_pos.extend(
            self.black_pawns_pos + self.black_rooks_pos + self.black_bishops_pos + 
            self.black_knights_pos + self.black_queen_pos + self.black_king_pos
        )   
   
    def Update_Array(self):
        self.board = np.empty((8, 8), dtype='U10')
        piece_positions = {
            "w_pawn": self.white_pawns_pos,
            "w_rook": self.white_rooks_pos,
            "w_knight": self.white_knights_pos,
            "w_bishop": self.white_bishops_pos,
            "w_queen": self.white_queen_pos,
            "w_king": self.white_king_pos,
            
            "b_pawn": self.black_pawns_pos,
            "b_rook": self.black_rooks_pos,
            "b_knight": self.black_knights_pos,
            "b_bishop": self.black_bishops_pos,
            "b_queen": self.black_queen_pos,
            "b_king": self.black_king_pos
        }
        
        
        

        for piece, pos in piece_positions.items():
            for coord  in pos:
                self.board[coord] = piece
                                  
    def Draw_Board(self):
        for x in range(self.board.shape[1]):
            for y in range(self.board.shape[0]):
                a = self.square_size
                
                self.canvas.create_rectangle(x * self.square_size + a,
                                             y * self.square_size + a,
                                             x * self.square_size,
                                             y * self.square_size,
                                             fill= "#e75480" if (x+y) % 2 == 1 else "Pink",
                                             outline = "Black",
                                             tags=f"{y},{x}")
                
    def on_click(self, event):
        self.clicked_x = event.x // self.square_size
        self.clicked_y = event.y // self.square_size
        self.clicked = True
        # self.Is_white_king_at_check()
        # self.Is_black_king_at_check() # doesnt work yet
        #  
        self.canvas.coords(f"({self.clicked_x},{self.clicked_y})", event.x,event.y)
        if (self.clicked_y, self.clicked_x) in self.white_pieces_pos:
            white(self.clicked_y, self.clicked_x, True)
            
        if (self.clicked_y, self.clicked_x) in self.black_pieces_pos:
            AI("black")            
            
    def on_release(self, event):
        self.release_x = event.x // self.square_size
        self.release_y = event.y // self.square_size
        
        self.clicked = False
        white(self.clicked_y, self.clicked_x, False)
        
        
        self.Update_Board()
        
    def on_mouse_move(self, event):
        if self.clicked == True:
            x = event.x
            y = event.y
            self.canvas.coords(f"({self.clicked_x},{self.clicked_y})", x,y)

    def Is_white_king_at_check(self):
        check_class = Check_check("white")
        self.white_check = check_class.Is_check    
        
    def Is_black_king_at_check(self):
        check_class = Check_check("black")
        self.black_check = check_class.Is_check
        
        

        
class AI:
    def __init__(self, parent):
        self.piece_positions_dic = {
            "w_pawn": view.white_pawns_pos,
            "w_rook": view.white_rooks_pos,
            "w_knight": view.white_knights_pos,
            "w_bishop": view.white_bishops_pos,
            "w_queen": view.white_queen_pos,
            "w_king": view.white_king_pos,
            
            "b_pawn": view.black_pawns_pos,
            "b_rook": view.black_rooks_pos,
            "b_knight": view.black_knights_pos,
            "b_bishop": view.black_bishops_pos,
            "b_queen": view.black_queen_pos,
            "b_king": view.black_king_pos
        }
        
        self.piece_weight_dic = {
            "w_pawn": -1,
            "w_rook": -5,
            "w_knight": -3.5,
            "w_bishop": -3,
            "w_queen": -9,
            "w_king": -100 if parent == "black" else -1000,
            
            "b_pawn": 1,
            "b_rook": 5,
            "b_knight": 3.5,
            "b_bishop": 3,
            "b_queen": 9,
            "b_king": 100 if parent == "white" else 1000,
        }
        
        self.Load_classes()
        
        self.piece_classes_dic = {
            "w_pawn": [self.white_pawn_class],
            "w_rook": [self.white_rook_class],
            "w_knight": [self.white_knight_class],
            "w_bishop": [self.white_bishop_class],
            "w_queen" : [self.white_rook_class, self.white_bishop_class],
            "w_king": [self.white_king_class],
            
            "b_pawn": [self.black_pawn_class],
            "b_rook": [self.black_rook_class],
            "b_knight": [self.black_knight_class],
            "b_bishop": [self.black_bishop_class],
            "b_queen" : [self.black_rook_class, self.black_bishop_class],
            "b_king": [self.black_king_class]
        }

        self.tranpositions_dic = {}

        
        start_time = time.time()
        self.evaluations = 0
        board_key = 0
        
        self.simulation_black_castle_left = view.black_can_castle_left
        self.simulation_black_castle_right = view.black_can_castle_right
        self.simulation_white_castle_left = view.white_can_castle_left
        self.simulation_white_castle_right = view.white_can_castle_right
        

        
        scores_info = self.Minimax(parent, 0, 5, view.board, -math.inf, math.inf, board_key)
 
        elapsed_time = time.time() - start_time
        print (elapsed_time, self.evaluations)
        print(self.evaluations/elapsed_time)
        
        
        # figures out the best move to make
        max_score = -math.inf if parent == "black" else math.inf
        piece_to_move_info = [] 
        for score in scores_info: # decides what move to do based on scores
            print(score)
            if (score[3] > max_score) if parent == "black" else (score[3] < max_score):
                piece_to_move_info = score[:3]
                max_score = score[3]
            elif score[3] == max_score:
                to_move_rand = randint(0,1)
                if to_move_rand == 1:
                    max_score = score[3]
                    piece_to_move_info = score[:3]
                    
        # castling check
        self.castling_logic(parent, piece_to_move_info) 
                    
                
        # do the move on the real board
        self.delet_if_captured_for_real(piece_to_move_info[2])    
        piece_positions = self.piece_positions_dic[piece_to_move_info[0]]
        piece_positions[piece_positions.index(piece_to_move_info[1])] = piece_to_move_info[2]
        view.Update_Board()

    def castling_logic(self, parent, piece_to_move_info):
        if parent == "white":            
            if view.white_can_castle_right == True: # castle right
                if piece_to_move_info[2] == (7,6): #coords for right castling
                    view.white_rooks_pos[view.white_rooks_pos.index((7, 7))] = (7,5) 
                    
            if view.white_can_castle_left == True: # castle left
                if piece_to_move_info[2] == (7,2): #coords for left castling
                    view.white_rooks_pos[view.white_rooks_pos.index((7, 0))] = (7,3) 
        elif parent == "black":            
            if view.black_can_castle_right == True: # castle right
                if piece_to_move_info[2] == (0,6): #coords for right castling
                    view.black_rooks_pos[view.black_rooks_pos.index((0, 7))] = (0,5) 
                    
            if view.black_can_castle_left == True: # castle left
                if piece_to_move_info[2] == (0,2): #coords for left castling
                    view.black_rooks_pos[view.black_rooks_pos.index((0, 0))] = (0,3)
        
        
        if parent == "white" and piece_to_move_info[0] == "w_king":
            view.white_can_castle_left, view.white_can_castle_right = False, False
        elif parent == "black" and piece_to_move_info[0] == "b_king":
            view.black_can_castle_left, view.black_can_castle_right = False, False
            
        if parent == "black":
            if piece_to_move_info[0] == "b_rook": # rooks check
                if piece_to_move_info[1] == (0,0): # left castling
                    view.black_can_castle_left = False
                elif piece_to_move_info[1] == (0,7): # right castling
                    view.black_can_castle_right = False
        elif parent == "white":
            if piece_to_move_info[0] == "w_rook": # rooks check
                if piece_to_move_info[1] == (7,0): # left castling
                    view.black_can_castle_left = False
                elif piece_to_move_info[1] == (7,7): # right castling
                    view.black_can_castle_right = False
                    
        

    def Load_classes(self):
        self.white_pawn_class = Pawns(0, 0, "white", True, False, "ai")
        self.white_knight_class = Knights(0, 0, "white", True, False, "ai")
        self.white_bishop_class = Bishops(0, 0, "white", True, False, "ai")
        self.white_rook_class = Rooks(0, 0, "white", True, False, "ai")
        self.white_king_class = King(0, 0, "white", True, False, "ai")
        
        self.black_pawn_class = Pawns(7, 7, "black", True, False, "ai")
        self.black_knight_class = Knights(7, 7, "black", True, False, "ai")
        self.black_bishop_class = Bishops(7, 7, "black", True, False, "ai")
        self.black_rook_class = Rooks(7, 7, "black", True, False, "ai")
        self.black_king_class = King(7, 7, "black", True, False, "ai")

        
        

    def Minimax(self, parent, current_depth, max_depth, board, alpha, beta, board_key):
        current_depth += 1
        scores = []
        
        
        for index, piece_name in enumerate(board.flatten()): # iterates over the whole board
            if piece_name != "" and piece_name[0] == parent[0]: # if the colour of the piece is same as the parent
                piece_start_pos = (index // board.shape[0], index - ((index // board.shape[0])*8)) # calculates the coords of the piece
                piece_classes = self.piece_classes_dic[piece_name] # gets the class instance of that piece for queen both of the classes
                valid_moves = []

                for piece_class in piece_classes:
                    valid_moves.extend(piece_class.Get_Valid_moves(piece_start_pos[0], piece_start_pos[1], board)) # gets the valid moves of that piece
            
                        
                for move_to_pos in valid_moves:
                    new_board = deepcopy(board)
                    
                    # check if the move is castling and if yes then move the rook
                    castling_info = []
                    if parent == "black":
                        if move_to_pos == (0,6) and piece_start_pos == (0,4): # castle right
                            if self.simulation_black_castle_right == True:
                                if new_board[0,7] == "b_rook":
                                    self.simulation_black_castle_right = False
                                    new_board[0,7] = ""
                                    new_board[0,5] = "b_rook"
                                    castling_info = [(0,7), (0,5), self.simulation_black_castle_right, "b_rook"]
                        if move_to_pos == (0,2) and piece_start_pos == (0,4): # castle left
                            if self.simulation_black_castle_left == True:
                                if new_board[0,0] == "b_rook":
                                    self.simulation_black_castle_right = False
                                    new_board[0,0] = ""
                                    new_board[0,3] = "b_rook"
                                    castling_info = [(0,0), (0,3), self.simulation_black_castle_left, "b_rook"]
                    if parent == "white":
                        if move_to_pos == (7,6) and piece_start_pos == (7,4): # castle right
                            if self.simulation_white_castle_right == True:
                                if new_board[7,7] == "w_rook":
                                    self.simulation_white_castle_right = False
                                    new_board[7,7] = ""
                                    new_board[7,5] = "w_rook"
                                    castling_info = [(7,7), (7,5), self.simulation_white_castle_right, "w_rook"]
                        if move_to_pos == (7,2) and piece_start_pos == (7,4): # castle left
                            if self.simulation_white_castle_left == True:
                                if new_board[7,0] == "w_rook":
                                    self.simulation_black_castle_right = False
                                    new_board[7,0] = ""
                                    new_board[7,3] = "w_rook"
                                    castling_info = [(7,0), (7,3), self.simulation_white_castle_left, "w_rook"]
                                
                    
                    # do the move
                    deleted_info = self.delete_if_captured(move_to_pos, new_board) # captures and stores the name and the coord where it captured
                    new_board[piece_start_pos] = ""
                    if move_to_pos[0] == (0 if parent == "white" else 7) and piece_name[2:] == "pawn": # promotion logic
                        new_board[move_to_pos] = f"{parent[0]}_queen" 
                    else:
                        new_board[move_to_pos] = piece_name


                    
                    board_key =  hashlib.sha256(new_board.tobytes() + current_depth.to_bytes(1, byteorder='little', signed=True)).hexdigest()
                    if current_depth == 1: 
                        scores.append([piece_name, piece_start_pos, move_to_pos, self.Minimax("white" if parent == "black" else "black", current_depth, max_depth, new_board, alpha, beta, board_key)]) 
                    elif board_key not in self.tranpositions_dic:
                        # evaluate
                        if current_depth != max_depth:
                            scores.append(self.Minimax("white" if parent == "black" else "black", current_depth, max_depth, new_board, alpha,  beta, board_key))
                        elif current_depth == max_depth:
                            scores.append(self.Evaluate(new_board))
                            
                        self.tranpositions_dic[board_key] = scores[-1]
                    else:
                        scores.append(self.tranpositions_dic[board_key])
                       
                        
                    # bubiiiik dance dd yellow hihihihihihi
                    # reverse the move
                    new_board[piece_start_pos] = piece_name
                    new_board[move_to_pos] = ""
                    if deleted_info != None:
                        new_board[deleted_info[1]] = deleted_info[0]
                        
                    # reverse the castling
                    if castling_info != []:
                        castling_info[2] = True
                        new_board[castling_info[0]] = castling_info[3]
                        new_board[castling_info[1]] = ""
                        
                    if parent == "black" and current_depth != 1:
                        alpha = max(alpha, max(scores))
                    elif parent == "white" and current_depth != 1:
                        beta = min(beta, min(scores))

                        
                    if beta <= alpha:
                        break
                        
        if current_depth == 1:
            return scores
        else:

            return max(scores) if parent == "black" else min(scores)
            
                
                        
        
    def Evaluate(self, board):
        score = 0
        self.evaluations+=1
        for piece in board.flatten():
            if piece != "":
                score += self.piece_weight_dic[piece]
            
        return (score)
                
    def delete_if_captured(self, coord, board):
        if board[coord] != "":
            deleted_info = [board[coord], coord]
            board[coord] = ""
            return deleted_info
        return None

    def delet_if_captured_for_real(self, move_to):
        to_capture_positions = self.Get_captured_type(move_to[0], move_to[1])
        if to_capture_positions:
            del to_capture_positions[to_capture_positions.index(move_to)]
        
    def Get_captured_type(self, release_y, release_x):
        pieces_pos = [
            view.black_pawns_pos,
            view.black_rooks_pos,
            view.black_knights_pos,
            view.black_bishops_pos,
            view.black_queen_pos,
            view.black_king_pos,
            view.white_pawns_pos,
            view.white_rooks_pos,
            view.white_knights_pos,
            view.white_bishops_pos,
            view.white_queen_pos,
            view.white_king_pos
        ]
        
        for pos in pieces_pos:
            if (release_y, release_x) in pos:
                return pos
        return None
    
    
    
class white:
    def __init__(self, clicked_y, clicked_x, clicked):
        
        if (clicked_y,clicked_x) in view.white_pawns_pos:
            self.pawns(clicked_y, clicked_x, clicked)
        
        elif (clicked_y, clicked_x) in view.white_knights_pos:
            self.knights(clicked_y, clicked_x, clicked)     
            
        elif (clicked_y, clicked_x) in view.white_bishops_pos:
            self.bishops(clicked_y, clicked_x, clicked)         
            
        elif (clicked_y, clicked_x) in view.white_rooks_pos:
            self.rooks(clicked_y, clicked_x, clicked)
            
        elif (clicked_y, clicked_x) in view.white_queen_pos:
            self.queen(clicked_y, clicked_x, clicked)         
                        
        elif (clicked_y, clicked_x) in view.white_king_pos:
            self.king(clicked_y, clicked_x, clicked)  
            
                            
        


    def pawns(self, clicked_y, clicked_x, clicked):
        if clicked == True:
            Pawns(clicked_y,clicked_x, "white", clicked, True, "white")
        
        if clicked == False:
            pawns_class = Pawns(clicked_y, clicked_x, "white", clicked, True, "white")
            valid_moves = pawns_class.Get_Valid_moves(clicked_y, clicked_x, view.board)
            if (view.release_y, view.release_x) in valid_moves:
                view.white_pawns_pos[view.white_pawns_pos.index((clicked_y, clicked_x))] = (view.release_y, view.release_x)
                self.Delete_if_captured()
                        
    def knights(self, clicked_y, clicked_x, clicked):
        if clicked == True:
            Knights(clicked_y,clicked_x, "white", clicked, True, "white")
            
        if clicked == False:
            knights_class = Knights(clicked_y, clicked_x, "white", clicked, True, "white")
            valid_moves = knights_class.Get_Valid_moves(clicked_y, clicked_x, view.board)
            if (view.release_y, view.release_x) in valid_moves:
                view.white_knights_pos[view.white_knights_pos.index((clicked_y, clicked_x))] = (view.release_y, view.release_x)
                self.Delete_if_captured()
                
    def bishops(self, clicked_y, clicked_x, clicked):
        if clicked == True:
            Bishops(clicked_y,clicked_x, "white", clicked, True, "white")
            
        if clicked == False:
            bishops_class = Bishops(clicked_y, clicked_x, "white", clicked, True, "white")
            valid_moves = bishops_class.Get_Valid_moves(clicked_y, clicked_x, view.board)
            if (view.release_y, view.release_x) in valid_moves:
                view.white_bishops_pos[view.white_bishops_pos.index((clicked_y, clicked_x))] = (view.release_y, view.release_x)
                self.Delete_if_captured()

    def rooks(self, clicked_y, clicked_x, clicked):
        if clicked == True:
            Rooks(clicked_y,clicked_x, "white", clicked, True, "white")
            
        if clicked == False:
            rooks_class = Rooks(clicked_y, clicked_x, "white", clicked, True, "white")
            valid_moves = rooks_class.Get_Valid_moves(clicked_y, clicked_x, view.board)
            if (view.release_y, view.release_x) in valid_moves:
                
                # if moved from orig coords cannot castle
                if (clicked_y, clicked_x) == (7,0): #left rook start pos
                    view.white_can_castle_left = False
                elif (clicked_y, clicked_x) == (7,7): #right rook start pos
                    view.white_can_castle_right = False
                
                view.white_rooks_pos[view.white_rooks_pos.index((clicked_y, clicked_x))] = (view.release_y, view.release_x)
                self.Delete_if_captured()              
                
    def queen(self, clicked_y, clicked_x, clicked):
        if clicked == True:
            Rooks(clicked_y,clicked_x, "white", clicked, True, "white")
            Bishops(clicked_y,clicked_x, "white", clicked, True, "white")
            
        if clicked == False:
            rooks_class = Rooks(clicked_y, clicked_x, "white", clicked, True, "white")
            bishops_class = Bishops(clicked_y, clicked_x, "white", clicked, True, "white")
            
            valid_moves = bishops_class.Get_Valid_moves(clicked_y, clicked_x, view.board)
            valid_moves.extend(rooks_class.Get_Valid_moves(clicked_y, clicked_x, view.board))
            
            if (view.release_y, view.release_x) in valid_moves:
                view.white_queen_pos[view.white_queen_pos.index((clicked_y, clicked_x))] = (view.release_y, view.release_x)
                self.Delete_if_captured()

    def king(self, clicked_y, clicked_x, clicked):
        if clicked == True:
            King(clicked_y,clicked_x, "white", clicked, True, "white")
            
        if clicked == False:
            king_class = King(clicked_y, clicked_x, "white", clicked, True, "white")
            valid_moves = king_class.Get_Valid_moves(clicked_y, clicked_x, view.board)
            if (view.release_y, view.release_x) in valid_moves:
                
                view.white_king_pos[view.white_king_pos.index((clicked_y, clicked_x))] = (view.release_y, view.release_x)
                self.Delete_if_captured()
                
                # castling logic
                if view.white_can_castle_right == True: # castle right
                    if (view.release_y, view.release_x) == (7,6): #coords for right castling
                        view.white_rooks_pos[view.white_rooks_pos.index((7, 7))] = (7,5) 
                        
                if view.white_can_castle_left == True: # castle left
                    if (view.release_y, view.release_x) == (7,2): #coords for left castling
                        view.white_rooks_pos[view.white_rooks_pos.index((7, 0))] = (7,3) 
                        
                # when moved cannot castle anymore
                view.white_can_castle_left = False
                view.white_can_castle_right = False
                


    def Delete_if_captured(self):
        if (view.release_y, view.release_x) in view.black_pieces_pos:
            piece_to_capture = self.Get_captured_type(view.release_y, view.release_x)
            del piece_to_capture[piece_to_capture.index((view.release_y, view.release_x))]
    
    def Get_captured_type(self, release_y, release_x):
        pieces_pos = [
            view.black_pawns_pos,
            view.black_rooks_pos,
            view.black_knights_pos,
            view.black_bishops_pos,
            view.black_queen_pos,
            view.black_king_pos
        ]
        
        for pos in pieces_pos:
            if (release_y, release_x) in pos:
                return pos
        
        
        
        

class Pawns:
    def __init__(self, clicked_y, clicked_x, parent, clicked, to_highlight, called_from):
        self.to_highlight = to_highlight
        self.is_at_start = False
        self.clicked = clicked
        self.view = view
        self.parent = parent
        self.called_from = called_from
        self.oposite_colour = "w" if parent == "black" else "b"
        
        if parent == "white":
            self.direction = -1
            if clicked_y == 6 and parent == "white":
                self.is_at_start = True

        else:
            self.direction = 1
            if clicked_y == 1 and parent == "black":
                self.is_at_start = True
                
        self.valid_moves = self.Get_Valid_moves(clicked_y, clicked_x, view.board)
        if self.to_highlight == True:
            self.Highlight_squares(clicked_y, clicked_x)  
            
                  
    
    def Highlight_squares(self, clicked_y, clicked_x):
        for x in range(self.view.board.shape[1]):
            for y in range(self.view.board.shape[0]):
                if (y,x) in self.valid_moves:
                    self.view.canvas.itemconfig(f"{y},{x}", fill = "#FF6666" if self.clicked == True else "#e75480" if (x+y) % 2 == 1 else "Pink")

    def Get_Valid_moves(self, clicked_y, clicked_x, board):
        valid_moves = []
        if (self.parent == "black" and clicked_y == 1):
            self.is_at_start = True
        elif (self.parent == "white" and clicked_y == 6):
            self.is_at_start = True
        else:
            self.is_at_start = False
        
        # forward movement 
        to_move_front_coord = clicked_y + self.direction
        if 0 <= to_move_front_coord < 8:
            is_front_square_empty = (board[to_move_front_coord, clicked_x] == "")
            if is_front_square_empty:
                valid_moves.append((to_move_front_coord, clicked_x))
                if self.is_at_start == True:
                    if board[to_move_front_coord + self.direction, clicked_x] == "":
                        valid_moves.append((to_move_front_coord + self.direction, clicked_x))
            
                
        # capturing
        for dir in [-1, 1]:
            to_move_side_coord = clicked_x + dir
            if 0 <= to_move_side_coord < board.shape[1] and 0 <= to_move_front_coord < 8:
                if board[to_move_front_coord, to_move_side_coord] != "" and  board[to_move_front_coord, to_move_side_coord][0] == self.oposite_colour:
                    valid_moves.append((to_move_front_coord, to_move_side_coord))
                    
        # adjust valid_moves so that if the king is in check it cannot move somewhere where he remains in check
        if self.called_from != "check_class":
            if (view.white_check if self.parent == "white" else view.black_check) == True: 
                filtered_valid_moves = []
                Check_class = Check_check(self.parent)
                checks_coords = Check_class.to_inerupt_check_coords
                checks_coords = set(checks_coords)
                filtered_valid_moves = [coord for coord in valid_moves if coord in checks_coords]
                
                return filtered_valid_moves
                    
        return valid_moves
    
          
class Knights:
    def __init__(self, clicked_y, clicked_x, parent, clicked, to_highlight, called_from):
        self.to_highlight = to_highlight
        self.clicked = clicked
        self.view = view
        self.called_from = called_from
        self.parent = parent
        self.oposite_colour = "w" if parent == "black" else "b"
        self.knight_dir = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        self.Highlight_squares(clicked_y, clicked_x)            
    
    def Highlight_squares(self, clicked_y, clicked_x):
        valid_moves = self.Get_Valid_moves(clicked_y, clicked_x, view.board)
        
        if self.to_highlight == True:
            for x in range(self.view.board.shape[1]):
                for y in range(self.view.board.shape[0]):
                    if (y,x) in valid_moves:
                        self.view.canvas.itemconfig(f"{y},{x}", fill = "#FF6666" if self.clicked == True else "#e75480" if (x+y) % 2 == 1 else "Pink")

    def Get_Valid_moves(self, clicked_y, clicked_x, board):
        valid_moves = []
        
        for dy, dx in self.knight_dir:
            y = clicked_y - dy
            x = clicked_x - dx
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                move_to_piece_name = board[y, x]
                if move_to_piece_name == "" or move_to_piece_name[0] == self.oposite_colour:
                    valid_moves.append((y, x))
                
                
        # adjust valid_moves so that if the king is in check it cannot move somewhere where he remains in check
        if self.called_from != "check_class":
            if (view.white_check if self.parent == "white" else view.black_check) == True: 
                filtered_valid_moves = []
                Check_class = Check_check(self.parent)
                checks_coords = Check_class.to_inerupt_check_coords
                checks_coords = set(checks_coords)
                filtered_valid_moves = [coord for coord in valid_moves if coord in checks_coords]
                
                return filtered_valid_moves

        return valid_moves 
    
      
class Bishops:
    def __init__(self, clicked_y, clicked_x, parent, clicked, to_highlight, called_from):
        self.to_highlight = to_highlight
        self.clicked = clicked
        self.view = view
        self.parent = parent
        self.called_from = called_from
        self.oposite_colour = "w" if parent == "black" else "b"
        self.colour = "b" if parent == "black" else "w"
        
        self.Highlight_squares(clicked_y, clicked_x)            

    def Highlight_squares(self, clicked_y, clicked_x):
        valid_moves = self.Get_Valid_moves(clicked_y, clicked_x, view.board)
        
        if self.to_highlight == True:
            for x in range(self.view.board.shape[1]):
                for y in range(self.view.board.shape[0]):
                    if (y,x) in valid_moves:
                        self.view.canvas.itemconfig(f"{y},{x}", fill = "#FF6666" if self.clicked == True else "#e75480" if (x+y) % 2 == 1 else "Pink")

    def Get_Valid_moves(self, clicked_y, clicked_x, board):
        valid_moves = []
        
        for a in range(1, 8): # up left
            y = clicked_y - a
            x = clicked_x - a
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                if board[y, x] == "":
                    valid_moves.append((y, x))
                elif board[y, x][0] == self.colour:
                    break
                elif board[y, x][0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    break
                
        for a in range(1, 8): # up right
            y = clicked_y - a
            x = clicked_x + a
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                if board[y, x] == "":
                    valid_moves.append((y, x))
                elif board[y, x][0] == self.colour:
                    break
                elif board[y, x][0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    break
                
        for a in range(1, 8): # down left
            y = clicked_y + a
            x = clicked_x - a
            
            if 0 <= y < view.board.shape[0] and 0 <= x < view.board.shape[1]:
                if view.board[y, x] == "":
                    valid_moves.append((y, x))
                elif view.board[y, x][0] == self.colour:
                    break
                elif view.board[y, x][0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    break
                
        for a in range(1, 8): # down right
            y = clicked_y + a
            x = clicked_x + a
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                if board[y, x] == "":
                    valid_moves.append((y, x))
                elif board[y, x][0] == self.colour:
                    break
                elif board[y, x][0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    break


        return valid_moves   
           
        
class Rooks:
    def __init__(self, clicked_y, clicked_x, parent, clicked, to_highlight, called_from):
        self.to_highlight = to_highlight
        self.clicked = clicked
        self.view = view
        self.parent = parent
        self.called_from = called_from
        self.oposite_colour = "w" if parent == "black" else "b"
        self.colour = "b" if parent == "black" else "w"
        self.Highlight_squares(clicked_y, clicked_x)            

    def Highlight_squares(self, clicked_y, clicked_x):
        valid_moves = self.Get_Valid_moves(clicked_y, clicked_x, view.board)
        
        if self.to_highlight == True:
            for x in range(self.view.board.shape[1]):
                for y in range(self.view.board.shape[0]):
                    if (y,x) in valid_moves:
                        self.view.canvas.itemconfig(f"{y},{x}", fill = "#FF6666" if self.clicked == True else "#e75480" if (x+y) % 2 == 1 else "Pink")

    def Get_Valid_moves(self, clicked_y, clicked_x, board):
        valid_moves = []
        
        for a in range(1, clicked_y + 1): # up 
            y = clicked_y - a
            x = clicked_x 
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                to_move_piece_name = board[y, x]
                if to_move_piece_name == "":
                    valid_moves.append((y, x))
                elif to_move_piece_name[0] == self.colour:
                    break
                elif to_move_piece_name[0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    break
                
        for a in range(1, 9-clicked_x): # right
            y = clicked_y 
            x = clicked_x + a
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                to_move_piece_name = board[y, x]
                if to_move_piece_name == "":
                    valid_moves.append((y, x))
                elif to_move_piece_name[0] == self.colour:
                    break
                elif to_move_piece_name[0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    break
                
        for a in range(1, 9-clicked_y): # down
            y = clicked_y + a
            x = clicked_x 
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                to_move_piece_name = board[y, x]
                if to_move_piece_name == "":
                    valid_moves.append((y, x))
                elif to_move_piece_name[0] == self.colour:
                    break
                elif to_move_piece_name[0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    break
                
        for a in range(1, clicked_x+1): # left
            y = clicked_y
            x = clicked_x - a
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                to_move_piece_name = board[y, x]
                if to_move_piece_name == "":
                    valid_moves.append((y, x))
                elif to_move_piece_name[0] == self.colour:
                    break
                elif to_move_piece_name[0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    break

        return valid_moves   
               
        
class King:
    def __init__(self, clicked_y, clicked_x, parent, clicked, to_highlight, called_from):
        self.to_highlight = to_highlight
        self.clicked = clicked
        self.view = view
        self.parent = parent
        self.called_from = called_from
        self.oposite_colour = "w" if parent == "black" else "b"
        
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        
        self.Highlight_squares(clicked_y, clicked_x)            
    
    def Highlight_squares(self, clicked_y, clicked_x):
        valid_moves = self.Get_Valid_moves(clicked_y, clicked_x, view.board)
        
        if self.to_highlight == True:
            for x in range(self.view.board.shape[1]):
                for y in range(self.view.board.shape[0]):
                    if (y,x) in valid_moves:
                        self.view.canvas.itemconfig(f"{y},{x}", fill = "#FF6666" if self.clicked == True else "#e75480" if (x+y) % 2 == 1 else "Pink")

    def Get_Valid_moves(self, clicked_y, clicked_x, board):
        valid_moves = []
        
        for dir in self.directions:
            y = clicked_y - dir[0]
            x = clicked_x - dir[1]
            
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                if board[y, x] == "":
                    valid_moves.append((y, x))
                elif board[y, x][0] == self.oposite_colour:
                    valid_moves.append((y, x))
                    
        # castling check
        if self.parent == "white":
            if view.white_can_castle_right == True and np.all(board[7, 5:7] == ""):
                valid_moves.append((7,6))
            if view.white_can_castle_left == True and np.all(board[7, 1:4] == ""):
                valid_moves.append((7,2))
        elif self.parent == "black":
            if view.black_can_castle_right == True and np.all(board[0, 5:7] == ""):
                valid_moves.append((0,6))
            if view.black_can_castle_left == True and np.all(board[0, 1:4] == ""):
                valid_moves.append((0,2))
             
                

        return valid_moves
    
    
    
    
    
class Check_check:
    def __init__(self, color):
        self.Is_check = False
        self.to_inerupt_check_coords = []
        self.pieces_prevent_check_pos = []
        self.color = color
        
        
        self.king_pos = view.white_king_pos[0] if color == "white" else view.black_king_pos[0]
        self.oposite_colour_pieces_pos = view.black_pieces_pos if color == "white" else view.white_pieces_pos
        
        
        self.find_check_pos()
        
    def find_check_pos(self):
        directions = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
        piece_classes_dictionary = {
            "pawn": [Pawns],
            "rook": [Rooks],
            "knight": [Knights],
            "bishop": [Bishops],
            "queen" : [Rooks, Bishops],
            "king": [King]
        }
     
        for coord in self.oposite_colour_pieces_pos: 
            
            # findig moves that each piece of the oposite colour can take
            valid_moves = []
            piece_name = view.board[coord][2:] # gets the nem of the piece
            piece_classes = piece_classes_dictionary[piece_name] # gets the class for the piece and for the queen the rook and bishop classes
            for piece_class in piece_classes: # this is here because queen is the mix of rook and bishop
                piece_instance = piece_class(coord[0], coord[1], "black" if self.color == "white" else "white", True, False, "check_class") # false for not coloring the sqares
                valid_moves += piece_instance.Get_Valid_moves(coord[0], coord[1], view.board)
        
                
            #checking if any of that positions are the same as kings (Check)
            if self.king_pos in valid_moves:
                self.Is_check = True
                
                middle_coord = ()
                
                if piece_name != "pawn":
                    for dir in directions:
                        middle_coord = tuple(num1 + num2 for num1, num2 in zip(self.king_pos, dir)) 
                        if middle_coord in valid_moves: 
                            a = 0
                            self.to_inerupt_check_coords += [(middle_coord[0] + dir[0] * a, middle_coord[1] + dir[1] * a)] # adds the first square
                            while (middle_coord[0] + dir[0] * a, middle_coord[1] + dir[1] * a) != coord:
                                a += 1
                                self.to_inerupt_check_coords += [(middle_coord[0] + dir[0] * a, middle_coord[1] + dir[1] * a)]
                else:
                     self.to_inerupt_check_coords += [coord]
                                
            else:
                continue
                
            
    

           
if __name__ == "__main__":
    view = View()

    view.root.mainloop()


