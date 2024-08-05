import sys,math
sys.path.insert(1,"../")

from PWP.Generator.ScriptGenerator import ScriptGenerator
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC

settings={
    "name":"8_split_by_color",
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

    def create(self):
        '''
        1. work on the filled path
        Returns: a list of paths
        '''
        path_storage=[]
        w=self.wh_m[0]
        h=self.wh_m[1]
        rect = UG.create_rect(
            0, 0, w, h, True
        )
        path_storage.append(
            Path(
                coordinates=rect,
                tool_idx=0,
                filled=True
            )
        )

        return path_storage


generator=PathManipulation(
    settings=settings,
    split_to_tool_svgs=True,
    split_to_tool_pys=True
)
generator.generate()
