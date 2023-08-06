# the utils function 






# numbers 
def array2binary(array):
    """Convert the array to binary.
    
    Args:
        array: the array to be converted.
    
    Returns:
        int: the binary representation of the array.
    """
    return int(''.join(map(lambda x: str(int(x)), array)), 2)

