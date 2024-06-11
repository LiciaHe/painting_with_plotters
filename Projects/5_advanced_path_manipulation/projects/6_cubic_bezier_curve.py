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

    def annotate_a_path(self,path_coordinates,tool_idx,path_storage):
        '''
        Given a path coordinates, create a Path object for the path,
            for each pt in the path, generate a circle object for th path.

        Args:
            path_coordinates:

        Returns: a list of Path objects

        '''
        path_storage.append(
            Path(
                coordinates=path_coordinates,
                tool_idx=tool_idx
            ))
        for pt in path_coordinates:
            circle=UG.create_uniform_polygon(
                x=pt[0],
                y=pt[1],
                r=5,
                side_ct=10,
                closed=True
            )
            path_storage.append(
                Path(
                    coordinates=circle,
                    tool_idx=tool_idx,
                )
            )



    def create_colored_paths(self,list_of_coors,path_storage,filled=False):

        for i,coordinates in enumerate(list_of_coors):
            path_storage.append(
                Path(
                    coordinates=coordinates,
                    tool_idx=i%self.tools_ct,
                    filled=filled
                )
            )

    def visualize_skeleton(self,start_pt,cp_0,cp_1,end_pt,path_storage):
        radius=5
        side_ct=10
        for pt in [start_pt,end_pt]:
            path_storage.append(
                Path(UG.create_uniform_polygon(*pt,radius*2,side_ct,True),0,filled=True)
            )
        path_storage.append(
            Path([start_pt,end_pt], 0, filled=False)
        )
        for pt in [cp_0,cp_1]:
            path_storage.append(
                Path(UG.create_uniform_polygon(*pt,radius,side_ct,True),1)
            )
        for line in [[start_pt,cp_0],[end_pt,cp_1]]:
            path_storage.append(
                Path(line, 1, filled=False)
            )
    def create_control_points_by_row(self,row_idx):
        return UG.translate_path(self.control_pts,0,self.cell_height*row_idx)
    def create(self):
        '''
        Returns: a list of paths
        '''
        path_storage=[]
        start_pt=[0,100]
        end_pt=[300,100]
        cp_0=[0,0]
        cp_1=[300,350]

        self.cell_height=200
        self.control_pts=[start_pt,cp_0,cp_1,end_pt]
        # basic visualization
        self.visualize_skeleton(*self.create_control_points_by_row(0), path_storage)

        # produce bezier curve by number of sections
        pts_1=self.create_control_points_by_row(1)
        self.visualize_skeleton(*pts_1, path_storage)
        bc_1=[]
        for i in range(0,105,5):
            t=i/100
            pt=UG.get_cubic_bezier_point_by_t(
                t,
                *pts_1
            )
            bc_1.append(pt)
        self.annotate_a_path(bc_1,2,path_storage)

        # produce bezier curve in relation to length
        pts_2 = self.create_control_points_by_row(2)
        self.visualize_skeleton(*pts_2, path_storage)
        bc_2 = UG.create_cubic_bezier_curves_with_eq_segs(*pts_2,seg_length=20)
        self.annotate_a_path(bc_2, 3, path_storage)




        return path_storage


generator=PathManipulation(
    settings=settings,
    split_to_tool_svgs=False,
    split_to_tool_pys=False
)
generator.generate()
