from avl import AVL

avl = AVL()
arr = [15, 3, 7, 6, 4, 8, 10, 17, 20, 18, 22, 16]
avl.sort(arr)
print(avl.height(), avl.height(avl.root.left))