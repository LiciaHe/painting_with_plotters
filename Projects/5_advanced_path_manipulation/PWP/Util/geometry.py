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
def create_uniform_polygon(x,y,r,side_ct,closed=False):
    '''
     Return a path of a uniform polygon.
     The polygon is generated by rotation.
      Starting from right point and going clockwise.
    Args:
        x: center x
        y: center y
        r: radius
        side_ct: integer. Number of sides
        closed: whether the rectangle path is closed

    Returns: a path of a uniform polygon.
    '''
    polygon = []
    for i in range(side_ct):
        polygon.append([
            x+r * math.cos(2 * math.pi * i / side_ct),
            y+r * math.sin(2 * math.pi * i / side_ct)
        ])
    if closed:
        polygon.append(polygon[0].copy())
    return polygon
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
def rotate_line_by_center(line,angle_radian,in_place=False):
    '''
    Rotate a line based on its center
    Args:
        line: 2 points
        angle_radian: an angle in radians.
        in_place: whether the operation happens in place. False by default.

    Returns:a rotated line
    '''
    pt0,pt1=line
    center=pt1[0]-pt0[0],pt1[1]-pt0[0]

    return rotate_path(line,center,angle_radian,in_place)
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

###CALCULATE/GET
def get_pt_on_line_by_perc(pt0,pt1,dist_perc):
    '''
    Given two point, pt0 and pt1, find pt2 on line [pt0 pt1] so that ratios of their distances is the dist_perc
        dist(pt2, pt0)/dist(pt1,pt0)= dist_perc
    Args:
        pt0: a 2D pt. Start point.
        pt1: a 2D pt
        dist_perc: a number. If equals to 0, a copy of pt0 is returned. If equals to 1, a copy of pt1 is returned.
                    Can be negative or bigger than 1.

    Returns: A new point on the same line that makes dist(pt2, pt0)/dist(pt1,pt0)= dist_perc
    '''

    v=[pt1[0]-pt0[0],pt1[1]-pt0[1]]
    return [pt0[i]+dist_perc*v[i] for i in range(2)]
def get_pt_on_line_by_dist(pt0,pt1,dist):
    '''
    Given two point, pt0 and pt1, find pt2 on line [pt0 pt1] so that
        dist(pt2, pt0)=dist
    Args:
        pt0: a 2D pt. Start point.
        pt1: a 2D pt
        dist: the distance (directed like vector) between pt0 and the target point (pt2). Can be negative or larger than
                the distance between p0 and p1. If equals to 0 or the distance between pt0 and pt1 is 0, return a copy of pt0.

    Returns: A new point so that dist(pt2, pt0)=dist
    '''

    if dist==0:
        return pt0.copy()
    full_dist=math.dist(pt0,pt1)
    if full_dist==0:
        return pt0.copy()

    dist_perc=dist/full_dist

    return get_pt_on_line_by_perc(pt0,pt1,dist_perc)
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
        l+=math.dist(path[i-1],path[i])
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

    return min_x, max_x, min_y, max_y
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
def get_center_from_wh_bbox(wh_bbox):
    '''
    Given a bounding box in the width/height format, return its center.
    Args:
        wh_bbox: [x,y,w,h]

    Returns: center of the bounding box (a 2d point)

    '''
    x,y,w,h=wh_bbox
    return [x+w/2,y+h/2]
def get_wh_bbox_from_center(center,width,height):
    '''
    Given a center (x,y) and width, height, calculate the x and y.
    Args:
        center: x,y
        width: a number
        height: a number

    Returns: x,y,w,h
    '''
    return [center[0]-width/2,center[1]-height/2,width,height]
def get_center_of_path(path):
    '''
    Calculate the center of a path
    Args:
        path: a list of 2D coordinates

    Returns: center of the bounding box (a 2d point)

    '''
    wh_bbox=get_wh_bbox(path)
    return get_center_from_wh_bbox(wh_bbox)

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

