import sys,math
sys.path.insert(1,"../")

from PWP.Generator.ScriptGenerator import ScriptGenerator
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC

settings={
    "name":"8_hatch",
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
        h=self.wh_m[1]/2
        for i in range(2):
            rect = UG.create_rect(
                0, h*i, w, h, True
            )
            path=Path(
                    coordinates=rect,
                    tool_idx=i,
                    filled=True
            )
            if i==1:
                path.line_gap=10

            path_storage.append(path)
        return path_storage


generator=PathManipulation(
    settings=settings,
    split_to_tool_svgs=False,
    split_to_tool_pys=False,
    split_paths_to_unit_size=False
)
generator.generate()
