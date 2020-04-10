from node import *


class BST:

    # TODO: implement interview problems such as isBSBST() in the context of this class

    def __init__(self):
        self.root = None
        self.traversal_counter = 0

    def __str__(self):
        return ', '.join((str(node) for node in self._in_order(self.root)))

    def insert_rec(self, value, node=None):
        if not node:
            node = self.root

        if not self.root:
            self.root = Node(value)
            return

        # Create new child or send down recursively.
        if value < node:
            if not node.left:
                node.left = Node(value)
            else:
                self.insert_rec(value, node.left)
        elif value > node:
            if not node.right:
                node.right = Node(value)
            else:
                self.insert_rec(value, node.right)
        else:
            raise ValueError(f"Cannot insert value {value} that already exists in the tree")

    def delete_rec(self, value, node=None):
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        if not node:
            node = self.root

        # Send down recursively if target node not found yet.
        if value < node:
            if not node.left:
                raise ValueError(f"Cannot delete value {value} that does not exist in the tree")
            node.left = self.delete_rec(value, node.left)
            return node
        elif value > node:
            if not node.right:
                raise ValueError(f"Cannot delete value {value} that does not exist in the tree")
            node.right = self.delete_rec(value, node.right)
            return node

        # Determine deletion behavior based on which children exist.
        if not node.left and not node.right:
            node = None
            return None
        elif node.left and not node.right:
            temp = node.left
            node = None
            return temp
        elif node.right and not node.left:
            temp = node.right
            node = None
            return temp
        else:
            next = self.find_next_rec(node.value, node)
            node.value = next.value
            node.right = self.delete_rec(node.value, node.right)
            return node

    def find_next_rec(self, value, node=None, next=None):
        if not node:
            node = self._find(value)
            if not node:
                raise ValueError(f"Cannot find_next value {value} that does not exist in the tree")

        if node == value:
            if next:
                return next if next != value else None
            if node.right:
                return self.find_min_rec(node.right)
            return self.find_next_rec(value, self.root, node)
        elif node > value:
            return self.find_next_rec(value, node.left, node)
        elif node < value:
            return self.find_next_rec(value, node.right, next)

    def find_prev_rec(self, value, node=None, prev=None):
        if not node:
            node = self._find(value)
            if not node:
                raise ValueError(f"Cannot find_prev value {value} that does not exist in the tree")

        if node == value:
            if prev:
                return prev if prev != value else None
            if node.left:
                return self.find_max_rec(node.left)
            return self.find_prev_rec(value, self.root, node)
        elif node < value:
            return self.find_prev_rec(value, node.right, node)
        elif node > value:
            return self.find_prev_rec(value, node.left, prev)

    def find_min_rec(self, node=None):
        if not self.root:
            return None

        if not node:
            node = self.root

        return self.find_min_rec(node.left) if node.left else node

    def find_max_rec(self, node=None):
        if not self.root:
            return None

        if not node:
            node = self.root

        return self.find_max_rec(node.right) if node.right else node

    def insert_iter(self, value):
        if not self.root:
            self.traversal_counter += 1
            self.root = Node(value)
            return

        node = self.root
        parent = None

        # Search for appropriate spot to insert.
        while node:
            self.traversal_counter += 1
            parent = node
            # Using node comparison methods on this line causes performance issues on BST sorted.
            # This is because the performance hit is negligible until the worst case scenario.
            node = node.left if value < node.value else node.right

        # Perform insertion if applicable.
        self.traversal_counter += 1
        if value < parent:
            parent.left = Node(value)
        elif value > parent:
            parent.right = Node(value)
        else:
            raise ValueError(f"Cannot insert value {value} that already exists in the tree")

    def delete_iter(self, value):
        if not self.root:
            raise ValueError(f"Cannot delete value {value} that does not exist in the tree")

        node, parent = self._find(value, self.root, True)
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
                node = node.right
                value = next.value

                # Only update the parent value if there is at least one traversal to be done,
                # otherwise the algorithm will return to the tree's root and cause errors.
                if parent.right != parent:
                    node, parent = self._find(value, node, True)
                parent_side = self._left_or_right(node.value, parent)
                continue

            if parent_side == 'left':
                parent.left = temp
            elif parent_side == 'right':
                parent.right = temp
            else:
                self.root = temp
            break

    def find_next_iter(self, value, node=None):
        node = self._find(value) if not node else node
        if not node:
            raise ValueError(f"Cannot find_next value {value} that does not exist in the tree")

        next = None
        while True:
            if node == value:
                if next:
                    return next if next != value else None
                if node.right:
                    return self.find_min_iter(node.right)
                next = node
                node = self.root
            elif node > value:
                next = node
                node = node.left
            elif node < value:
                node = node.right

    def find_prev_iter(self, value, node=None):
        node = self._find(value) if not node else node
        if not node:
            raise ValueError(f"Cannot find_prev value {value} that does not exist in the tree")

        prev = None
        while True:
            if node == value:
                if prev:
                    return prev if prev != value else None
                if node.left:
                    return self.find_max_iter(node.left)
                prev = node
                node = self.root
            elif node < value:
                prev = node
                node = node.right
            elif node > value:
                node = node.left

    def find_min_iter(self, node=None):
        if not self.root:
            return None

        if not node:
            node = self.root

        while node.left:
            node = node.left

        return node

    def find_max_iter(self, node=None):
        if not self.root:
            return None

        if not node:
            node = self.root

        while node.right:
            node = node.right

        return node

    def sort(self, values, recursive=False):
        self.bulk_insert(values, recursive)
        print(self)

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

    def clear(self):
        self.root = None

    def display(self):
        self.root.display()

    def _find(self, value, node=None, track_parent=False):
        # Perform iterative binary search given value.
        node = self.root if not node else node
        parent = None

        while node and value != node:
            parent = node
            node = node.left if value < node else node.right

        if not node:
            parent = None

        return (node, parent) if track_parent else node

    def _in_order(self, node=None):
        if not self.root:
            return []

        if not node:
            node = self.root

        output = []
        if node.left:
            output += self._in_order(node.left)
        output.append(node.value)
        if node.right:
            output += self._in_order(node.right)
        return output

    @staticmethod
    def _left_or_right(value, node):
        if not node:
            return None

        if node.left and value == node.left:
            return 'left'
        if node.right and value == node.right:
            return 'right'


if __name__ == "__main__":
    bst = BST()

    # Demo recursive methods.
    print('generate whole tree')
    bst.sort([15, 3, 7, 6, 4, 8, 10, 17, 20, 18, 22, 16], True)
    bst.display()
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

    # Demo iterative methods.
    print('\ndelete 7, 6, 22, 16, 15')
    bst.bulk_delete([7, 6, 22, 16, 15])
    print(bst)
    bst.display()
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
