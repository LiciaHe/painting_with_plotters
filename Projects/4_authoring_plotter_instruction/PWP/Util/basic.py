import pickle,os
'''
Helper functions for 

1. File storage and manipulation 
2. Other common operations

'''

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
def unitConvert(val,unit,unitTo="px",ppi=96):
    '''
    Convert a given value to a different unit settings.

    Args:
        val: value to be converted
        unit: The unit of the given value
        unitTo: The unit to convert to
        ppi: pixel per inch. Default value is 96.


    Returns: The converted value

    '''
    i2cm=ppi/2.54

    unitMap={
        ("inch","px"):ppi,
        ("cm","px"):i2cm,
        ("cm","mm"):10,
        ("mm","px"):i2cm/10,
        ("m","px"):i2cm*100,
        ("inch", "cm"): ppi/i2cm,
        ("inch", "m"): ppi/(i2cm*100),
        ("inch", "mm"): ppi/(i2cm/10),
    }
    unitFrom=unit.lower()
    unitTo=unitTo.lower()
    if unitFrom==unitTo:
        return val
    if (unitFrom,unitTo) in unitMap:
        return unitMap[(unitFrom,unitTo)]*val
    if (unitTo,unitFrom) in unitMap:
        return val/unitMap[(unitTo,unitFrom)]

    print(val,unitFrom,unitTo,ppi, "The given parameters cannot be converted.")

    raise ValueError