import sys,math
sys.path.insert(1,"../")

from PWP.Generator.ScriptGenerator import ScriptGenerator
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC

settings={
    "name":"4_cut_and_split",
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
    def test_lines(self,paths):
        line=[[0,0],[self.wh_m[0],0]]
        line_path=Path(
            coordinates=line,
            tool_idx=0
        )
        paths.append(line_path)

        ## cut the path into 4 sections
        four_section_lines=[[0,100],[self.wh_m[0],100]]
        for i in range(4):
            start_pt=UG.get_pt_on_line_by_perc(
                pt0=four_section_lines[0],
                pt1=four_section_lines[1],
                dist_perc=i*0.25
            )
            end_pt=UG.get_pt_on_line_by_perc(
                pt0=four_section_lines[0],
                pt1=four_section_lines[1],
                dist_perc=(i+1)*0.25
            )
            paths.append(
                Path(
                    coordinates=[start_pt,end_pt],
                    tool_idx=i
                )

            )


        # split line into sections shorter than 100px
        line_to_split=UG.translate_path(line,0,200)
        line_splited=UG.split_line_by_dist(*line_to_split,100)
        paths+=self.annotate_a_path(line_splited,1)

        line_to_cut=UG.translate_path(line,0,300)
        line_segments=UG.cut_line_by_dist(*line_to_cut,100)
        self.create_colored_paths(line_segments,paths)

    def test_rectangles_cuts(self,paths):
        rectangle=UG.create_rect(
            0,400,100,100,True
        )
        paths.append(
            Path(
                coordinates=rectangle,
                tool_idx=0
            )
        )

        rect_tx=150
        # split a rectangle into lines shorter than 60 px
        rect_to_split=UG.translate_path(rectangle,rect_tx,0)
        rect_splited=UG.split_path_by_dist(rect_to_split,60)
        paths+=self.annotate_a_path(rect_splited,2)

        # cut a rectangle into lines shorter than 60 px
        rect_to_cut=UG.translate_path(rectangle,rect_tx*2,0)
        rect_cut_segments=UG.cut_path_to_lines_by_dist(rect_to_cut,60)
        self.create_colored_paths(rect_cut_segments, paths)

        #cut a rectangle into paths shorter than 60 px
        rect_to_cut=UG.translate_path(rectangle,rect_tx*3,0)
        rect_cut_segments=UG.cut_path_to_paths_by_dist(rect_to_cut,60)
        self.create_colored_paths(rect_cut_segments, paths)
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
        self.test_lines(paths)
        self.test_rectangles_cuts(paths)

        return paths


generator=PathManipulation(
    settings=settings,
    split_to_tool_svgs=False,
    split_to_tool_pys=False
)
generator.generate()
