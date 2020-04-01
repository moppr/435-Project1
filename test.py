from avl import AVL
from bst import BST
from arrays import *
from datetime import *

bst = BST()
avl = AVL()
arr = get_random_array(15)

bst.sort(arr)
bst.display()
avl.sort(arr)
avl.display()
