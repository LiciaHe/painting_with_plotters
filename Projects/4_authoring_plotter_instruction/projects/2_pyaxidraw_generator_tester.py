import sys
sys.path.insert(1,"../")

from PWP.Generator.ScriptGenerator import ScriptGenerator
from PWP.Util import geometry as UG
from PWP.Generator.Path import Path

settings={
    "name":"2_pyaxidraw_tester",
    "parameters":{
        "test_rg":[3,5]
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

#
# generator=SvgGenerator(settings=settings)
# print(generator.init_svg(additional_name="test"))
# rect_pts=UG.create_rect(
#     0,0,generator.wh_m[0],generator.wh_m[1],True
# )
# print(rect_pts)
# generator.add_path_to_svg(0,rect_pts,0)
# generator.export_svgs()
#
class PipelineTester(ScriptGenerator):
    def create(self):
        boundary_rect=UG.create_rect(
            0,0,self.wh_m[0],self.wh_m[1],True
        )
        rect_1=UG.create_rect(
            30,30,self.wh_m[0]-60,self.wh_m[1]-60,True
        )
        path_0=Path(
            path=boundary_rect,
            tool_idx=0,
            filled=False
        )
        path_1=Path(
            path=rect_1,
            tool_idx=1,
            filled=True
        )
        return [path_0,path_1]

generator=PipelineTester(
    settings=settings,
    split_to_tool_svgs=False,
    split_to_tool_pys=True
)
generator.generate()