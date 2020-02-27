class Node:

    def __init__(self, value):
        self.value = value
        self.left = self.right = None

    def __str__(self):
        return str(self.value)


class BSTRec:

    def __init__(self):
        self.root = None

    def insert_rec(self, value, node=None):
        # any calls with no parameter start from root
        if not node:
            node = self.root

        # create root if necessary
        if not self.root:
            self.root = Node(value)

        # if the value is less than current and current does not already have a left child,
        # set the left child to the value
        # otherwise, recursively send the value to the left child
        elif value < node.value:
            if not node.left:
                node.left = Node(value)
            else:
                self.insert_rec(value, node.left)
        # if the value is greater than current and current does not already have a right child,
        # set the right child to the value
        # otherwise, recursively send the value to the right child
        elif value > node.value:
            if not node.right:
                node.right = Node(value)
            else:
                self.insert_rec(value, node.right)

    def delete_rec(self):
        pass

    def find_next_rec(self):
        pass

    def find_prev_rec(self):
        pass

    def find_min_rec(self):
        pass

    def find_max_rec(self):
        pass

    def inorder(self, node=None):
        """Print inorder traversal"""
        if not node:
            node = self.root

        output = []

        if node.left:
            output += self.inorder(node.left)
        output.append(str(node.value))
        if node.right:
            output += self.inorder(node.right)
        return output


if __name__ == "__main__":
    bst = BSTRec()
    for x in [15, 3, 2, 6, 8, 11]:
        bst.insert_rec(x)
    print(', '.join(bst.inorder())