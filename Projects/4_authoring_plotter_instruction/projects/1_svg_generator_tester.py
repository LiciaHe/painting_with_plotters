import sys
sys.path.insert(1,"../")

from PWP.Generator.SvgGenerator import SvgGenerator
from PWP.Util import geometry as UG
settings={
    "name":"1_svg_tester",
    "parameters":{
        "test_rg":[3,5]
    },
    "basic_settings":{
        "export_loc": "output/",
        # for generating svg
        "unit":"inch",
        "width":8.3,
        "height":11.7,
        "margins": {"l": 1, "r": 1, "t": 1, "b": 1},
        #
        "tools_ct":4,
        "stroke-width":0.05,
    }
}
generator=SvgGenerator(settings=settings)
print(generator.init_svg(additional_name="test"))
rect_pts=UG.create_rect(
    0,0,generator.wh_m[0],generator.wh_m[1],True
)
print(rect_pts)
generator.add_path_to_svg(0,rect_pts,0)
generator.export_svgs()

