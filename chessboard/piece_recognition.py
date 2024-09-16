import numpy as np




class Chessboard:
    def __init__(self):
        # Initialize the chessboard: first two and last two rows filled with 1, rest with 0
        self.board = [
            [1]*8, [1]*8, [0]*8, [0]*8, [0]*8, [0]*8, [1]*8, [1]*8
        ]
        # Store history of positions
        self.history = [np.array(self.board)]

    def printBoard(self):
        # Print the board in a readable format
        print(self.board)
        return
    def get_current_board(self):
        return self.board
    def stand_by(self):
        while True:
            return

    def save_position(self):
        # Append the current position to history
        self.history.append(np.array(self.board))
    
    def get_history(self):
        return self.history
#chess = Chessboard(dummy=True)
#print(chess.get_current_board())
#chess.save_position()
#print(chess.get_history())
chess = Chessboard()
chess.printBoard()
