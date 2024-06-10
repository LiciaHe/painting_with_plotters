'''
Stores utility functions that
1) Create geometries/paths
2) Manipulate geometries/paths
3) Export geometries/paths
4) Calculate values related to geometries
'''
from ..Util import basic as UB
import math


### CREATE
def create_rect(x,y,w,h,closed=False):
    '''
    Return a path of a rectangle. Starting from top left corner and going clockwise.
    Args:
        x: top left
        y: top left
        w: width
        h: height
        closed: whether the rectangle path is closed (5 pts, including the repeating top left point) or not (4 pts)
    Returns: a list of 2d points.
    '''

    pts=[[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
    if closed:
        pts.append([x,y])
    return pts
### MANIPULATE
def scale_pt(point,scale_x,scale_y,scale_center,in_place=False):
    '''
    Scale a point according to a given center and scale factors
    Args:
        point: a 2d point
        scale_x: scale factor in the x direction.
        scale_y: scale factor in the y direction.
        scale_center: center of this scaling operation. A 2d point.
        in_place: Whether the transformation is in place or not. By default, False.

    Returns: the scaled point.

    '''

    scaled_pt=[point[0]*scale_x,point[1]*scale_y]
    translateX=(1-scale_x)*scale_center[0]
    translateY=(1-scale_y)*scale_center[1]
    x=scaled_pt[0]+translateX
    y=scaled_pt[1]+translateY
    if in_place:
        point[0]=x
        point[1]=y
        return point
    return [x,y]
def scale_path(path,scale_x,scale_y,scale_center,in_place=False):
    '''

    Scale a path according to a given center and scale factors
    Args:
        path: a list of 2d points
        scale_x: scale factor in the x direction.
        scale_y: scale factor in the y direction.
        scale_center: center of this scaling operation. A 2d point.
        in_place: Whether the transformation is in place or not. By default, False.

    Returns: the scaled path.

    '''
    if in_place:
        for i, pt in enumerate(path):
            path[i]=scale_pt(pt,scale_x,scale_y,scale_center,in_place)
        return path
    return [scale_pt(pt,scale_x,scale_y,scale_center,in_place) for pt in path]
