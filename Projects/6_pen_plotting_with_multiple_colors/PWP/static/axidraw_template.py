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

def run(ad,paths):
    for i, path in enumerate(paths):
        if len(path)<2:
            # Not a line. Skip.
            continue
        move_and_draw_path(ad, path[0], path[1:])
        if i%100==0:
            print(i)
    end(ad)

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return int(h),int(m),int(s)

def set_arg_parser(parser):
    '''
    Enable the command line options.
    Args:
        parser: The parser object.

    Returns: None

    '''
    parser.add_argument('-reg', '--register', action='store_true', help='Perform the registration action.')
    # run
    parser.add_argument('-re', '--resume', type=int,
                        help='Restart the run at a given index. Require an integer input for index')


def main():
    starttime = time.time()
    parser = argparse.ArgumentParser()
    set_arg_parser(parser)

    args = parser.parse_args()


    ad = initiate_axidraw()

    if args.resume:
        start_idx = args.resume
        print(f"Resume at index {start_idx}")
        run(ad,paths[:start_idx])
    elif args.register:
        print(f'Registering according to register_marks')
        run(ad,registration_marks)
    else:
        run(ad, paths)
    seconds = time.time() - starttime
    h, m, s = format_time(seconds)
    print(f'Total Running Time {int(h)}, {int(m)}, {int(s)}')



if __name__ == "__main__":
    main()

