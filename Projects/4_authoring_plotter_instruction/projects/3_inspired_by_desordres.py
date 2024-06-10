import sys
sys.path.insert(1,"../")

from PWP.Generator.ScriptGenerator import ScriptGenerator
from PWP.Util.Path import Path
from PWP.Util import geometry as UG

settings={
    "name":"3_inspired_by_desordres",
    "parameters":{
        "col_ct":[5,10],
        "row_ct":[10,15],
        "rect_per_cell":[3,10],
        "size_scale":[0.7,0.9],

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

class RectInGrid(ScriptGenerator):
    def create(self):
        '''
        Generate many rectangles in a grid system.

        Returns: a list of paths
        '''
        col_ct=int(self.get_random_value_from_parameters("col_ct"))
        row_ct=int(self.get_random_value_from_parameters("row_ct"))
        cell_width=self.wh_m[0]/col_ct
        cell_height=self.wh_m[1]/row_ct
        paths=[]
        for i in range(col_ct):
            x=i*cell_width
            for j in range(row_ct):
                y=j*cell_height
                rect=UG.create_rect(x,y,cell_width,cell_height,True)
                path=Path(
                    coordinates=rect,
                    tool_idx=self.get_random_tool_idx()
                )
                paths.append(path)

                center=x+cell_width/2,y+cell_height/2
                scale=1
                rep_ct=int(self.get_random_value_from_parameters("rect_per_cell"))

                for rc in range(rep_ct):
                    scale*=self.get_random_value_from_parameters("size_scale")
                    new_rect=UG.scale_path(
                            rect,
                            scale_x=scale,
                            scale_y=scale,
                            scale_center=center,
                            in_place=False
                        )
                    paths.append(
                        Path(
                            coordinates=new_rect,
                            tool_idx=self.get_random_tool_idx()
                        )
                    )
        return paths




generator=RectInGrid(
    settings=settings,
    split_to_tool_svgs=True,
    split_to_tool_pys=True
)
generator.generate()
