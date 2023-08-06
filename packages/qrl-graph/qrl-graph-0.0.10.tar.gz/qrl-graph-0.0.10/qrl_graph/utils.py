import numpy as np
import random
# the utils function 


##### utils function to construct the graph #####
# graph construction (glued tree)
def contruct_tree_graph(h):
    """contruct the graph for the balanced binary tree with height of h.

    Args:
        h (int): the height of the tree
        
    Returns:
        g (np.array): the graph of the tree
        list_child (list): the index of last layers of the tree
    """
    g = np.zeros((2**h-1, 2**h-1))
    index = 0
    list_parent = []
    list_parent.append(index)
    for _ in range(h-1):
        list_child = []
        for parent in list_parent:
            g[parent, index+1] = 1
            g[parent, index+2] = 1
            list_child.append(index+1)
            list_child.append(index+2)
            index += 2
        list_parent = list_child
    
    g = g + g.T
    return g, list_child

def generate_two_cycles(n):
    """construct the two cycles between the two list of length n.
    
    Args:
        n (int): the length of the two cycles.
        
    Returns:
        list_first_perm (list): the permutation of the first cycles.
        list_second_perm (list): the permutation of the second cycles.
    """

    list_first_perm = list(np.random.permutation(n))
    list_second_perm = []

    list_available = list(range(n))


    # the last element of the first perm must be in the entries before
    index_for_last = random.choice(range(n-1))
    list_available.remove(list_first_perm[-1])

    for i in range(n):
        if i == index_for_last:
            list_second_perm.append(list_first_perm[-1])
        else: 
            # one restriction (can not repeat the first cycle)
            list_available_i = [a for a in list_available if a != list_first_perm[i]]
            index = random.choice(list_available_i)
            list_available.remove(index)
            list_second_perm.append(index)

    return list_first_perm, list_second_perm

def contruct_glued_tree_graph(h):
    """contruct the graph for the balanced binary tree with height of h.

    Args:
        h (int): the height of the tree
    """
    n = 2**h-1

    # number of layer double! 
    g = np.zeros((2*n, 2*n))
    g_tree, list_nodes_left = contruct_tree_graph(h)
    
    # reflection (last layer)
    list_nodes_right = [ 2*n-1-i for i in list_nodes_left]
    
    for i in range(n):
        for j in range(n):
            g[i, j] = g_tree[i, j]
            # reflection (binary tree)
            g[2*n-1-i, 2*n-1-j] = g_tree[i, j]
        
    # build the random connection between the two last nodes of the trees. 
    list_perms = generate_two_cycles(len(list_nodes_left))
    
    for perm in list_perms:
        for i, j in enumerate(perm):
            g[list_nodes_left[i], list_nodes_right[j]] = 1
            g[list_nodes_right[j], list_nodes_left[i]] = 1
    
    return g


# numbers 
def array2binary(array):
    """Convert the array to binary.
    
    Args:
        array: the array to be converted.
    
    Returns:
        int: the binary representation of the array.
    """
    return int(''.join(map(lambda x: str(int(x)), array)), 2)

