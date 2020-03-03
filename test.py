from bst import *

bst = BSTRec()
try:
    bst.delete_rec(5)
except ValueError:
    print('deletion from empty tree caught')

try:
    bst.find_next_rec(5)
except ValueError:
    print('find_next from empty tree caught')

print('find_min from empty tree:', bst.find_min_rec())
print('empty tree print:', bst)
