'''
Stores utility functions that
1) Create geometries/paths
2) Manipulate geometries/paths
3) Export geometries/paths
4) Calculate values related to geometries
'''
import Util.basic as UB
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
def create_c_bezier_curve_by_angle_dist(start_end,p1_angle_deg,p2_angle_deg,p1_dist_perc,p2_dist_perc):
    '''
    Creating the control points of a cubic bezier curve using rotation and distance.
    Args:
        start_end: A list or tuple of 2 points, starting point and ending point.
        p1_angle_deg:
        p2_angle_deg:
        p1_dist_perc:
        p2_dist_perc:

    Returns:

    '''
### MANIPULATE
def rotate_pt(point, origin, angle_radian,in_place=False):
    '''
        Rotate a point counterclockwise by a given angle around a given origin.
        The angle should be given in radians.
    Args:
        point: A 2d point
        origin: A 2d point to be rotated around
        angle_radian: a radian format angle
        in_place: whether to return a new point or to manipulate the original point. False by default

    Returns: the rotated point.
    '''
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle_radian) * (px - ox) - math.sin(angle_radian) * (py - oy)
    qy = oy + math.sin(angle_radian) * (px - ox) + math.cos(angle_radian) * (py - oy)

    if in_place:
        point[0]=qx
        point[1]=qy
        return point
    else:
        return [qx, qy]
def rotate_path(path,origin, angle_radian,in_place=False):
    '''
    Rotate a path counterclockwise by a given angle around a given origin.
        The angle should be given in radians.
    Args:
        path: A list of 2d points
        origin: A 2d point to be rotated around
        angle_radian: a radian format angle
        in_place: whether to return a new point or to manipulate the original point. False by default

    Returns: the rotated path
    '''
    if in_place:
        for i, pt in enumerate(path):
            path[i]=rotate_pt(pt,origin,angle_radian,in_place)
        return path
    return [rotate_pt(pt,origin,angle_radian,in_place) for pt in path]
def round_pt(point,precision=2,in_place=False):
    '''
    Round a point to the given precision
    Args:
        point: 2d point
        precision: by default, 2
        in_place: whether the action is in place. By default, False

    Returns: a rounded point.
    '''
    if in_place:
        point[0]=round(point[0],precision)
        point[1]=round(point[1],precision)
        return point
    return [round(xy,precision) for xy in point]
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

def translate_pt(pt,tx,ty,in_place=False):
    '''
    Translate a point.
    Args:
        pt: A 2d point
        tx: translation in the x direction
        ty: translation in the y direction
        in_place: Whether the transformation is in place or not. By default, False.

    Returns: the translated point
    '''
    if in_place:
        pt[0]+=tx
        pt[1]+=ty
        return pt
    return [pt[0]+tx,pt[1]+ty]
def translate_path(path,tx,ty,in_place=False):
    '''

    Scale a point according to a given center and scale factors
    Args:
        path: a list of 2d points
        tx: translation in the x direction
        ty: translation in the y direction
        in_place: Whether the transformation is in place or not. By default, False.

    Returns: the translated path.

    '''
    if in_place:
        for i, pt in enumerate(path):
            path[i]=translate_pt(pt,tx,ty,in_place)
        return path
    return [translate_pt(pt,tx,ty,in_place) for pt in path]

### EXPORT

def export_path_to_string(path,closed=False,nestable=False,round_precision=2):
    '''
    Convert a path into a d path string (used for <path> element in svg).

    If the given nestable, will join multiple paths into one
    Args:
        path: [[x,y],[x1,y1]....] for a non-nested path
                If a path is nested, it is [[[x,y],[x1,y1]....],[[xn,yn]...]]
        closed: Whether the given path is a closed shape. If closed, a "Z" would be added to the end.
        nestable: Whether to treat the path as a one-layer path (a list of 2d arrays) or a 2-layer path.
        round_precision: the precision setting for the exported value. By default, round to the 2nd place.

    Returns: A string in the format required for "d" attribute of the <path> element in SVG.
    '''
    if not nestable:
        d_str="M"+" L".join([",".join([str(round(l,round_precision)) for l in xy[:2]]) for xy in path])
        if closed:
            d_str+= "Z"
    else:
        d_str=""
        for pl in path:
            d_str+="M"+" L".join([",".join([str(round(l,round_precision)) for l in xy[:2]]) for xy in pl])
            if closed:
                d_str += "Z"

    return d_str

### CALCULATE/GET
def calc_dist_between_pts(p0, p1):
    '''
    Return the distance between 2 2D points.
    Args:
        p1: [x,y]
        p2: [x,y]

    Returns: distance between p0 and p1

    '''
    return math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)
def calc_path_length(path):
    '''
    Given a path (2D array, not nestable), return the length of this path by calculating the distance between each point.
    Args:
        path: A list of 2D points.

    Returns: Sum of distance between each point in this path (i.e., the length of this path).
    '''
    l=0
    if len(path)<2:
        return l
    for i in range(1,len(path)):
        l+=calc_dist_between_pts(path[i-1],path[i])
    return l
def get_wh_bbox(path):
    '''
    given a path, return the bounding box in the width-height style
    Args:
        path: a list of 2d points

    Returns: (x,y,w,h) of the path.
    '''
    return convert_mmbbox_to_whbbox(get_mm_bbox(path))

def convert_mmbbox_to_whbbox(mm_bbox):
    '''
    Convert a min/max bbox to a width/height bbox
    Args:
        mm_bbox: (min_x,max_x,min_y, max_y)

    Returns: (x,y,w,h)
    '''
    return [mm_bbox[0], mm_bbox[2], mm_bbox[1] - mm_bbox[0], mm_bbox[3] - mm_bbox[2]]
def get_mm_bbox(path):
    '''

    Given a path, return the bounding box in the min-max style.
    Args:
        path: a list of 2d points

    Returns: (min_x,max_x,min_y, max_y) of the path. (0,0,0,0) if the path is empty.

    '''
    if not path:
        return 0, 0, 0, 0

    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    for point in path:
        x, y = point
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    return min_x, min_y, max_x, max_y
def pt_within_bbox(pt,bbox):
    '''
    check if a point is within a given bbox. The bbox is given in a min/max style.
    The boundary values are not included.
        i.e., the point sits on the edge/corner of the bbox is not considered as sitting inside the bbox.
    Args:
        pt: 2d point
        bbox: a min/max style bbox

    Returns: if the point is inside a bbox.
    '''
    min_x,max_x,min_y,max_y=bbox
    return max_x > pt[0] > min_x and max_y > pt[1] > min_y

def calc_polygon_area(path):
    '''
    Calculate the area of a polygon.

    Args:
        path:a list of 2d point. Will be considered as a closed polygon.

    Returns: area of the polygon.

    '''
    n = len(path)
    area = 0

    for i in range(n):
        x1, y1 = path[i]
        x2, y2 = path[(i + 1) % n]
        area += x1 * y2
        area -= y1 * x2

    area = abs(area) / 2.0
    return area
