class Node:

    def __init__(self, value):
        self.value = value
        self.left = self.right = None
        self.height = 0
        # TODO: see if height is useful anywhere in BST

    def __str__(self):
        return str(self.value)


class BST:

    def __init__(self):
        self.root = None
        self.traversal_counter = 0

    # TODO: double check which methods are supposed to return something
    # TODO: make another pass on the comments - less verbose in some places, more in others
    # TODO: implement isBSBST() and related methods in the context of this class

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
        # nothing to delete on an empty tree
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        # any calls with no node given start from root
        if not node:
            node = self.root

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
        # manually handle empty tree
        if not self.root:
            return None

        # any calls with no node given start from root
        if not node:
            node = self.root

        # return a recursive call on the left child if there is one, else return the current node
        return self.find_min_rec(node.left) if node.left else node

    def find_max_rec(self, node=None):
        # manually handle empty tree
        if not self.root:
            return None

        # any calls with no node given start from root
        if not node:
            node = self.root

        # return a recursive call on the right child if there is one, else return the current node
        return self.find_max_rec(node.right) if node.right else node

    def insert_iter(self, value):
        # create root if this is the first node in the tree
        if not self.root:
            self.root = Node(value)
            return

        # start insertion from root
        node = self.root
        parent = None

        # search for appropriate spot to insert
        while node:
            parent = node
            node = node.left if value < node.value else node.right

        # perform insertion where applicable
        if value < parent.value:
            parent.left = Node(value)
        elif value > parent.value:
            parent.right = Node(value)
        else:
            raise ValueError(f"Cannot insert value {value} that already exists in the tree")

    def delete_iter(self, value):
        # nothing to delete on an empty tree
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        # search for the node to delete and its parent starting from root
        # and check which side of the parent the node is on
        node, parent = self.find(value, self.root, True)
        parent_side = self.left_or_right(node.value, parent) if parent else None

        # can't delete if the node wasn't found
        if not node:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        while True:
            # if the node has no children, delete it
            if not node.left and not node.right:
                temp = None
            # if the node has one child, save that child to give to its parent later
            elif node.left and not node.right:
                temp = node.left
            elif node.right and not node.left:
                temp = node.right
            # if the node has two children, swap its value with the next value and
            # delete the successor starting from its right child
            else:
                next = self.find_next_iter(node.value, node)
                node.value = next.value
                parent = node
                node = node.right
                value = next.value

                # ONLY update the parent value if there is at least one traversal to be done
                # because otherwise we'll unintentionally go back to the whole tree's root and break stuff
                if parent.right.value != parent.value:
                    node, parent = self.find(value, node, True)
                parent_side = self.left_or_right(node.value, parent)
                continue

            # set the parent's child to be the new value (None for 0 children, child for 1)
            # if there is no parent, that means the 'child' is actually the whole tree's root
            if parent_side == 'left':
                parent.left = temp
            elif parent_side == 'right':
                parent.right = temp
            else:
                self.root = temp
            break

        # return new root at the end
        return self.root

    def find_next_iter(self, value, node=None):
        # node can be set to specify a starting point, such as from delete function
        node = self.find(value) if not node else node
        if not node:
            raise ValueError(f"Cannot find_next value {value} that does not exist in the tree")

        next = None

        while True:
            # if on the starting node, we're either ready to return or we need to start searching
            if node.value == value:
                # return appropriate result if we're done searching
                if next:
                    return next if next.value != value else None
                # if there's a right child, the successor is the smallest in the right subtree
                if node.right:
                    return self.find_min_iter(node.right)
                # otherwise, start searching from root
                next = node
                node = self.root
            # if searching and we're on a larger node, save current value as the highest seen so far
            # and move to its left child
            elif node.value > value:
                next = node
                node = node.left
            # if searching and we're on a smaller node, don't update highest value seen so far
            # just move to the right child
            elif node.value < value:
                node = node.right

    def find_prev_iter(self, value, node=None):
        # note: should not be called with non-default value of node,
        # however leaving it like that to match find_next_iter
        node = self.find(value) if not node else node
        if not node:
            raise ValueError(f"Cannot find_prev value {value} that does not exist in the tree")

        prev = None

        while True:
            # if on the starting node, we're either ready to return or we need to start searching
            if node.value == value:
                # return appropriate result if we're done searching
                if prev:
                    return prev if prev.value != value else None
                # if there's a left child, the successor is the largest in the left subtree
                if node.left:
                    return self.find_max_iter(node.left)
                # otherwise, start searching from root
                prev = node
                node = self.root
            # if searching and we're on a smaller node, save current value as the smallest seen so far
            # and move to its right child
            elif node.value < value:
                prev = node
                node = node.right
            # if searching and we're on a larger node, don't update smallest value seen so far
            # just move to the left child
            elif node.value > value:
                node = node.left

    def find_min_iter(self, node=None):
        # nothing to find on empty tree
        if not self.root:
            return None

        # start from root unless otherwise specified
        node = self.root if not node else node

        # move left as much as possible
        while node.left:
            node = node.left

        return node

    def find_max_iter(self, node=None):
        # nothing to find on empty tree
        if not self.root:
            return None

        # start from root unless otherwise specified
        node = self.root if not node else node

        # move right as much as possible
        while node.right:
            node = node.right

        return node

    def sort(self, values, recursive=False):
        # bulk insert values and print the in-order traversal to sort them
        self.bulk_insert(values, recursive)
        print(self)

    # below this point are all helper functions that are not directly related to question 1 or 2

    def find(self, value, node=None, track_parent=False):
        # simple iterative binary search to retrieve node given its value
        node = self.root if not node else node
        parent = None

        while node and value != node.value:
            parent = node
            node = node.left if value < node.value else node.right

        # parent doesn't check by itself if it should exist, so nodes not found need to manually
        # have parent set to None
        if not node:
            parent = None

        return (node, parent) if track_parent else node

    def bulk_insert(self, values, recursive=False):
        for value in values:
            if recursive:
                self.insert_rec(value)
            else:
                self.insert_iter(value)

    def bulk_delete(self, values, recursive=False):
        for value in values:
            if recursive:
                self.delete_rec(value)
            else:
                self.delete_iter(value)

    def in_order(self, node=None):
        # manually handle empty tree
        if not self.root:
            return []

        # any calls with no node given start from root
        if not node:
            node = self.root

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

    def clear(self):
        self.root = None

    # note: the following static method doesn't have default values like some other methods do
    # because there is no context in which it would be called with no node specified

    @staticmethod
    def left_or_right(value, node):
        # given a value, check if one of the children matches it, and return the child if so
        if node.left and value == node.left.value:
            return 'left'
        if node.right and value == node.right.value:
            return 'right'
        return None


if __name__ == "__main__":
    # some demo code to display each of the functions in action
    # https://i.imgur.com/ySfT1lJ.png
    bst = BST()

    # recursive methods
    print('generate whole tree')
    bst.sort([15, 3, 7, 6, 4, 8, 10, 17, 20, 18, 22, 16], True)
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

    # iterative methods
    print('\ndelete 7, 6, 22, 16, 15')
    bst.bulk_delete([7, 6, 22, 16, 15])
    print(bst)
    print('root:', bst.root)
    print('max:', bst.find_max_iter())
    print('min:', bst.find_min_iter())
    print('root left:', bst.root.left)
    print('root right:', bst.root.right)
    print('root next:', bst.find_next_iter(bst.root.value))
    print('root prev:', bst.find_prev_iter(bst.root.value))
    print('20 next:', bst.find_next_iter(20))
    print('10 next:', bst.find_next_iter(10))
    print('17 prev:', bst.find_prev_iter(17))
