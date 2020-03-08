from bst import BST
from avl import AVL
from arrays import *
from datetime import *

if __name__ == "__main__":
    random_arr = get_random_array(10000)  # works up to 10mil on my PC
    sorted_arr = get_sorted_array(10000)
    bst = BST()
    avl = AVL()

    try:
        bst.bulk_insert(random_arr, True)
        print("BST random recursive success")
    except RecursionError:
        print("Maximum recursion depth exceeded for bst random recursive")
    bst.clear()
    print()

    now = datetime.now()
    bst.bulk_insert(random_arr)
    print("BST random iterative success")
    print(bst.traversal_counter, "traversals to insert")
    bst.bulk_delete(random_arr)
    print(f"{len(random_arr)} insert/delete on BST random took", datetime.now() - now)
    bst.clear()
    print()

    # at the time of writing, there is no AVL recursive implementation
    '''    
    try:
        avl_random.bulk_insert(random_arr, True)
        print("AVL random recursive success")
    except RecursionError:
        print("Maximum recursion depth exceeded for avl random recursive")
    avl.clear()
    print()
    '''

    now = datetime.now()
    avl.bulk_insert(random_arr)
    print("AVL random iterative success")
    print(avl.traversal_counter, "traversals to insert")
    avl.bulk_delete(random_arr)
    print(f"{len(random_arr)} insert/delete on AVL random took", datetime.now() - now)
    avl.clear()
    print()

    try:
        bst.bulk_insert(sorted_arr, True)
        print("BST sorted recursive success")
    except RecursionError:
        print("Maximum recursion depth exceeded for bst sorted recursive")
    bst.clear()
    print()

    now = datetime.now()
    bst.bulk_insert(sorted_arr)
    print("BST sorted iterative success")
    print(bst.traversal_counter, "traversals to insert")
    bst.bulk_delete(sorted_arr)
    print(f"{len(sorted_arr)} insert/delete on BST sorted took", datetime.now() - now)
    bst.clear()
    print()

    # at the time of writing, there is no AVL recursive implementation
    '''    
    try:
        avl_random.bulk_insert(sorted_arr, True)
        print("AVL sorted recursive success")
    except RecursionError:
        print("Maximum recursion depth exceeded for avl sorted recursive")
    avl.clear()
    print()
    '''

    now = datetime.now()
    avl.bulk_insert(sorted_arr)
    print("AVL sorted iterative success")
    print(avl.traversal_counter, "traversals to insert")
    avl.bulk_delete(sorted_arr)
    print(f"{len(sorted_arr)} insert/delete on AVL sorted took", datetime.now() - now)
    avl.clear()
