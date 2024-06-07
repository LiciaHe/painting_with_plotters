from pyaxidraw import axidraw
default_options = {
    "port_config": 2,
    "model": 2,
    "pen_rate_lower": 100,
    "pen_rate_raise": 90,
    "pen_delay_down": 0,
    "pen_delay_up": 0,
    "accel": 90,
    "unit": 0,
    "pen_pos_up": 80,
    "pen_pos_down": 45,
    "speed_pendown":25,
    "speed_penup":25,
}

def initiate_axidraw(portName):
    '''
    Initiate an axidraw instance.
    Args:
        portName: If connecting to a specific port, provide the port name (String)

    Returns: An instance of the Axidraw class
    '''

    ad = axidraw.AxiDraw()
    ad.interactive()

    if portName:
        default_options["port"]=portName

    for key in default_options:
        setattr(ad.options,key,default_options[key])

    ad.connect()
    ad.update()

    ad.penup()
    return ad

def move_and_draw_path(ad,move_to_pt,path):
    '''
    Move to a given point,draw a given line.
    Args:
        ad: axidraw instance
        move_to_pt: a 2d point.
        path: a list of 2D points.

    Returns: None
    '''
    ad.penup()
    mx,my=move_to_pt
    ad.moveto(mx, my)
    ad.pendown()
    for pt in path:
        px,py=pt
        ad.moveto(px,py)
    ad.penup()

def end(ad):
    '''
    Return the given axidraw to home (0,0) and disconnect it.
    Args:
        ad: an axidraw instance.

    Returns:None
    '''
    ad.moveto(0,0)
    ad.disconnect()

def run(ad,paths):
    for i, path in enumerate(paths):
        if len(path)<2:
            # Not a line. Skip.
            continue
        move_and_draw_path(ad, path[0], path[1:])
    end(ad)


portName="kitty" # use None if there's only one plotter, or the plotter is not named.
paths=[]#list of paths
ad = initiate_axidraw(portName=portName)
run(ad, paths)





