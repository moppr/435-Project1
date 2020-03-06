from bst import BST
from avl import AVL
from arrays import *

if __name__ == "__main__":
    random_arr = get_random_array(100000)  # works for 10mil on my PC
    sorted_arr = get_sorted_array(10000)
    bst = BST()
    avl = AVL()

    try:
        bst.bulk_insert(random_arr, True)
        print("bst random recursive success")
    except RecursionError:
        print("Maximum recursion depth exceeded for bst random recursive")
    bst.clear()

    try:
        bst.bulk_insert(random_arr)
        print("bst random iterative success")
    except RecursionError:
        print("Maximum recursion depth exceeded for bst random iterative")
    bst.clear()

    # at the time of writing, there is no AVL recursive implementation
    '''    
    try:
        avl_random.bulk_insert(random_arr, True)
        print("avl random recursive success")
    except RecursionError:
        print("Maximum recursion depth exceeded for avl random recursive")
    avl.clear()
    '''
    try:
        avl.bulk_insert(random_arr)
        print("avl random iterative success")
    except RecursionError:
        print("Maximum recursion depth exceeded for avl random iterative")
    avl.clear()

    try:
        bst.bulk_insert(sorted_arr, True)
        print("bst sorted recursive success")
    except RecursionError:
        print("Maximum recursion depth exceeded for bst sorted recursive")
    bst.clear()

    try:
        bst.bulk_insert(sorted_arr)
        print("bst sorted iterative success")
    except RecursionError:
        print("Maximum recursion depth exceeded for bst sorted iterative")
    bst.clear()

    # at the time of writing, there is no AVL recursive implementation
    '''    
    try:
        avl_random.bulk_insert(sorted_arr, True)
        print("avl sorted recursive success")
    except RecursionError:
        print("Maximum recursion depth exceeded for avl sorted recursive")
    avl.clear()
    '''
    try:
        avl.bulk_insert(sorted_arr)
        print("avl sorted iterative success")
    except RecursionError:
        print("Maximum recursion depth exceeded for avl sorted iterative")
    avl.clear()
