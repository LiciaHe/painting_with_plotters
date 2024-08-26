import sys,math,random
sys.path.insert(1,"../")

from PWP.Generator.RefillGenerator import RefillGenerator
from PWP.Refiller.A3_45mm import A3_45mm
from PWP.Util.Path import Path
from PWP.Util import geometry as UG
from PWP.Util import clipper_helper as UC


settings={
    "name":"12_color_blend",
    "parameters":{
        "col_ct":[10,20],
        "row_ct":[5,15],
        "rot_radians":[-6.28,6.28],
        "highlight_rate":0.1,

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
    color_weight=[10,5,3,2,1]
    def get_random_tool_idx(self):
        return random.choices(range(self.tools_ct),weights=self.color_weight)[0]

    def fill_evenly(self,rect,paths):
        '''
        Fill the path with lines evenly.
        Args:
            rect:
            path:

        Returns:
        '''
        paths.append(Path(
            coordinates=rect,
            tool_idx=self.get_random_tool_idx(),
            filled=True
        ))
    def fill_by_half(self,rect,paths):
        lines=UC.fill_with_line(
            rect,
            self.stroke_width,
            rot_radians=self.get_random_value_from_parameters("rot_radians")
        )
        half_idx=int(len(lines)/2)
        paths.append(
            Path(rect,self.get_random_tool_idx(),False)
        )
        two_colors=[self.get_random_tool_idx() for i in range(2)]
        for i,line in enumerate(lines):
            if i <half_idx:
                t=two_colors[0]
            else:
                t=two_colors[1]
            paths.append(
                Path(line,t,False)
            )

    def fill_by_random(self,rect,paths):
        lines=UC.fill_with_line(
            rect,
            self.stroke_width,
            rot_radians=self.get_random_value_from_parameters("rot_radians")
        )
        paths.append(
            Path(rect,self.get_random_tool_idx(),False)
        )
        for i, line in enumerate(lines):
            paths.append(
                Path(line, self.get_random_tool_idx(), False)
            )

    def gap_fill_with_highlight(self,rect,paths):
        lines=UC.fill_with_line(
            rect,
            random.choice(self.line_gaps),
            rot_radians=self.get_random_value_from_parameters("rot_radians")
        )
        t=self.get_random_tool_idx()
        paths.append(
            Path(rect,t,False)
        )
        for i, line in enumerate(lines):
            lt=t
            if random.random()<self.get_value_from_parameters("highlight_rate"):
                lt=self.get_random_tool_idx()
            paths.append(
                Path(line,lt, False)
            )

    def create(self):
        '''
        Fill the space with rectangles. Each fill with different methods
        '''
        rects=[]
        paths=[]
        col_ct=int(self.get_random_value_from_parameters("col_ct"))
        row_ct=int(self.get_random_value_from_parameters("row_ct"))
        cell_wh=self.wh_m[0]/col_ct,self.wh_m[1]/row_ct
        self.line_gaps = [self.stroke_width,self.stroke_width*2,self.stroke_width*3,self.stroke_width*0.75]
        fill_funcs=[
            self.fill_evenly,
            self.fill_by_random,
            self.fill_by_half,
            self.gap_fill_with_highlight
        ]
        for i in range(col_ct):
            for j in range(row_ct):
                rect=UG.create_rect(i*cell_wh[0],j*cell_wh[1],cell_wh[0],cell_wh[1],True)
                rects.append(rect)
        random.shuffle(rects)
        for rect in rects:
            func=random.choice(fill_funcs)
            func(rect,paths)

        return paths


generator=RefillVisualizer(
    settings=settings,
    inktray=A3_45mm(),
    seed="test"
)
generator.generate()
