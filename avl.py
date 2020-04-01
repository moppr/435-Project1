from collections import deque
from bst import BST, Node


class AVL(BST):

    def insert_rec(self, value, node=None):
        raise NotImplementedError

    def delete_rec(self, value, node=None):
        raise NotImplementedError

    def find_next_rec(self, value, node=None, next=None):
        raise NotImplementedError

    def find_prev_rec(self, value, node=None, prev=None):
        raise NotImplementedError

    def find_min_rec(self, node=None):
        raise NotImplementedError

    def find_max_rec(self, node=None):
        raise NotImplementedError

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

        # perform insertion if applicable
        self.traversal_counter += 1
        if value < parent.value:
            parent.left = Node(value)
        elif value > parent.value:
            parent.right = Node(value)
        else:
            raise ValueError(f"Cannot insert value {value} that already exists in the tree")

        # update heights starting from most recently visited parent
        for node in parents:
            self._update_height(node)

        # rebalance the tree when done, from most recent parent up to root
        for i, parent in enumerate(parents):
            self._rebalance(parent, parents[i + 1] if i + 1 < len(parents) else None)

    def delete_iter(self, value):
        # nothing to delete on an empty tree
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        # search for the node to delete and its parent
        # as well as whatever parents were visited to reach there
        # and check which side of the parent the node is on
        node, parent, parents = self._find(value, self.root, True)
        parent_side = self._left_or_right(node.value, parent)

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
                    find_results = self._find(value, node, True, True)
                    node, parent = find_results[:2]
                    parents = find_results[2] + parents
                parent_side = self._left_or_right(node.value, parent)
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

        # update heights starting from most recently visited parent
        for node in parents:
            self._update_height(node)

        # rebalance the tree when done, from most recent parent up to root
        for i, parent in enumerate(parents):
            self._rebalance(parent, parents[i + 1] if i + 1 < len(parents) else None)

    # this method calculates the height of a given node with no prior knowledge,
    # which is now deprecated since the Node class has been updated to store its own height
    # (much quicker than running an O(n) traversal every time height was needed)
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
        height = -1
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

    def deep_traversal(self):
        if not self.root:
            print("tree is empty")
            return

        # this is just for testing purposes - prints traversal of the deepest path
        node = self.root
        while node:
            print(node, node.height, '>', self._height(node.left), self._height(node.right))
            node = node.right if self._height(node.right) > self._height(node.left) else node.left

    def _balance_factor(self, node=None):
        # empty trees are balanced
        if not self.root:
            return 0

        # any calls with no node given start from root
        if not node:
            node = self.root

        # return height of left tree minus height of right tree
        return self._height(node.left) - self._height(node.right)

    def _left_rotate(self, old_root, local_root):
        # old root's right child becomes the new root and new root's left subtree becomes old root's right subtree
        new_root = old_root.right
        subtree = new_root.left
        old_root.right = subtree
        new_root.left = old_root
        if local_root:
            if new_root.value < local_root.value:
                local_root.left = new_root
            else:
                local_root.right = new_root
        else:
            self.root = new_root
        self._update_height(old_root)
        self._update_height(new_root)
        return new_root

    def _right_rotate(self, old_root, local_root):
        # old root's left child becomes the new root and new root's right subtree becomes old root's left subtree
        new_root = old_root.left
        subtree = new_root.right
        old_root.left = subtree
        new_root.right = old_root
        if local_root:
            if new_root.value < local_root.value:
                local_root.left = new_root
            else:
                local_root.right = new_root
        else:
            self.root = new_root
        self._update_height(old_root)
        self._update_height(new_root)
        return new_root

    def _rebalance(self, node, parent):
        balance_factor = self._balance_factor(node)

        # left-heavy
        if balance_factor > 1:
            # extra step for left-right
            if self._balance_factor(node.left) < 0:
                node.left = self._left_rotate(node.left, node)
            # both right-right and left-right
            return self._right_rotate(node, parent)
        # right-heavy
        if balance_factor < -1:
            # extra step for right-left
            if self._balance_factor(node.right) > 0:
                node.right = self._right_rotate(node.right, node)
            # both left-left and right-left
            return self._left_rotate(node, parent)
        # no rebalance because tree is sufficiently balanced
        return node

    def _find(self, value, node=None, track_parents=False, decrement_path=False):
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

    def _update_height(self, node):
        # note: wanted this to be static, but apparently that means it has no way of accessing self._height?
        node.height = max(self._height(node.left), self._height(node.right)) + 1

    @staticmethod
    def _height(node):
        # used to safely access height of a node if it may or may not exist
        return node.height if node else -1


if __name__ == "__main__":
    # some demo code to display each of the functions in action
    avl = AVL()

    # TODO: replace these with recursive versions once implemented
    print('generate whole tree')
    avl.sort([15, 3, 7, 6, 4, 8, 10, 17, 20, 18, 22, 16])
    avl.display()
    print('root:', avl.root)
    print('max:', avl.find_max_iter())
    print('min:', avl.find_min_iter())
    print('root left:', avl.root.left)
    print('root right:', avl.root.right)
    print('root next:', avl.find_next_iter(avl.root.value))
    print('root prev:', avl.find_prev_iter(avl.root.value))
    print('4 prev:', avl.find_prev_iter(4))
    print('10 next:', avl.find_next_iter(10))
    print('18 prev:', avl.find_prev_iter(18))

    # iterative methods
    print('\ndelete 7, 6, 22, 16, 15')
    avl.bulk_delete([7, 6, 22, 16, 15])
    print(avl)
    avl.display()
    print('root:', avl.root)
    print('max:', avl.find_max_iter())
    print('min:', avl.find_min_iter())
    print('root left:', avl.root.left)
    print('root right:', avl.root.right)
    print('root next:', avl.find_next_iter(avl.root.value))
    print('root prev:', avl.find_prev_iter(avl.root.value))
    print('20 next:', avl.find_next_iter(20))
    print('10 next:', avl.find_next_iter(10))
    print('17 prev:', avl.find_prev_iter(17))
