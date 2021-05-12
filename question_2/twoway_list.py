"""
"""
class Node:
    """
    """
    def __init__(self, data, next = None):
        """
        Instantiates a Node with default next of None
        """
        self.data = data
        self.next = next

class TwoWayNode(Node):
    """
    """
    def __init__(self, data, previous = None, next = None):
        Node.__init__(self, data, next)
        self.previous = previous

class TW_linked_list:
    """
    """
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def add(self, node):
        if self.tail == None:
            self.head = node
            self.tail = node
        else:
            tail = self.tail
            tail.next, node.previous = node, tail
            self.tail = node

    def __iter__(self):
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self.head)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)