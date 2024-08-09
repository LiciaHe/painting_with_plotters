import sys,math
sys.path.insert(1,"../")

from PWP.Generator.ScriptGenerator import ScriptGenerator
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC

settings={
    "name":"9_split_by_dist",
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
    def line_test(self):
        path_storage=[]
        # w=self.wh_m[0]
        # h=self.wh_m[1]
        line_gap=10

        # self.hatch_rotation_range=(0,0)
        # total_hatch_line=h/10
        # self.max_dist_per_file=total_hatch_line/2*self.wh_m[0] #only impact tool svg and tool path
        #
        # rect = UG.create_rect(
        #     0, 0, w, h, True
        # )
        line_gap=10
        rep_ct=10*10
        for i in range(rep_ct):
            path= Path(
                coordinates=[[0,i*line_gap],[self.wh_m[0],i*line_gap]],
                tool_idx=0,
                filled=False,
            )
            path_storage.append(path)

        self.max_dist_per_file=self.wh_m[0]*rep_ct/4 #only impact tool svg and tool path
        return path_storage

    def filled_rect_test(self):

        rect = UG.create_rect(
            0, 0, self.wh_m[0], self.wh_m[1], True
        )
        line_gap=10
        path = Path(
            coordinates=rect,
            tool_idx=0,
            filled=True,
            line_gap=line_gap
        )
        self.max_dist_per_file = self.wh_m[0]*self.wh_m[1]/line_gap/2
        return [path]


    def create(self):
        '''
        Returns: a list of paths
        '''
        return self.filled_rect_test()


generator=PathManipulation(
    settings=settings,
    split_to_tool_svgs=True,
    split_to_tool_pys=False,
    split_paths_to_unit_size=False
)
generator.generate()
