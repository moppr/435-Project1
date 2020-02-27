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

    def delete_rec(self, value, node=None):
        # any calls with no parameter start from root
        if not node:
            node = self.root

        # if the value is lesser or greater than the current node, recursively call delete
        # on the left or right child respectively and point the resulting new root to be the new
        # left or right child of the current node, and return the current node
        if value < node.value:
            node.left = self.delete_rec(value, node.left)
            return node
        elif value > node.value:
            node.right = self.delete_rec(value, node.right)
            return node
        # if the value is equal to the current node, if it has no children, delete the node and return None
        else:
            if not node.left and not node.right:
                node = None
                return
            # if it has one child, delete the node and return the child
            elif node.left and not node.right:
                temp = node.left
                node = None
                return temp
            elif node.right and not node.left:
                temp = node.right
                node = None
                return temp
            # if it has two children, find the node with the next value and swap it with the current node
            # and delete it, and return the current node
            else:
                next = self.find_next_rec(node.value, node)
                node.value = next.value
                node.right = self.delete_rec(next.value, node.right)
                return node

    def find_next_rec(self, value, node):
        # if the current node is equal to the value (currently on the starting node) and there is a right child
        # return the smallest element in the right subtree
        if value == node.value:
            if node.right:
                return self.find_min_rec(node.right)
        # if the current node is smaller than the value, and there is a right child,
        # return the recursive call on that child, else None
        elif value > node.value:
            return self.find_next_rec(value, node.right) if node.right else None
        # if the current node is larger than the value, and there is a left child,
        # return the recursive call on that child, else None
        else:
            return self.find_next_rec(value, node.left) if node.left else None

    def find_prev_rec(self, value, node):
        # if the current node is equal to the value (currently on the starting node) and there is a left child
        # return the largest element in the left subtree
        if value == node.value:
            if node.left:
                return self.find_max_rec(node.left)
        # if the current node is larger than the value, and there is a left child,
        # return the recursive call on that child, else None
        elif value < node.value:
            return self.find_prev_rec(value, node.left) if node.left else None
        # if the current node is smaller than the value, and there is a right child,
        # return the recursive call on that child, else None
        else:
            return self.find_prev_rec(value, node.right) if node.right else None

    def find_min_rec(self, node):
        # return a recursive call on the left child if there is one, else return the current node
        return self.find_min_rec(node.left) if node.left else node

    def find_max_rec(self, node):
        # return a recursive call on the right child if there is one, else return the current node
        return self.find_max_rec(node.right) if node.right else node

    def inorder(self, node=None):
        """Return inorder traversal as array - used for printing out tree"""
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
    # testing each of the functions
    bst = BSTRec()
    for x in [15, 3, 2, 6, 8, 11, 9, 4, 16]:
        bst.insert_rec(x)
    print('whole tree')
    print(', '.join(bst.inorder()), end='\n\n')
    bst.delete_rec(6)
    bst.delete_rec(8)
    bst.delete_rec(3)
    bst.delete_rec(11)
    print('delete 6, 8, 3, 11')
    print(', '.join(bst.inorder()), end='\n\n')
    print('root', bst.root)
    print('max', bst.find_max_rec(bst.root))
    print('min', bst.find_min_rec(bst.root))
    print('root next', bst.find_next_rec(bst.root.value, bst.root))
    print('root prev', bst.find_prev_rec(bst.root.value, bst.root))
