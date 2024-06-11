import pyclipper,math

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