from collections import deque
from bst import BST, Node


class AVL(BST):

    # the following methods are intentionally inherited from BST:
    # (4c) find_next_rec, find_prev_rec, find_min_rec, find_max_rec
    # (4d) find_next_iter, find_prev_iter, find_min_iter, find_max_iter
    # __init__, sort, all helper methods

    def insert_iter(self, value):
        # create root if this is the first node in the tree
        if not self.root:
            self.traversal_counter += 1
            self.root = Node(value)
            return

        # start insertion from root
        node = self.root
        parent = None

        # keep track of parents so we can update their heights (in correct order) later
        parents = deque()
        # search for appropriate spot to insert
        while node:
            self.traversal_counter += 1
            parents.appendleft(node)
            parent = node
            node = node.left if value < node.value else node.right

        # perform insertion where applicable
        self.traversal_counter += 1
        if value < parent.value:
            parent.left = Node(value)
        elif value > parent.value:
            parent.right = Node(value)
        else:
            raise ValueError(f"Cannot insert value {value} that already exists in the tree")

        # update heights starting from most recently visited parent (goes from leaf up)
        for node in parents:
            self.update_height(node)

        # rebalance the tree when done
        self.rebalance(value)

    def delete_iter(self, value):
        # nothing to delete on an empty tree
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        # search for the node to delete and its parent starting from root
        # as well as whatever parents were visited to reach there
        # and check which side of the parent the node is on
        node, parent, parents = self.find(value, self.root, True)
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
                # also need to keep track of which parents were visited on the way down to the successor
                parents.appendleft(parent)
                node = node.right
                value = next.value

                # ONLY update the node/parent if there is at least one traversal to be done
                # because otherwise we'll unintentionally go back to the whole tree's root and break stuff
                if parent.right.value != parent.value:
                    find_results = self.find(value, node, True, True)
                    node, parent = find_results[:2]
                    parents = find_results[2] + parents
                parent_side = self.left_or_right(node.value, parent)
                continue

            # set the parent's child to be the new value (None for 0 child, child for 1)
            # if there is no parent, that means the 'child' is actually the whole tree's root
            if parent_side == 'left':
                parent.left = temp
            elif parent_side == 'right':
                parent.right = temp
            else:
                self.root = temp
            break

        # update heights starting from most recently visited parent (goes from leaf up)
        for node in parents:
            self.update_height(node)

        # rebalance the tree when done
        return self.rebalance(value, True)

    # below this point are all helper functions that are not directly related to question 4

    # this method was used to calculate the height of a given node with no prior knowledge,
    # which is now deprecated since the Node class has been updated to store its own height
    # (much quicker than running an O(n) traversal every time height was needed)
    # note: this returns the number of levels in the tree, which is one more than what the root
    # stores internally as its height (counting from 0 vs 1)
    def height_manual(self, node=None):
        # empty trees are considered to be height -1
        if not self.root:
            return -1

        # any calls with no node given start from root
        if not node:
            node = self.root

        # calculate height iteratively by performing a level-order traversal
        # use queue to track all the nodes on the current level
        queue = [node]
        height = 0
        while True:
            nodes = len(queue)
            # nodeless level indicates that the maximum height has been reached
            if not nodes:
                return height
            height += 1
            # add the children of the current level, in level-order, to the queue
            # and pop current level out in the process, effectively moving down to the next level
            while nodes:
                node = queue.pop(0)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                nodes -= 1

    def balance_factor(self, node=None):
        # empty trees are balanced
        if not self.root:
            return 0

        # any calls with no node given start from root
        if not node:
            node = self.root

        # return height of left tree minus height of right tree
        return self.height(node.left) - self.height(node.right)

    def left_rotate(self, old_root):
        # old root's right child becomes the new root and new root's left subtree becomes old root's right subtree
        new_root = old_root.right
        subtree = new_root.left
        old_root.right = subtree
        new_root.left = old_root
        self.root = new_root
        self.update_height(old_root)
        self.update_height(new_root)
        return new_root

    def right_rotate(self, old_root):
        # old root's left child becomes the new root and new root's right subtree becomes old root's left subtree
        new_root = old_root.left
        subtree = new_root.right
        old_root.left = subtree
        new_root.right = old_root
        self.root = new_root
        self.update_height(old_root)
        self.update_height(new_root)
        return new_root

    def rebalance(self, value, delete=False):
        # all rebalances start from root
        node = self.root
        balance_factor = self.balance_factor(node)

        # left
        if balance_factor > 1:
            # extra step for left-right
            if (delete and self.balance_factor(node.left) < 0) or (not delete and value > node.left.value):
                node.left = self.left_rotate(node.left)
            # both left-left and left-right
            return self.right_rotate(node)
        # right
        if balance_factor < -1:
            # extra step for right-left
            if (delete and self.balance_factor(node.right) > 0) or (not delete and value < node.right.value):
                node.right = self.right_rotate(node.right)
            # both right-right and right-left
            return self.left_rotate(node)
        # no rebalance because tree is sufficiently balanced
        return node

    def find(self, value, node=None, track_parents=False, decrement_path=False):
        # simple iterative binary search to retrieve node given its value
        node = self.root if not node else node
        parent = None
        parents = deque()

        while node and value != node.value:
            parents.appendleft(node)
            parent = node
            # decrement_path used during deletion if swap was made (2+ children)
            if decrement_path:
                node.height -= 1
            node = node.left if value < node.value else node.right

        # parent doesn't check by itself if it should exist, so nodes not found need to manually
        # have parent set to None
        if not node:
            parent = None

        return (node, parent, parents) if track_parents else node

    def update_height(self, node):
        # note: wanted this to be static, but apparently that means it has no way of accessing self.height?
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def verify_height(self):
        if not self.root:
            print("tree is empty")
            return

        # this is just for testing purposes - prints traversal of the deepest path
        node = self.root
        while node:
            print(node, node.height, '>', self.height(node.left), self.height(node.right))
            node = node.right if self.height(node.right) > self.height(node.left) else node.left

    # note: the following static methods don't have default values like some other methods do
    # because there is no context in which they would be called with no node specified

    @staticmethod
    def height(node):
        # used to safely access height of a node if it may or may not exist
        return node.height if node else -1


if __name__ == "__main__":
    # some demo code to display each of the functions in action
    avl = AVL()
    avl.bulk_insert([5, 3, 2, 7, 34])
    print(avl)
