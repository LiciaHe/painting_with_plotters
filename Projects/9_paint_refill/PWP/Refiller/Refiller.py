from ..Util import geometry as UG
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
        self.tool_idx=0
        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.boundary_path = Path(
            coordinates=UG.create_rect(*self.bbox,True),
            tool_idx=self.tool_idx
        )
        self.center = UG.get_center_from_wh_bbox(bbox)
        self.margined_bbox=[bbox[0]+self.margin,bbox[1]+self.margin,bbox[2]-2*self.margin,bbox[3]-2*self.margin]
    def translate(self,tx,ty):
        '''
        Translate all location information within this inkwell.
        will update
        1) center,
        2) bbox
        3) boundary_path,
        4) margined_bbox
        5) paths
        6) alt_paths
        Args:
            tx: a value in px
            ty: a value in px

        Returns:

        '''
        self.center[0]+=tx
        self.center[1]+=tx

        self.bbox[0]+=tx
        self.bbox[1]+=ty
        self.boundary_path= Path(
            coordinates=UG.create_rect(*self.bbox,True),
            tool_idx=self.tool_idx
        )
        self.margined_bbox[0]+=tx
        self.margined_bbox[1]+=ty
        for path in self.paths:
            UG.translate_path(
                path.coordinates,
                tx,ty,in_place=True
            )
        for path in self.alt_paths:
            UG.translate_path(
                path.coordinates,
                tx,ty,in_place=True
            )

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
            if stroke_ct == 1:
                y+=h/2
                y_gap=0
            else:
                y_gap=h/(stroke_ct-1)
            x_gap=0
        else:
            if stroke_ct==1:
                x+=w/2
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
            tool_idx=self.tool_idx
        )

    def get_paths(self):
        '''
        Return a list of paths associated with this inkwell.
        If the following 3 criteria are met, return the alt_paths
        1) this inkwell has alt_trigger_ct,
        2) the usage count reaches the trigger ct criteria
        3) the alt paths is not None or empty,

        in other situations, return the paths

        Returns:a list of paths

        '''
        self.usage_ct+=1
        if self.alt_trigger_ct and self.usage_ct%self.alt_trigger_ct==0 and self.alt_paths:
            return self.alt_paths
        return self.paths
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

    def translate(self,tx,ty):
        '''
        Translate all the inkwell and cleaning stations in this tray by a given translation x and translation y.

        will update
        1) center,
        2) bbox
        3) boundary_path,
        4) margined_bbox
        5) paths
        6) alt_paths

        Args:
            tx: a value in px
            ty: a value in px

        Returns:

        '''
        for inkwell in self.inkwells+self.cleaning_stations:
            inkwell.translate(tx,ty)
    def get_paths_by_inkwell_idx(self,idx):
        '''
        Given the index of an inkwell, return the list of paths associated with the inkwell.

        Args:
            idx: index of the inkwell.

        Returns:a list of Paths
        '''
        inkwell=self.inkwells[idx]
        return inkwell.get_paths()

    def get_clean_paths_by_id(self,idx):
        '''
        Given the index of an inkwell, return the list of paths associated with the inkwell.

        Args:
            idx: index of the inkwell.

        Returns:a list of Paths
        '''
        inkwell=self.cleaning_stations[idx]
        return inkwell.get_paths()
    def get_cleaning_paths(self):
        return  self.get_clean_paths_by_id(0)

