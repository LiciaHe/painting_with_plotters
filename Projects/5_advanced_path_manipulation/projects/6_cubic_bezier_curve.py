import sys,math
sys.path.insert(1,"../")

from PWP.Generator.ScriptGenerator import ScriptGenerator
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC

settings={
    "name":"6_cubic_bezier_curve",
    "parameters":{
    },
    "basic_settings":{
        "export_loc": "output/",
        "unit":"inch",
        "width":8.3,
        "height":11.7,
        "margins": {"l": 1, "r": 1, "t": 1, "b": 1},
        "tools_ct":4,
        "stroke-width":0.05,
        "script_options":{
            "port":"kitty"
        }
    }
}

class PathManipulation(ScriptGenerator):

    def annotate_a_path(self,path_coordinates,tool_idx):
        '''
        Given a path coordinates, create a Path object for the path,
            for each pt in the path, generate a circle object for th path.

        Args:
            path_coordinates:

        Returns: a list of Path objects

        '''
        paths=[
            Path(
                coordinates=path_coordinates,
                tool_idx=tool_idx
            )
        ]
        for pt in path_coordinates:
            circle=UG.create_uniform_polygon(
                x=pt[0],
                y=pt[1],
                r=5,
                side_ct=10,
                closed=True
            )
            paths.append(
                Path(
                    coordinates=circle,
                    tool_idx=tool_idx,
                )
            )
        return paths


    def create_colored_paths(self,list_of_coors,path_storage,filled=False):

        for i,coordinates in enumerate(list_of_coors):
            path_storage.append(
                Path(
                    coordinates=coordinates,
                    tool_idx=i%self.tools_ct,
                    filled=filled
                )
            )
    def create(self):
        '''
        1. Cut a line (2 point) into sections
        2. Cut a path (multiple points) into sections
        3. Boolean Operation
        4. Hatch
        5. Drawing a curve
        Returns: a list of paths
        '''
        paths=[]

        return paths


generator=PathManipulation(
    settings=settings,
    split_to_tool_svgs=False,
    split_to_tool_pys=False
)
generator.generate()
