from avl import AVL
from bst import BST
from arrays import *
import random

'''avl = AVL()
arr = [15, 3, 7, 6, 4, 8, 10, 17, 20, 18, 22, 16]
avl.sort(arr)'''
bst = BST()
arr = get_random_array(20)
print(arr)
bst.sort(arr)
for _ in range(15):
    n = random.choice(arr)
    arr.pop(arr.index(n))
    bst.delete_iter(n)
    print(n, '\n', bst, sep='')