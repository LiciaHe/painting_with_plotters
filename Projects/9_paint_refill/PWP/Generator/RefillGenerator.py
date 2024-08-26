'''
An extension of ScriptGenerator that handles the generation and storage of scripts that uses the refiller pipeline.

Each project needs to implement the "create()" function.
The "generate()" function processes the information, create svg files for visualization and python script for plotting
'''

from ..Generator.ScriptGenerator import ScriptGenerator
import json
import importlib.resources
from ..Util import basic as UB
from ..Util import geometry as UG
from ..Util.Path import Path
class RefillGenerator(ScriptGenerator):
    path_unit_size=5
    split_paths_to_unit_size=True
    refill_dist=200


    def process_paths(self,paths):
        '''
        Overwrite the function in SvgGenerator so that the list of paths will have refill paths and cleaning paths.
        Args:
            paths: list of paths, obtained from the create() function.

        Returns: None
        '''
        super().process_paths(paths)

        if len(paths)<1:
            return
        path_stack = paths.copy()
        paths.clear()  # will need to update the list in place
        #adds cleaning at the beginning
        if not self.inktray.skip_clean:
            for clean_path in self.inktray.get_cleaning_paths():
                paths.append(clean_path)

        path_stack.reverse()
        current_dist = 0
        pre_tool=None

        while len(path_stack) > 0:
            current_path = path_stack.pop()

            if pre_tool is None:
                pre_tool=current_path.tool_idx
            if pre_tool!=current_path.tool_idx and not self.inktray.skip_clean:
                #needs cleaning
                for clean_path in self.inktray.get_cleaning_paths():
                    paths.append(clean_path)
                current_dist=0
            pre_tool=current_path.tool_idx

            dist_quota = self.refill_dist-current_dist
            break_idx = UG.find_pt_in_path_by_dist(current_path.coordinates, dist_quota)
            if current_path.filled:
                for fill_path_obj in current_path.fill_path_objects:
                    path_stack.append(fill_path_obj)

            if break_idx is None:
                # not breaking
                paths.append(current_path)
                current_dist += UG.calc_path_length(current_path.coordinates)

            else:
                #break into 2 parts
                broken_path_start = Path(
                    coordinates=current_path.coordinates[:break_idx+1],
                    tool_idx=current_path.tool_idx,
                    filled=False
                )
                broken_path_end = Path(
                    coordinates=current_path.coordinates[break_idx:],
                    tool_idx=current_path.tool_idx,
                    filled=False
                )
                paths.append(broken_path_start)
                #adds refill
                for ink_path in self.inktray.get_paths_by_inkwell_idx(current_path.tool_idx):
                    paths.append(ink_path)
                path_stack.append(broken_path_end)
                current_dist=0


    def __init__(self,settings,inktray,**kwargs):
        self.inktray=inktray
        super().__init__(settings=settings, **kwargs)
        self.width=max(self.width,self.inktray.tray_translation[0]+self.inktray.tray_w)
        self.height=max(self.height,self.inktray.tray_translation[1]+self.inktray.tray_h)

        # make sure all inkwell takes the margin into consideration.
        self.inktray.translate(-self.margins["l"],-self.margins["t"])

    # def generate(self):
    #     '''
    #
    #     Returns:
    #
    #     '''
    #     paths=
    #     self.prepare_script_writers()
    #     self.process_and_append_paths_to_script(paths)
    #     self.export_scripts()
    def create_refill_plan(self):
        '''

        visualize the plan of the plot, to include
        1) full plotting area
        2) canvas area
        3) image area
        4) inktray boundaries (of individual inkwells)
        5) inking paths (including alternative paths)
        Returns:
        '''
        full_rect=UG.create_rect(
            -self.margins["l"],
            -self.margins["t"],
            self.width,
            self.height
        )
        canvas_rect=UG.create_rect(
            0,
            0,
            self.wh_m[0],
            self.wh_m[1]
        )
        canvas_rect_with_margin=UG.create_rect(
            -self.margins["l"],
            -self.margins["t"],
            self.wh_m[0]+self.margins["l"]+self.margins["r"],
            self.wh_m[1]+self.margins["t"]+self.margins["b"]
        )
        boundary_paths=[
            Path(coordinates=coor,tool_idx=0) for coor in [full_rect,canvas_rect,canvas_rect_with_margin]
        ]
        inkwell_boundary_paths=[
            inkwell.boundary_path for inkwell in self.inktray.inkwells
        ]
        cleaning_station_boundary_paths=[
            inkwell.boundary_path for inkwell in self.inktray.cleaning_stations
        ]

        for path in cleaning_station_boundary_paths:
            path.tool_idx=0

        inkwell_strokes=[]
        for inkwell in self.inktray.inkwells:
            for path in inkwell.paths:
                inkwell_strokes.append(path)
            for path in inkwell.alt_paths:
                inkwell_strokes.append(path)

        cleaning_station_strokes=[]
        for inkwell in self.inktray.cleaning_stations:
            for path in inkwell.paths:
                cleaning_station_strokes.append(path)
                path.tool_idx=0
            for path in inkwell.alt_paths:
                cleaning_station_strokes.append(path)
                path.tool_idx=0
        paths=boundary_paths+inkwell_boundary_paths+cleaning_station_boundary_paths+inkwell_strokes+cleaning_station_strokes
        return paths