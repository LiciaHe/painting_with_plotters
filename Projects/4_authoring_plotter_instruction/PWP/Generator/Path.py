'''
A class that represent one path in the design. Used to store path (coordinates) and tool (index) together.
'''
from ..Util.basic import convert_unit
class Path:
    def __init__(self,path,tool_idx,filled=False):
        '''
        Stores the given information
        Args:
            path: a list of 2d points
            tool_idx: an integer
            filled: a boolean value. By default, False.
        '''
        self.path=path
        self.tool_idx=tool_idx
        self.filled=filled
    def convert_to_unit(self,unit_to,overwrite=False):
        '''
        Given a unit to convert to (a string), convert points stored in self.path
        into a path using the given unit.
        Store the value in self.unit_path
        If self.unit_path has been generated, this function will not overwrite the previous result unless overwrite is True.
        Args:
            unit_to: a string: in, cm, or mm.
            overwrite: whether to overwrite previous values stored in self.unit_path. Default False.

        Returns:

        '''
        if hasattr(self,"unit_path") and not overwrite:
            return

        self.unit_path=[]
        for pt in self.path:
            new_pt=[convert_unit(v,unit="px",unitTo=unit_to) for v in pt]
            self.unit_path.append(new_pt)