### SPLIT AND CUT
def split_line_by_dist(start_pt,end_pt,dist_lim):
    '''
    Given a line, adding additional points to the line so no line segment within the line is longer than dist_lim

    Args:
        start_pt: a 2 points.
        end_pt: a 2 points.
        dist_lim: the maximum length of any given line segment in the new path.

    Returns: a new path is the same geometry with the given path, but none of the line segment with the new path is longer than the given dist limitation.
    '''
    line_length=math.dist(start_pt,end_pt)
    if line_length<dist_lim:
        return [start_pt.copy(),end_pt.copy()]

    new_path=[start_pt.copy()]
    seg_ct = math.ceil(line_length / dist_lim)
    for i in range(seg_ct):
        pt=get_pt_on_line_by_dist(
            pt0=start_pt,
            pt1=end_pt,
            dist=min(line_length,dist_lim*(i+1)))
        new_path.append(pt)
    return new_path

def cut_line_by_dist(start_pt,end_pt,dist_lim):
    '''
    Given a line, cut it into sections so that no section is longer than dist_lim

    Args:
        start_pt: a 2 points.
        end_pt: a 2 points.
        dist_lim: the maximum length of any given line segment in the new path.

    Returns: a list of lines, none of which is longer than dist_lim
    '''
    line_split=split_line_by_dist(start_pt,end_pt,dist_lim)
    line_segments=[]
    for i in range(len(line_split)-1):
        line_segments.append([
            line_split[i-1],
            line_split[i],
        ])
    return line_segments

def split_path_by_dist(path,dist_lim):
    '''
    Given a path, go through every segment of the path to make sure no line segment is longer than the given dist_lim

    Args:
        path: A list of 2d points
        dist_lim: the maximum length of any given line segment in the new path.

    Returns: a new path is the same geometry with the given path, but none of the line segment with the new path is longer than the given dist limitation.

    '''
    if len(path)<2:
        return [pt.copy() for pt in path]

    split_path=[]
    for i in range(1,len(path)):
        pre_pt=path[i-1]
        this_pt=path[i]
        split_line=split_line_by_dist(pre_pt,this_pt,dist_lim)
        if i!=len(path)-1 and len(split_line)>0:
            # remove the last point because next line would contain it.
            split_line.pop()
        split_path+=split_line

    return split_path

def cut_path_to_lines_by_dist(path,dist_lim):

    '''
    Given a path, go through every line segment of the path. If any segment is longer than the given dist limit, cut it into multiple lines so that each segment is shorter than the limit.

    Args:
        path: A list of 2d points
        dist_lim: the maximum length of any given line segment in the new path.

    Returns: a list of lines (2 pts) that are shorter than the dist_lim
    '''

    split_path=split_path_by_dist(path,dist_lim)
    line_segments=[]
    for i in range(1,len(split_path)):
        line_segments.append([
            split_path[i-1],
            split_path[i],
        ])
    return line_segments

def cut_path_to_paths_by_dist(path,dist_lim):

    '''
    Given a path, cut it into sections that are shorter than the dist_lim.
    The result can contain paths, whereas cut_path_to_lines_by_dist() can only return lines.

    Args:
        path: A list of 2d points
        dist_lim: the maximum length of any given line segment in the new path.

    Returns: a list of paths (2-n pts) that are shorter than the dist_lim
    '''
    if len(path)<2:
        return [[pt.copy() for pt in path]]
    path_segments=[]

    path_length=calc_path_length(path)
    if path_length<dist_lim:
        #the full length of the path is shorter than dist_lim.
        #Return a copy of the the uncut path.
        return [[pt.copy() for pt in path]]

    to_process=path.copy()
    to_process.reverse()
    current_pt=to_process.pop()
    next_pt=to_process.pop()
    current_seg=[current_pt]
    current_dist=0
    while len(to_process)>0:
        dist=math.dist(current_pt,next_pt)
        if current_dist+dist<=dist_lim:
            #can append the next point to the current seg
            current_seg.append(next_pt)
            current_dist+=dist
            current_pt=next_pt
            next_pt=to_process.pop()
        else:
            #need to produce a break point and start the next seg.
            break_pt=get_pt_on_line_by_dist(current_pt,next_pt,dist_lim-current_dist)
            current_seg.append(break_pt)
            path_segments.append(current_seg)
            current_seg=[break_pt]
            current_pt=break_pt
            current_dist=0

    if current_seg!=path_segments[-1]:
        path_segments.append(current_seg)
    if current_pt!=next_pt:
        path_segments+=cut_line_by_dist(current_pt,next_pt,dist_lim)


    return path_segments






