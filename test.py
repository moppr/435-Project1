from bst import BST

bst = BST()
bst.sort([15, 3, 7, 6, 4, 8, 10, 17, 20, 18, 22, 16])
bst.delete_iter(8)
bst.delete_iter(10)
print(bst)
