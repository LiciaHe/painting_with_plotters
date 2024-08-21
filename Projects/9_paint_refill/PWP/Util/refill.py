import geometry
from Path import Path
class Inkwell:
    '''
    A class that represent individual inkwell
    '''
    def __init__(self,**kwargs):
        self.paths = None
        self.alt_paths = None

        self.boundary_path = None
        self.bbox = None
        self.center = None

        self.alt_trigger_ct = None
        self.usage_ct = 0

        for key in kwargs:
            setattr(self,key,kwargs[key])


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
        export the boundary paths of all the inkwells (normal inkwells and cleaning stations)

        Returns: inkwell_paths, cleaning_station_paths
        '''
    def __init__(self,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.inkwells=[] #contains only color
        self.cleaning_stations=[]
        self.setup()