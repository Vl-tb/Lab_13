"""
This module contains one ADT LinkedBinaryTree.
"""

class LinkedBinaryTree:
    """
    This class represents linked binary tree. It's without
    methods because game doesn't require them.
    """
    def __init__(self, root=None):
        self.key = root
        self.left_child = None
        self.right_child = None
