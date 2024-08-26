import pyclipper,math
from ..Util import geometry as UG

OFFSETTYPES={
    "CLOSEDPOLYGON":pyclipper.ET_CLOSEDPOLYGON,
    "CLOSEDLINE":pyclipper.ET_CLOSEDLINE,
    "OPENROUND":pyclipper.ET_OPENROUND,
    "OPENSQUARE":pyclipper.ET_OPENSQUARE,
    "OPENBUTT":pyclipper.ET_OPENBUTT
}
JOINTTYPES={
    "MITER":pyclipper.JT_MITER,
    "ROUND":pyclipper.JT_ROUND,
    "SQUARE":pyclipper.JT_SQUARE
}
CLIPPER_TYPE={"intersection":pyclipper.CT_INTERSECTION,"union":pyclipper.CT_UNION,"difference":pyclipper.CT_DIFFERENCE,"xor":pyclipper.CT_XOR}

FILL_TYPE={"evenodd":pyclipper.PFT_EVENODD,"positive":pyclipper.PFT_POSITIVE,"negative":pyclipper.PFT_NEGATIVE,"nonzero":pyclipper.PFT_NONZERO}


def make_clipper(subj_path,clip_path,clipper_type_string,subj_fill="positive",clip_fill="positive",subj_closed=True,subj_multi=False,clip_multi=False,close_result=True):
    '''
        Produce a clipper operation between subj and clip
    Args:
        subj_path: a path to be clipped.
        clip_path: a path to use as the clipper.
        clipper_type_string: one of the following values: intersection, union, difference, xor.
        subj_fill: one of the following values: evenodd, positive, negative, nonzero.
        clip_fill: one of the following values: evenodd, positive, negative, nonzero.
        subj_closed: whether the subj_path is a closed path.
        subj_multi: whether the subj_path is a nested path.
        clip_multi:  whether the clip_path is a nested path.
        close_result: make the result paths as closed polygons.

    Returns:

    '''

    pc = pyclipper.Pyclipper()
    scaled_subj = pyclipper.scale_to_clipper(subj_path)
    scaled_clip = pyclipper.scale_to_clipper(clip_path)
    # print("clip",scaledClip)
    clipper_type = CLIPPER_TYPE[clipper_type_string]

    if subj_multi:
        pc.AddPaths(scaled_subj, pyclipper.PT_SUBJECT, subj_closed)
    else:
        pc.AddPath(scaled_subj, pyclipper.PT_SUBJECT, subj_closed)
    if clip_multi:
        pc.AddPaths(scaled_clip, pyclipper.PT_CLIP, True)
    else:
        pc.AddPath(scaled_clip, pyclipper.PT_CLIP, True)

    fill1=FILL_TYPE[subj_fill]
    fill2=FILL_TYPE[clip_fill]
    result_paths = []
    solution = pc.Execute2(clipper_type, fill1, fill2)
    paths = pyclipper.PolyTreeToPaths(solution)

    for p in paths:
        scaled_back_path=pyclipper.scale_from_clipper(p)
        if close_result and len(scaled_back_path)>0:
            scaled_back_path.append(scaled_back_path[0].copy())
        result_paths.append(scaled_back_path)
    return result_paths


def fill_with_line(path,gap,rot_radians=0,fill_type="positive"):
    '''
    Given a path, produce hatch lines that fill the space.
    Args:
        path: A list of 2d points.
        gap: distance between the hatch line
        rot_radians: angle of the line. By default, horizontal (0)
        fill_type: the fill type of the subject (path)


    Returns:

    '''
    #generate original bbox and large bbox
    bbox = UG.get_wh_bbox(path)
    max_wh = max(bbox[2:]) * 2 ** 0.5
    lg_bbox = UG.get_wh_bbox_from_center(
        center=UG.get_center_from_wh_bbox(bbox),
        width=max_wh,
        height=max_wh,
    )
    x,y,w,h=lg_bbox
    box_center=UG.get_center_from_wh_bbox(lg_bbox)

    #generate rotated lines
    lines = []
    line = [[x,y],[x+w,y]]
    lines.append(
        UG.rotate_path(line, origin=box_center, angle_radian=rot_radians)
    )

    rep_ct = math.ceil(lg_bbox[3] / gap)
    for i in range(rep_ct):
        line = UG.translate_path(line, 0, gap)
        lines.append(UG.rotate_path(line, origin=box_center, angle_radian=rot_radians))

    #cut lines into the shape.
    result_fills=[]
    for line in lines:
        result_fills+=make_clipper(
            subj_path=line,
            clip_path=path,
            clipper_type_string="intersection",
            close_result=False,
            subj_closed=False,
            clip_fill=fill_type
        )
    return result_fills


def make_offset(subj_path,offset_width,offset_type="OPENSQUARE",joint_type="SQUARE",close_result=True):
    '''
    Given a path, offset it.
    See     http://www.angusj.com/delphi/clipper/documentation/Docs/Units/ClipperLib/Types/EndType.htm
    http://www.angusj.com/delphi/clipper/documentation/Docs/Units/ClipperLib/Types/JoinType.htm

    Args:
        subj_path: a list of 2d points
        offset_width: how much to offset.
        offsetType: one of the following values: CLOSEDPOLYGON, CLOSEDLINE, OPENROUND,OPENSQUARE, OPENBUTT
        jointType: one of MITER, ROUND, SQUARE
        close_result: whether to close the result. Default True.

    Returns: The result of the offset. A list of paths.
    '''

    offset_width=int(offset_width)
    offsetType=OFFSETTYPES[offset_type.upper()]
    jointType=JOINTTYPES[joint_type.upper()]
    pco = pyclipper.PyclipperOffset()
    sub_s=pyclipper.scale_to_clipper(subj_path)
    pco.AddPath(sub_s,jointType, offsetType)
    solution = pco.Execute(pyclipper.scale_to_clipper(offset_width))
    scaled_solution=pyclipper.scale_from_clipper(solution)
    for ss in scaled_solution:
        if close_result and len(ss)>0:
            ss.append(ss[0].copy())
    return scaled_solution