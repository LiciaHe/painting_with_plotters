'''
A class that represent one path in the design. Used to store path (coordinates) and tool (index) together.
'''
from PWP.Util.basic import convert_unit
class Path:
    def __init__(self,coordinates,tool_idx,filled=False):
        '''
        Stores the given information
        Args:
            coordinates: a list of 2d points
            tool_idx: an integer
            filled: a boolean value. By default, False.
        '''
        self.coordinates=coordinates
        self.tool_idx=tool_idx
        self.filled=filled

    def create_margined_unit_path(self,unit_to,margins,overwrite=False):
        '''
        Given a unit to convert to (a string), convert points stored in self.path
        into a path using the given unit.
        For each point, also append the margin.
        Store the value in self.unit_path
        If self.unit_path has been generated, this function will not overwrite the previous result unless overwrite is True.
        Args:
            unit_to: a string: in, cm, or mm.
            margins: a dictionary that contains {"l","r","t,"p"} margin value in px.
            overwrite: whether to overwrite previous values stored in self.unit_path. Default False.

        Returns:

        '''
        if hasattr(self,"unit_path") and not overwrite:
            return

        self.unit_path=[]
        converted_margin={}
        for key in ["l","t"]:
            converted_margin[key]=convert_unit(margins[key],unit="px",unitTo=unit_to)

        for pt in self.coordinates:
            new_pt=[convert_unit(v,unit="px",unitTo=unit_to) for v in pt]
            new_pt[0]+=converted_margin["l"]
            new_pt[1]+=converted_margin["t"]
            self.unit_path.append(new_pt)

