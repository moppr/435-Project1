from bst import BST

bst = BST()
arr = [15, 3, 7, 6, 4, 8, 10, 17, 20, 18, 22, 16]
bst.sort(arr)
bst.delete_iter(6)
print(bst)
