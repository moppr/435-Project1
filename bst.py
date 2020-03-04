class Node:

    def __init__(self, value):
        self.value = value
        self.left = self.right = None

    def __str__(self):
        return str(self.value)


class BST:

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
            raise ValueError(f"Cannot insert value {value} that already exists in the tree")

    def delete_rec(self, value, node=None):
        # any calls with no node given start from root
        if not node:
            node = self.root

        # nothing to delete on an empty tree
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        # if the value is not equal to the current node, recursively call delete
        # on the appropriate child and point the resulting new root to be the new
        # child of the current node, and return the current node
        if value < node.value:
            # deleting nonexistent value is illegal
            if not node.left:
                raise ValueError(f"Cannot delete value {value} that does not exist in the tree")
            node.left = self.delete_rec(value, node.left)
            return node
        elif value > node.value:
            # deleting nonexistent value is illegal
            if not node.right:
                raise ValueError(f"Cannot delete value {value} that does not exist in the tree")
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
                raise ValueError(f"Cannot find_next value {value} that does not exist in the tree")

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
                raise ValueError(f"Cannot find_prev value {value} that does not exist in the tree")

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

    # TODO: iter functions go here

    # TODO: possibly root checks should be the first thing, before setting node

    def insert_iter(self, value):
        node = self.root

        # create root if this is the first node in the tree
        if not self.root:
            self.root = Node(value)
            return

        while True:
            # if the value is less than current and current does not already have a left child,
            # set the left child to the value and return to indicate completion
            # otherwise, move to the left child
            if value < node.value:
                if not node.left:
                    node.left = Node(value)
                    return
                else:
                    node = node.left
            # if the value is greater than current and current does not already have a right child,
            # set the right child to the value and return to indicate completion
            # otherwise, move to the right child
            elif value > node.value:
                if not node.right:
                    node.right = Node(value)
                    return
                else:
                    node = node.right
            # adding an existing value is illegal
            else:
                raise ValueError(f"Cannot insert value {value} that already exists in the tree")

    def delete_iter(self, value):
        node = self.root

        # nothing to delete on an empty tree
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        # use find with the track_parent option to get both the node and its parent
        node, parent = self.find(value, True)

        if not node:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        parent_side = self.left_or_right(node.value, parent)

        # if the node has no children
        if not node.left and not node.right:
            node = None  # why isn't this working???
            # workaround
            temp = None
            if parent_side == 'left':
                parent.left = temp
            elif parent_side == 'right':
                parent.right = temp
            else:
                raise ValueError("something is wrong while deleting with no child")
        # one child
        # TODO: this can be condensed, check first if it makes it too messy before proceeding though
        elif node.left and not node.right:
            temp = node.left
            node = None
            if parent_side == 'left':
                parent.left = temp
            elif parent_side == 'right':
                parent.right = temp
            else:
                raise ValueError("something is wrong while deleting with one child")
        elif node.right and not node.left:
            temp = node.right
            node = None
            if parent_side == 'left':
                parent.left = temp
            elif parent_side == 'right':
                parent.right = temp
            else:
                raise ValueError("something is wrong while deleting with one child")
        else:
            # TODO: implement two children case
            pass

        # return new root at the end
        return self.root



    def sort(self, values, refresh=False):
        # optional refresh will wipe the tree and use values to start a new tree
        if refresh:
            self.root = None

        # bulk insert values and print the in-order traversal to sort them
        self.bulk_insert(values)
        print(self)

    # below this point are all helper functions that are not directly related to question 1 or 2

    def left_or_right(self, value, parent):
        # TODO: probably a better way to write this
        if parent.left and value < parent.value:
            return 'left' if value == parent.left.value else None
        if parent.right and value > parent.value:
            return 'right' if value == parent.right.value else None
        return None

    def find(self, value, track_parent=False):
        # simple iterative binary search to retrieve node given its value
        node = self.root
        parent = None
        while node and value != node.value:
            parent = node
            node = node.left if value < node.value else node.right
        # parent doesn't check by itself if it should exist, so nodes not found need to manually
        # have parent set to None
        if not node:
            parent = None
        return (node, parent) if track_parent else node

    def bulk_insert(self, values):
        for value in values:
            self.insert_iter(value)

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


if __name__ == "__main__":
    # some demo code to display each of the functions in action
    # https://i.imgur.com/ySfT1lJ.png
    bst = BST()
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
