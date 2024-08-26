from ..Util import geometry
from ..Util.Path import Path
from ..Util import basic
class Inkwell:
    '''
    A class that represent individual inkwell
    '''
    def __init__(self,bbox,**kwargs):
        self.paths = []
        self.alt_paths = []
        self.alt_trigger_ct = None
        self.usage_ct = 0
        self.bbox = bbox
        self.margin=0
        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.boundary_path = Path(
            coordinates=geometry.create_rect(*self.bbox),
            tool_idx=None
        )
        self.center = geometry.get_center_from_wh_bbox(*bbox)
        self.margined_bbox=[bbox[0]+self.margin,bbox[1]+self.margin,bbox[2]-2*self.margin,bbox[3]-2*self.margin]


    def produce_ink_path(self,stroke_ct,stroke_direction):
        '''
        Assuming the bbox is associated with self, produce a Path object that goes through the margined boundary shape.

        Args:
            stroke_ct: the number of strokes in the path. If stroke_ct =1 , it's a line that goes through the center of the boundary shape
            stroke_direction: horizontal "hor" or "vertical" for vertical

        Returns: A Path object.
        '''
        coordinates=[]
        x,y,w,h=self.margined_bbox
        if stroke_direction=="hor":
            y_gap=h/(stroke_ct-1)
            x_gap=0
        else:
            x_gap=w/(stroke_ct-1)
            y_gap=0
        for i in range(stroke_ct):
            if stroke_direction=='hor':
                line=[
                   [x,i*y_gap+y],
                    [x+w,i*y_gap+y]
                ]
            else:
                line=[
                    [x+i*x_gap,y],
                    [x+i*x_gap,y+h]
                ]
            if i%2==0:
                line.reverse()
            coordinates+=line

        return Path(
            coordinates=coordinates,
            tool_idx=None
        )


class InkTray:
    '''
    a collection of inkwells
    '''
    def setup(self):
        '''
        Used by individual tray to set up the tray.
        Called by the init function
        @return:
        '''
        raise NotImplementedError
    def export_boundary_paths(self):
        '''
        export the boundary paths (Path Objects) of all the inkwells (normal inkwells and cleaning stations)

        Returns: inkwell_paths, cleaning_station_paths
        '''
        inkwell_paths=[]
        cleaning_station_paths=[]

    skip_clean=False
    # full_w=17
    # full_h=11
    # canvas_w=15
    # canvas_h=11
    m = basic.convert_unit(0.35, 'inch')


    def __init__(self,**kwargs):

        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.inkwells=[] #contains only color
        self.cleaning_stations=[]
        self.setup()