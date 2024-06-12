from pyaxidraw import axidraw
import time,argparse,ast,re
def initiate_axidraw():
    '''
    Initiate an axidraw instance.
    Args:
        portName: If connecting to a specific port, provide the port name (String)

    Returns: An instance of the Axidraw class
    '''

    ad = axidraw.AxiDraw()
    ad.interactive()

    for key in options:
        setattr(ad.options,key,options[key])

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

def run(ad,paths,start_idx=0):
    path_ct=len(paths)
    for i, path in enumerate(paths[start_idx:]):
        if len(path)<2:
            # Not a line. Skip.
            continue
        current_idx=start_idx+i
        if i%10==0:
            print(f'{current_idx}/{path_ct}')
        move_and_draw_path(ad, path[0], path[1:])
    end(ad)

starttime = time.time()
parser = argparse.ArgumentParser()
parser.add_argument('-reg', '--register', action='store_true', help='Perform the registration action.')
parser.add_argument('-sk', '--shake', action='store_true',
                    help='Enable shaking. Using shake_idx and shake_times to control the shaking.')
parser.add_argument('-re', '--resume', type=int,
                    help='Restart the run at a given index. Require an integer input for index')
args = parser.parse_args()
ad = initiate_axidraw()
if args.register:
    run(ad, anchor_paths)
elif args.resume:
    print(f"Resume at index {args.resume}")
    run(ad,paths,start_idx=args.resume)
else:
    run(ad,paths)






