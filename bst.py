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
        # any calls with no node given start from root
        if not node:
            node = self.root

        # create root if this is the first node in the tree
        if not self.root:
            self.root = Node(value)
            return

        # if the value is less than current and current does not already have a left child,
        # set the left child to the value
        # otherwise, recursively send the value to the left child
        if value < node.value:
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
        # adding an existing value is illegal
        else:
            raise ValueError("Cannot insert value that already exists in the tree")

    def delete_rec(self, value, node=None):
        # any calls with no node given start from root
        if not node:
            node = self.root

        # nothing to delete on an empty tree
        if not self.root:
            raise ValueError("Cannot delete value that does not exist in the tree")

        # if the value is not equal to the current node, recursively call delete
        # on the appropriate child and point the resulting new root to be the new
        # child of the current node, and return the current node
        if value < node.value:
            # deleting nonexistent value is illegal
            if not node.left:
                raise ValueError("Cannot delete value that does not exist in the tree")
            node.left = self.delete_rec(value, node.left)
            return node
        elif value > node.value:
            # deleting nonexistent value is illegal
            if not node.right:
                raise ValueError("Cannot delete value that does not exist in the tree")
            node.right = self.delete_rec(value, node.right)
            return node

        # if the value is equal to the current node, if it has no children, delete the node and return None
        if not node.left and not node.right:
            node = None
            return None
        # if it has one child, delete the node and return the child
        elif node.left and not node.right:
            temp = node.left
            node = None
            return temp
        elif node.right and not node.left:
            temp = node.right
            node = None
            return temp
        # if it has two children, find the node with the next value and copy it to the current node
        # and recursively delete the new value from the right child, and return the current node
        else:
            next = self.find_next_rec(node.value, node)
            node.value = next.value
            node.right = self.delete_rec(node.value, node.right)
            return node

    def find_next_rec(self, value, node=None, next=None):
        # providing value only used for user calls, providing value and node used by delete function
        if not node:
            node = self.find(value)
            # if value not found in tree, the algorithm can't work (recurses endlessly)
            # so the operation is illegal
            if not node:
                raise ValueError("Cannot find_next value that does not exist in the tree")

        # currently on the starting node
        if node.value == value:
            # next being None indicates that this is the initial call
            # if it exists and we reached the original node, it's time to return
            # next being equal to the original node indicates that no successor was found
            if next:
                return next if next.value != value else None
            # if the starting node has a right child, the successor is the smallest element
            # of the right subtree
            if node.right:
                return self.find_min_rec(node.right)
            # if there is no right child, start searching from the root
            return self.find_next_rec(value, self.root, node)
        # if the current node is larger than the target, call recursively on its left child
        # and tag the current node as the next largest seen so far
        elif node.value > value:
            return self.find_next_rec(value, node.left, node)
        # if the current node is smaller than the target, call recursively on its right child
        # and leave the next largest seen so far as whatever it was previously
        elif node.value < value:
            return self.find_next_rec(value, node.right, next)

    def find_prev_rec(self, value, node=None, prev=None):
        # providing value only used for user calls
        if not node:
            node = self.find(value)
            # if value not found in tree, the algorithm can't work (recurses endlessly)
            # so the operation is illegal
            if not node:
                raise ValueError("Cannot find_prev value that does not exist in the tree")

        # currently on the starting node
        if node.value == value:
            # next being None indicates that this is the initial call
            # if it exists and we reached the original node, it's time to return
            # next being equal to the original node indicates that no successor was found
            if prev:
                return prev if prev.value != value else None
            # if the starting node has a left child, the successor is the largest element
            # of the left subtree
            if node.left:
                return self.find_max_rec(node.left)
            # if there is no left child, start searching from the root
            return self.find_prev_rec(value, self.root, node)
        # if the current node is smaller than the target, call recursively on its right child
        # and tag the current node as the next smallest seen so far
        elif node.value < value:
            return self.find_prev_rec(value, node.right, node)
        # if the current node is larger than the target, call recursively on its left child
        # and leave the next smallest seen so far as whatever it was previously
        elif node.value > value:
            return self.find_prev_rec(value, node.left, prev)

    def find_min_rec(self, node=None):
        # any calls with no node given start from root
        if not node:
            node = self.root

        # manually handle empty tree
        if not self.root:
            return None

        # return a recursive call on the left child if there is one, else return the current node
        return self.find_min_rec(node.left) if node.left else node

    def find_max_rec(self, node=None):
        # any calls with no node given start from root
        if not node:
            node = self.root

        # manually handle empty tree
        if not self.root:
            return None

        # return a recursive call on the right child if there is one, else return the current node
        return self.find_max_rec(node.right) if node.right else node

    def sort(self, values, refresh=False):
        # optional refresh will wipe the tree and use values to start a new tree
        if refresh:
            self.root = None

        # bulk insert values and print the in-order traversal to sort them
        self.bulk_insert(values)
        print(self)

    # below this point are all helper functions that are not directly related to question 1 or 2

    def find(self, value):
        # simple iterative binary search to retrieve node given its value
        node = self.root
        while node and value != node.value:
            node = node.left if value < node.value else node.right
        return node

    def bulk_insert(self, values):
        for value in values:
            self.insert_rec(value)

    def bulk_delete(self, values):
        for value in values:
            self.delete_rec(value)

    def in_order(self, node=None):
        # any calls with no node given start from root
        if not node:
            node = self.root

        # manually handle empty tree
        if not self.root:
            return []

        # return in-order traversal as array, used for string representation of whole tree
        output = []
        if node.left:
            output += self.in_order(node.left)
        output.append(node.value)
        if node.right:
            output += self.in_order(node.right)
        return output

    def __str__(self):
        return ', '.join((str(node) for node in self.in_order(self.root)))

'''
class BSTIter:

    def __init__(self):
        self.root = None

    def insert_iter(self, node):
        if node:
            curr = node
        else
'''

if __name__ == "__main__":
    # some demo code to display each of the functions in action
    # https://i.imgur.com/ySfT1lJ.png
    bst = BSTRec()
    print('generate whole tree')
    bst.sort([15, 3, 7, 6, 4, 8, 10, 17, 20, 18, 22, 16])
    print('root:', bst.root)
    print('max:', bst.find_max_rec())
    print('min:', bst.find_min_rec())
    print('root left:', bst.root.left)
    print('root right:', bst.root.right)
    print('root next:', bst.find_next_rec(bst.root.value))
    print('root prev:', bst.find_prev_rec(bst.root.value))
    print('4 prev:', bst.find_prev_rec(4))
    print('10 next:', bst.find_next_rec(10))
    print('18 prev:', bst.find_prev_rec(18))

    print('\ndelete 7, 6, 22, 16, 15')
    bst.bulk_delete([7, 6, 22, 16, 15])
    print(bst)
    print('root:', bst.root)
    print('max:', bst.find_max_rec())
    print('min:', bst.find_min_rec())
    print('root left:', bst.root.left)
    print('root right:', bst.root.right)
    print('root next:', bst.find_next_rec(bst.root.value))
    print('root prev:', bst.find_prev_rec(bst.root.value))
    print('20 next:', bst.find_next_rec(20))
    print('10 next:', bst.find_next_rec(10))
    print('17 prev:', bst.find_prev_rec(17))
