import sys,math
sys.path.insert(1,"../")

from PWP.Generator.RefillGenerator import RefillGenerator
from PWP.Refiller.A3_45mm import A3_45mm
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC

settings={
    "name":"10_refill_plan",
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
        return self.create_refill_plan()


generator=RefillVisualizer(
    settings=settings,
    inktray=A3_45mm()
)
generator.generate()
