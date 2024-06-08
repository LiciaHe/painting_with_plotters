from pyaxidraw import axidraw

default_options = {
    "port_config": 2,
    "model": 2,# 1 for SE/A4, 2 for SE/A3, 5 for SE/A1
    #"penlift": 3,# If the plotter has the brushless servo upgrade, use 3. Otherwise, omit this or use default value 1.
    "pen_pos_up": 80,# Pen height when the pen is up (Z axis). 0-100.
    "pen_pos_down": 0, #Pen height when the pen is down (Z axis). 0-100.
    "pen_rate_lower": 75,# Rate for z-axis movement (0-100)
    "pen_rate_raise": 75,# Rate for z-axis movement (0-100)
    "accel": 90,#accelerate rate(1-100)
    "unit": 0,#0 for inch, 1 for cm, 2 for mm. Default 0
    "speed_pendown": 80, #Maximum XY speed when the pen is down (0-100)
    "speed_penup": 80 #Maximum XY speed when the pen is up (0-100)
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

    mx,my=move_to_pt
    # ad.moveto(mx,my) is the equivalent of the following 2 lines.
    ad.penup()
    ad.goto(mx, my)

    ad.pendown()
    for pt in path:
        px,py=pt
        #can use ad.lineto() to replace pendown() and goto()
        ad.goto(px,py)

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
paths=[[[1,1],[5,1],[5,5],[1,5],[1,1]],[[1,1],[5,5]]]#list of paths. Specified in inch.
ad = initiate_axidraw(portName=portName)
run(ad, paths)





