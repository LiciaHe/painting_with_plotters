import sys,math
sys.path.insert(1,"../")

from PWP.Generator.RefillGenerator import RefillGenerator
from PWP.Refiller.A3_45mm import A3_45mm
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC

settings={
    "name":"11_refill_test",
    "parameters":{
    },
    "basic_settings":{
        "export_loc": "output/",
        "unit":"inch",
        "width":15,
        "height":11,
        "margins": {"l": 0, "r": 1, "t": 1, "b": 0},
        "tools_ct":5,
        "stroke-width":0.05,
        "script_options":{
            "port":"kitty"
        }
    }
}

class RefillVisualizer(RefillGenerator):

    def create(self):
        '''
        Returns: a list of paths
        '''
        cell_width=self.wh_m[0]/self.tools_ct
        rect_width=cell_width*0.8
        rect_height=self.wh_m[1]*0.8
        gap=cell_width*0.1,self.wh_m[1]*0.1
        paths=[]
        for i in range(self.tools_ct):
            rect=UG.create_rect(
                i*cell_width+gap[0],
                gap[1],
                rect_width,
                rect_height,
                True
            )
            paths.append(
                Path(
                    coordinates=rect,
                    tool_idx=i,
                    filled=True
                )
            )
        return paths


generator=RefillVisualizer(
    settings=settings,
    inktray=A3_45mm(),
    refill_dist=100
)
generator.generate()
