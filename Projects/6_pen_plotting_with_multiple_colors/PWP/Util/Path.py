'''
A class that represent one path in the design. Used to store path (coordinates) and tool (index) together.
'''
from PWP.Util.basic import convert_unit
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UCH
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
        self.split_coordinates=[]

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

    def split_to_unit_size(self,unit_size):
        '''
        Ensure the distance between any two adjacent points (in this path) is shorter or equal to the unit_size
        Args:
            unit_size: a number in pixel.

        Returns: None. The new list of coordinates will be stored in self.split_coordinates

        '''
        self.split_coordinates=UG.split_path_by_dist(unit_size)


    def produce_line_fills(self,line_gap,rot_radians,split_to_unit):
        '''
        Assuming self.coordinates stores a closed path, fill the path with lines using the given line_gap and rotation
        Args:
            line_gap:
            rotation:

        Returns:

        '''
        fill_lines=UCH.fill_with_line(
            path=self.coordinates,
            gap=line_gap,
            rot_radians=rot_radians,
        )
        if split_to_unit:
            for i,fl in enumerate(fill_lines):
                fill_lines[i]=UG.split_path_by_dist(fl,split_to_unit)


