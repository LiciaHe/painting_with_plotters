import os
'''
Helper functions for 

1. File storage and manipulation 
2. Other common operations

'''
def mkdir(path):
    '''
    Given a path to a directory location, make a new directory if this path does not exist.
    Args:
        path: path to the directory

    Returns: True if this function made a new directory. Return False if the directory exists.

    '''
    if (not os.path.exists(path)):
        os.mkdir(path)
        return True
    return False
