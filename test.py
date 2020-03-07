from avl import AVL
from bst import BST
from arrays import *
import random

bst = BST()
avl = AVL()
#arr = [63, 20, 65, 46, 48, 3, 62]
arr = get_random_array(31)
print(arr)


avl.sort(arr)
for _ in range(29):
    n = random.choice(arr)
    arr.pop(arr.index(n))
    avl.delete_iter(n)
    print(n, '\n', avl.root.display(), sep='')


'''avl.sort(arr)
avl.root.display()
print('height:', avl.root.height)'''


# confirms that tree is the height it claims to be
'''node = avl.root
while node:
    print(node, node.height, '>', avl.height(node.left), avl.height(node.right))
    node = node.right if avl.height(node.right) > avl.height(node.left) else node.left'''

'''print('deleting', arr[62])
avl.delete_iter(arr[62])
print(avl)
print('height:', avl.root.height)'''

'''for _ in range(100):
    n = random.choice(arr)
    arr.pop(arr.index(n))
    avl.delete_iter(n)
    print(n, avl, avl.root.height if avl.root else -1, sep='\n')'''

'''avl.verify_height()
print(avl.height_manual())
'''

'''avl.insert_iter(5)
print(avl, avl.root.height)
avl.insert_iter(10)
print(avl, avl.root.height)
avl.insert_iter(3)
print(avl, avl.root.height)
avl.insert_iter(15)
print(avl, avl.root.height)
avl.insert_iter(25)
print(avl, avl.root.height)

print(avl.root.left.left, avl.root.left, avl.root, avl.root.right, avl.root.right.right)'''