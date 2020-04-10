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
        if not self.root:
            self.traversal_counter += 1
            self.root = Node(value)
            return

        node = self.root
        parent = None

        # Search for appropriate spot to insert and keep track of parents.
        parents = deque()
        while node:
            self.traversal_counter += 1
            parents.appendleft(node)
            parent = node
            node = node.left if value < node else node.right

        # Perform insertion if applicable.
        self.traversal_counter += 1
        if value < parent:
            parent.left = Node(value)
        elif value > parent:
            parent.right = Node(value)
        else:
            raise ValueError(f"Cannot insert value {value} that already exists in the tree")

        for node in parents:
            self._update_height(node)

        for i, parent in enumerate(parents):
            self._rebalance(parent, parents[i + 1] if i + 1 < len(parents) else None)

    def delete_iter(self, value):
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        node, parent, parents = self._find(value, self.root, True)
        parent_side = self._left_or_right(node.value, parent)

        if not node:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        # Determine deletion behavior based on which children exist.
        while True:
            if not node.left and not node.right:
                temp = None
            elif node.left and not node.right:
                temp = node.left
            elif node.right and not node.left:
                temp = node.right
            else:
                next = self.find_next_iter(node.value, node)
                node.value = next.value
                parent = node
                parents.appendleft(parent)
                node = node.right
                value = next.value

                # Only update the node/parent if there is at least one traversal to be done,
                # otherwise the algorithm will return to the tree's root and cause errors.
                if parent.right != parent:
                    find_results = self._find(value, node, True, True)
                    node, parent = find_results[:2]
                    parents = find_results[2] + parents
                parent_side = self._left_or_right(node.value, parent)
                continue

            if parent_side == 'left':
                parent.left = temp
            elif parent_side == 'right':
                parent.right = temp
            else:
                self.root = temp
            break

        for node in parents:
            self._update_height(node)

        for i, parent in enumerate(parents):
            self._rebalance(parent, parents[i + 1] if i + 1 < len(parents) else None)

    def _balance_factor(self, node=None):
        if not self.root:
            return 0

        if not node:
            node = self.root

        return self._height(node.left) - self._height(node.right)

    def _left_rotate(self, old_root, local_root):
        # Old root's right child becomes the new root and new root's left subtree becomes old root's right subtree.
        new_root = old_root.right
        subtree = new_root.left
        old_root.right = subtree
        new_root.left = old_root
        if local_root:
            if new_root < local_root:
                local_root.left = new_root
            else:
                local_root.right = new_root
        else:
            self.root = new_root
        self._update_height(old_root)
        self._update_height(new_root)
        return new_root

    def _right_rotate(self, old_root, local_root):
        # Old root's left child becomes the new root and new root's right subtree becomes old root's left subtree.
        new_root = old_root.left
        subtree = new_root.right
        old_root.left = subtree
        new_root.right = old_root
        if local_root:
            if new_root < local_root:
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

        # Perform appropriate two-step rebalance, if necessary.
        if balance_factor > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._left_rotate(node.left, node)
            return self._right_rotate(node, parent)
        if balance_factor < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._right_rotate(node.right, node)
            return self._left_rotate(node, parent)
        return node

    def _find(self, value, node=None, track_parents=False, decrement_path=False):
        # Perform iterative binary search to retrieve node given its value.
        node = self.root if not node else node
        parent = None
        parents = deque()

        while node and value != node:
            parents.appendleft(node)
            parent = node
            # Decrement_path used during deletion if swap was made (2+ children).
            if decrement_path:
                node.height -= 1
            node = node.left if value < node else node.right

        if not node:
            parent = None

        return (node, parent, parents) if track_parents else node

    @staticmethod
    def _update_height(node):
        node.height = max(AVL._height(node.left), AVL._height(node.right)) + 1

    @staticmethod
    def _height(node):
        return node.height if node else -1


if __name__ == "__main__":
    avl = AVL()

    # TODO: replace these with recursive versions once implemented
    # Demo iterative methods.
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

    # Demo iterative methods.
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
