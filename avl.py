from bst import BST, left_or_right  # TODO: determine if left_or_right is actually needed


class AVL(BST):

    # the following methods are intentionally inherited from BST:
    # (4c) find_next_rec, find_prev_rec, find_min_rec, find_max_rec
    # (4d) find_next_iter, find_prev_iter, find_min_iter, find_max_iter
    # __init__, sort, all helper methods

    def insert_rec(self, value, node=None):
        pass

    # below this point are all helper functions that are not directly related to question 4

    def height(self, node=None):
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
        # this could have been done with marginally less work if height was implemented without defaulting to root
        # but it will remain this way for better consistency between methods
        left = self.height(node.left) if node.left else -1
        right = self.height(node.right) if node.right else -1
        return left - right


if __name__ == "__main__":
    # some demo code to display each of the functions in action
    avl = AVL()
    avl.bulk_insert([5, 3, 2, 7, 34])
    print(avl)
