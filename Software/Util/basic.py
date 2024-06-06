import pickle,os
'''
Helper functions for 

1. File storage and manipulation 
2. Other common operations

'''
### pickle
def load_object(filename):
    '''
    Given a pickle address, load and return it
    Args:
        filename: path to a pickle file

    Returns: the loaded object
    '''

    with open(filename, 'rb') as inputF:
        obj = pickle.load(inputF)
        inputF.close()
    return obj
def save_object(obj, filename):
    '''
    Given a pickle address, store a given object at the address.
    Args:
        obj: object to be stored
        filename: path to a pickle file

    Returns: None
    '''
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
### directory and file
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
def rmfile(filePath):
    '''
    Given a path to a file, try to remove the file. Will catch errors and print them instead of throwing the error.
    Args:
        filePath: path to file

    Returns:

    '''
    try:
        os.remove(filePath)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
def rmdir(directory_path):
    '''
    Given a path to a file, try to remove the file. Will catch errors and print them instead of throwing the error.
    Args:
        directory_path:

    Returns:

    '''
    try:
        os.rmdir(directory_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
### file naming util
def get_slug(input_string):
    '''
    Generate a slug (a string that is lower case, no space, each word joined with "_")
    Useful for generating file names and paths.

    Args:
        input_string: a string

    Returns: Slug: (a string that is lower case, no space, each word joined with "_")

    '''
    return "_".join(input_string.lower().strip().split(" "))

