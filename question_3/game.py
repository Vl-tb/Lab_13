"""
This is main module of x o game.
"""

from board import Board
from blessed import Terminal

def game():
    """
    This is the main function, which starts the game.
    """
    terminal = Terminal()
    board = Board()
    while board.get_status() == "continue":
        move = status(board, terminal)
        try:
            move_checker(board, move)
            board.make_move(move, "x")
            print("/"*terminal.width)
            print()
            print(board)
            print()
            if board.get_status() != "continue":
                break
            board.make_computer_move()
            board.counter_left = 0
            board.counter_right = 0
        except ValueError:
            print("This move is not allowed!")
            print()
    if board.get_status() == "x":
        print("Congrats! You win")
    elif board.get_status() == "0":
        print("Unfortunately, you lose!")
    else:
        print("Oh, it's a draw!")
    return
    

def status(board, terminal):
    """
    This function print current status of the board and
    returns player's move.
    """
    print("/"*terminal.width)
    print()
    print(board)
    print()
    coords = input("Enter your move (row, column):")
    try:
        move = (int(coords[1]), int(coords[4]))
    except ValueError:
        move = ("-", "-")
    return move


def move_checker(board, move):
    """
    This function checks if move is allowed.
    """
    if move not in board.empty:
        raise ValueError

if __name__ == "__main__":
    game()
