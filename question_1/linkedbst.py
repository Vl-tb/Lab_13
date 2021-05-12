"""
File: linkedbst.py
Author: Ken Lambert & Vladyslav Protsenko
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log, ceil


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            output = ""
            if node != None:
                output += recurse(node.right, level + 1)
                output += "| " * level
                output += str(node.data) + "\n"
                output += recurse(node.left, level + 1)
            return output

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return lyst

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_left_subtree(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_left_subtree(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        root = self._root
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top == None:
                return -1
            children = [top.left, top.right]
            return 1 + max(height1(child) for child in children)

        return height1(root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        nodes = self._size
        balance = ceil(log(nodes + 1, 2) - 1)
        height = self.height()
        if height <= balance:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        nodes = self.inorder()
        output = []
        for node in nodes:
            if node >= low and node <= high:
                output.append(node)
        return output

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = self.inorder()
        self.clear()
        def recurse(lst):
            """
            """
            if len(lst) == 1:
                if self.find(lst[0]) == None:
                    self.add(lst[0])
                return
            elif len(lst) == 0:
                return
            else:
                root = lst[ceil((len(lst)-1) / 2)]
                self.add(root)
                first_part = lst[:ceil((len(lst)-1) / 2)]
                second_part = lst[ceil((len(lst)-1) / 2) + 1:]
                recurse(first_part)
                recurse(second_part)
                return
        recurse(nodes)
        return self


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        param = 0
        if self.find(item) == None:
            param = 1
            self.add(item)
        nodes = self.inorder()
        index = nodes.index(item)
        if index == len(nodes)-1:
            if param:
                self.remove(item)
            return None
        successor = nodes[index + 1]
        if param:
            self.remove(item)
        return successor

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        param = 0
        if self.find(item) == None:
            param = 1
            self.add(item)
        nodes = self.inorder()
        index = nodes.index(item)
        if not index:
            if param:
                self.remove(item)
            return None
        predecessor = nodes[index - 1]
        if param:
            self.remove(item)
        return predecessor
        
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
    
if __name__ == "__main__":
    tree = LinkedBST()
    tree_1 = LinkedBST()
    tree.add(1)
    tree.add(2)
    tree.add(3)
    tree.add(4)
    tree.add(5)
    tree.add(6)
    tree.add(7)
    tree.add(8)
    tree.add(9)
    tree.add(20)

    # tree.add(34)
    # tree.add(32)
    # tree.add(70)
    # tree.add(19)
    # tree.add(33)
    # tree.add(61)
    # tree.add(100)
    # tree.add(10)
    # tree.add(23)
    # tree.add(21)
    # tree.add(25)
    # print(tree)
    # print(tree.height())
    print(tree.inorder())
    # print(tree.successor(99))
    # print(tree.predecessor(22))
    print(tree.rebalance())
    # print(tree)
    # print(tree.height())
    # print(tree._size)
    # print(tree.is_balanced())
    # print(tree.range_find(20, 76))
    # print(tree_1.height())
    # print(type(tree_1))
