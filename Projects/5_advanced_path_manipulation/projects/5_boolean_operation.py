import sys,math
sys.path.insert(1,"../")

from PWP.Generator.ScriptGenerator import ScriptGenerator
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC

settings={
    "name":"5_boolean_operation",
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

    def test_boolean(self,path_storage):
        rectangle=UG.create_rect(
            0,0,80,80,True
        )
        hexagon=UG.create_uniform_polygon(
            50,0,45,6,True
        )
        path_storage.append(
            Path(
                coordinates=rectangle,
                tool_idx=0
            )
        )
        path_storage.append(
            Path(
                coordinates=hexagon,
                tool_idx=1
            )
        )
        cell_w=120
        clip_types=["intersection","union","difference","xor"]
        for i, ct in enumerate(clip_types):
            tx=(i+1)*cell_w
            subj=UG.translate_path(rectangle,tx,0)
            clip=UG.translate_path(hexagon,tx,0)
            clipper_results=UC.make_clipper(
                subj_path=subj,
                clip_path=clip,
                clipper_type_string=ct
            )
            self.create_colored_paths(clipper_results,path_storage,filled=True)

    def test_hatch(self,path_storage):

        coordinates=[]
        circle=UG.scale_path(UG.create_uniform_polygon(50,200,50,30,True),scale_x=1.1,scale_y=0.9,scale_center=[50,200])
        path_storage.append(
            Path(
                circle,
                0
            )
        )
        cell_width=220
        cell_height=200
        coordinates.append(circle)

        # produce bounding box and larger bounding box
        c1=UG.translate_path(circle,cell_width,0)
        # create bounding box
        bbox=UG.get_wh_bbox(c1)
        # x,y,w,h=bbox
        bbox_rect=UG.create_rect(*bbox,True)

        #create a larger bbox
        max_wh=max(bbox[2:])*2**0.5
        lg_bbox=UG.get_wh_bbox_from_center(
            center=UG.get_center_from_wh_bbox(bbox),
            width=max_wh,
            height=max_wh,
        )
        lg_rect=UG.create_rect(*lg_bbox,True)
        coordinates.append(c1)
        coordinates.append(bbox_rect)
        coordinates.append(lg_rect)

        # fill the larger box with lines

        c2=UG.translate_path(circle,cell_width*2,0)
        lg_rect2=UG.translate_path(lg_rect,cell_width,0)
        coordinates.append(c2)
        coordinates.append(lg_rect2)


        lines=[]
        line=[lg_rect2[0],lg_rect2[1]]

        box_center=UG.get_center_of_path(lg_rect2)
        gap=10
        rot_radians=math.radians(120)
        lines.append(
            UG.rotate_path(line,origin=box_center,angle_radian=rot_radians)
        )


        rep_ct=math.ceil(lg_bbox[3]/gap)
        for i in range(rep_ct):
            line=UG.translate_path(line,0,gap)
            lines.append(UG.rotate_path(line,origin=box_center,angle_radian=rot_radians))

        coordinates+=lines

        c3=UG.translate_path(circle,0,cell_height,False)
        fill_lines=UC.fill_with_line(
            path=c3,
            gap=gap,
            rot_radians=rot_radians,
        )
        coordinates+=fill_lines

        self.create_colored_paths(coordinates,path_storage)

        c4=UG.translate_path(circle,cell_width,cell_height,False)
        fill_lines_4=UC.fill_with_line(
            path=c4,
            gap=self.stroke_width,
            rot_radians=rot_radians,
        )
        for l in fill_lines_4:
            path_storage.append(
                Path(l,0)
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
        self.test_boolean(paths)
        self.test_hatch(paths)

        return paths


generator=PathManipulation(
    settings=settings,
    split_to_tool_svgs=False,
    split_to_tool_pys=False
)
generator.generate()
