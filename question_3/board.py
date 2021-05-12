"""
This module contains ADT Board.
"""

from btree import LinkedBinaryTree
from btnode import BSTNode
from copy import deepcopy

class Board:
    """
    This class represents 3x3 board for
    x o game.
    """
    def __init__(self):
        self.last = None
        self.board = []
        self.empty = []
        self.counter_left = 0
        self.counter_right = 0
        for i in range(3):
            row = []
            for j in range(3):
                row.append("' '")
                self.empty.append((i, j))
            self.board.append(row)

    def __str__(self):
        output = ''
        for i in range(3):
            output += '['
            for j in range(3):
                if self.board[i][j] != "' '":
                    output += f"\'{self.board[i][j]}\'" + ', '
                else:
                    output += self.board[i][j] + ', '
            output = output[:-2] +']' + "\n"
        output = output[:-1]
        return output

    def get_status(self):
        """
        This method checks the status of this board.
        """
        def column_check(board, num):
            """
            This function checks if there is 3 signs in
            the same column.
            """
            if (board[0][num] == board[1][num] and
                board[2][num] == board[0][num] and
                board[0][num] != "' '"):
                return board[0][num]
            return 0

        def row_check(board, num):
            """
            This function checks if there is 3 signs in
            the same row.
            """
            if (board[num][0] == board[num][1] and
                board[num][2] == board[num][0] and
                board[num][0] != "' '"):
                return board[num][0]
            return 0

        def diagonal_check(board):
            """
            This function checks if there is 3 signs in
            the same diagonal.
            """
            if (board[0][0] == board[1][1] and
                board[2][2] == board[0][0] and
                board[0][0] != "' '"):
                return board[0][0]
            elif (board[0][2] == board[1][1] and
                board[0][2] == board[2][0] and
                board[0][2] != "' '"):
                return board[0][2]
            return 0

        check_diag = diagonal_check(self.board)
        if check_diag:
            return check_diag
        for index in range(3):
            check_col = column_check(self.board, index)
            check_row = row_check(self.board, index)
            if check_col:
                return check_col
            if check_row:
                return check_row
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "' '":
                    return "continue"
        return "draw"

    def make_move(self, position, turn):
        """
        This method changes the board by editing it.
        """
        if turn != "x" and turn != "0":
            raise IndexError
        try:
            self.board[position[0]][position[1]] = turn
            self.empty.remove(position)
            self.last = (turn, position)
            return self
        except IndexError & ValueError:
            raise IndexError


    def tree_creating(self):
        """
        This method creates binary tree of
        possible game variants.
        """
        tree = LinkedBinaryTree()
        tree.key = BSTNode(self)

        def recurse(node, last_sign="x"):
            """
            Recursive function for creating the tree.
            """
            move = ["x", "0"]
            move.remove(last_sign)
            next_sign = move[0]
            new_node_l = 0
            new_node_r = 0
            if node.key.data.empty != []:
                new_node_l = deepcopy(node)
                new_node_l.key.data.make_move(new_node_l.key.data.empty[0], next_sign)
                node.left_child = new_node_l
            if len(node.key.data.empty) > 1:
                new_node_r = deepcopy(node)
                new_node_r.key.data.make_move(new_node_r.key.data.empty[1], next_sign)
                node.right_child = new_node_r
            if new_node_l and new_node_l.key.data.get_status() == "continue":
                recurse(new_node_l, next_sign)
            if new_node_r and new_node_r.key.data.get_status() == "continue":
                recurse(new_node_r, next_sign)

        recurse(tree)
        return tree

    def move_counter(self, tree):
        """
        This method counts win/lose for each branch.
        """
        base_l = tree.left_child
        base_r = tree.right_child
        self.inorder(base_l, "l")
        self.inorder(base_r, "r")
        return (self.counter_left, self.counter_right)

    def inorder(self, tree, direction):
        """
        This method helps to count win/lose for
        branches. Actually, it's modified inorder() function
        for binary tree.
        """
        if tree.left_child:
            self.inorder(tree.left_child, direction)
        if tree.key.data.get_status() == '0':
            if direction == "l":
                self.counter_left += 1
            else:
                self.counter_right += 1
        if tree.key.data.get_status() == 'x':
            if direction == "l":
                self.counter_left -= 1
            else:
                self.counter_right -= 1
        if tree.right_child:
            self.inorder(tree.right_child, direction)
        return
    
    def make_computer_move(self):
        """
        This method changes the board by computer move.
        """
        result_tree = self.tree_creating()
        win_lose = self.move_counter(result_tree)
        if win_lose[0] >= win_lose[1]:
            self.make_move(self.empty[0], "0")
        else:
            self.make_move(self.empty[1], "0")
