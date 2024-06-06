'''
A template file used as the basis of an axidraw-operating script.

To construct a finished script, the following information is required (append before this instruction)

### BASICS####
    portName="kitty" #string name to the usb port
    pathList=[] # a list of paths (list of 2D coordinates) to be drawn
    options={} # a dictionary used to overwrite default pyaxidraw options
    anchorPoints=[] #a list of paths to be drawn if the --registration option is called.

#### FOR SPECIAL MODES ###
    util_func_check={
        "enable_pause":False,
        "enable_shake":False,
        "enable_adj": False,
        "enable_timer":False
    } # a dictionary that stores triggers for special modes


## INK MODE ##
    inkPoints=[] #a list of paths to be drawn if the --ink option is called.

## PAUSE MODE ##
    pause_second=0
    pauseIdxList=[]# a list of integers that represent the path indexes.
                    #If enable_pause is true, after reaching these indexes, pause for a



## ADJUSTMENT/TRANSLATION MODE ##
    adjusts={
        "x":0,
        "y":0,
    }# if enable_adj is true, add translation in this dictionary to every path.

## SHAKE MODE ##
    shake_idx=300 # a positive integer. If the shaking mode is enabled and the shake_idx count is reached,
                  #perform the shaking action
                  #(e.g., shake_idx=10, after every 10 paths, trigger the shaking)
    shake_times=10 # an integer that determines how many times the pen is shaken.

## TIMER MODE ##
    timer_setting=[{
        "session_start_idx":None, # until which session (inclusive) that this setting starts to work.
        "session_time":None, # how long (in second) each session
        "break_time":None # how long (in second) the machine will rest before the next session.
    },#{....} can have multiple settings
    ]

'''
from pyaxidraw import axidraw
import time,argparse,ast,re

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
shake_options={
    "pen_rate_lower": 100,
    "pen_rate_raise": 100,
    "pen_pos_up": 100,
}
before_shake_options={}


def initiate_axidraw(portName):
    ad = axidraw.AxiDraw()
    ad.interactive()

    ad.params.auto_clip_lift = False
    ad.params.clip_to_page = False
    default_options["port"]=portName
    default_options.update(options)

    for key in default_options:
        setattr(ad.options,key,default_options[key])

    ad.connect()
    ad.update()
    ad.penup()
    shake_options["pen_pos_down"]=default_options["pen_pos_up"]
    before_keys=["pen_pos_down","pen_pos_up","pen_rate_lower","pen_rate_raise"]
    for key in before_keys:
        before_shake_options[key]=default_options[key]

    return ad

def shake_pen(ad):
    for key in shake_options:
        setattr(ad.options,key,shake_options[key])
    ad.update()
    for i in range(shake_times):
        ad.pendown()
        ad.penup()
    for key in before_shake_options:
        setattr(ad.options,key,before_shake_options[key])
    ad.update()


    #resume
def moveAndLine(ad,moveToLoc,line):
    ad.penup()
    mx,my=moveToLoc
    if util_func_check["enable_adj"]:
        mx+=adjusts["x"]
        my+=adjusts["y"]

    ad.moveto(mx,my)
    for pt in line:
        px,py=pt
        if util_func_check["enable_adj"]:
            px+=adjusts["x"]
            py+=adjusts["y"]
        ad.lineto(px,py)

def disconnect(ad):
    ad.moveto(0,0)
    ad.disconnect()

def run(ad,startIdx=0,mode="normal"):

    current_session_idx=0
    current_session_start=time.time()
    timer_setting.reverse() #will use pop
    current_session_setting=None
    next_session_setting=None
    if len(timer_setting)>0:
        current_session_setting=timer_setting.pop()
    if len(timer_setting)>0:
        next_session_setting=timer_setting.pop()

    # current_session_lim=timer_setting["init_session"]
    # break_time=timer_setting["break_time"]

    lstToRun=pathList
    if mode=="register":
        lstToRun=anchorPoints
    elif mode=="custom":
        lstToRun=customPath
    elif mode=="ink":
        lstToRun=inkPoints
    for i, l in enumerate(lstToRun[startIdx:]):
        if util_func_check["enable_timer"] and current_session_setting:
            current_session_length=time.time()-current_session_start
            if current_session_length>=current_session_setting["session_time"]:
                #Session finished, break
                ad.penup()
                print(f'session {current_session_idx} done, took {format(current_session_length)}. Break for {format_time(current_session_setting["break_time"])}')
                time.sleep(current_session_setting["break_time"])
                current_session_start=time.time()
                current_session_idx+=1
                # determine whether to switch session settings.
                if next_session_setting:
                    next_starter=next_session_setting["session_start_idx"]
                    if current_session_idx>=next_starter:
                        current_session_setting=next_session_setting
                        if len(timer_setting) > 0:
                            next_session_setting = timer_setting.pop()

        if (i + startIdx) % 10 == 0:
            print(i + startIdx)
        if len(l) < 2:
            continue

        current_idx=startIdx+i
        if util_func_check["enable_shake"] and (current_idx%shake_idx==0):
            shake_pen(ad)
        moveAndLine(ad, l[0], l[1:])
        if util_func_check["enable_pause"] and (current_idx in pauseIdxList):
            ad.penup()
            time.sleep(pause_second)

    print(f'final session ct {current_session_idx}')
    disconnect(ad)

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return int(h),int(m),int(s)


def parse_2d_array(array_str):
    try:
        # Safely evaluate the string to a Python object
        array = ast.literal_eval(array_str)
        if isinstance(array, list) and all(isinstance(i, list) for i in array):
            return array
        else:
            raise ValueError
    except (ValueError, SyntaxError):
        raise argparse.ArgumentTypeError('Input must be a 2D array like [[1,2],[3,4]].')


def parse_list_of_dicts(dicts_str):
    # Preprocess the string to ensure keys are quoted
    dicts_str = re.sub(r'([{,])(\s*)([a-zA-Z_]\w*)(\s*):', r'\1"\3":', dicts_str)
    try:
        # Safely evaluate the string to a Python object
        dicts = ast.literal_eval(dicts_str)
        if isinstance(dicts, list) and all(isinstance(d, dict) for d in dicts):
            return dicts
        else:
            raise ValueError
    except (ValueError, SyntaxError):
        raise argparse.ArgumentTypeError('Input must be a list of dictionaries like [{"a":3,"b":5},{"c":3}].')


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def set_arg_parser(parser):
    #####standalone
    parser.add_argument('-reg', '--register', action='store_true', help='Perform the registration action.')

    parser.add_argument('-cp', '--custom_path', type=parse_2d_array, required=False,
                        help='Going to custom path specified by the customPath argument')

    parser.add_argument('-ik', '--ink_location', action='store_true',
                        help='Drawing paths defined by the "inkPoints" parameter')
    parser.add_argument('-sk', '--shake', action='store_true',
                        help='Enable shaking. Using shake_idx and shake_times to control the shaking.')

    ####add on
    parser.add_argument('-p', '--pause', type=float,
                        help='Enable pausing for the given seconds. Requires pauseIdxList. Will pause after every index specified by the pauseIdxList')

    parser.add_argument('-al', '--adjust_location', type=float, nargs=2,
                        help='Adjust location for the entire run.  Requires an input of two locations (adjx and adjy, in inches), will adjust the adjx and adjy parameter, will also trigger the adjust_location to be true.')

    parser.add_argument('-delay', '--init_delay', type=float,
                        help='Adjust location for the entire run.  Requires an input of a delay duration (in second). The Run action will start after the delay. ')

    parser.add_argument('-es', '--enable_session', type=str2bool,
                        help='Enable timed session. The variable timer_setting needs to be available. Set timer_setting using --set_sessions')

    parser.add_argument('-ss', '--set_session', type=parse_list_of_dicts,
                        help='Set the timer settings. Example setting: {"session_start_idx":0,"session_time":10,"break_time":50}')

    # run
    parser.add_argument('-re', '--resume', type=int,
                        help='Restart the run at a given index. Require an integer input for index')


def main():
    starttime = time.time()
    parser = argparse.ArgumentParser(description=f'Running {portName}')
    set_arg_parser(parser)

    args = parser.parse_args()

    if args.adjust_location:
        adjusts["x"] = args.adjust_location[0]
        adjusts["y"] = args.adjust_location[1]
        util_func_check["enable_adj"] = True
        print(f'Adjust Location by adding {adjusts} (inch) to every path.')

    if args.init_delay:
        delay_sec = args.init_delay
        print(f'Delay {delay_sec} seconds.')
        time.sleep(delay_sec)

    if args.pause:
        global pause_second
        pause_second = args.pause
        util_func_check["enable_pause"] = True
        print(f'After every index specified in the pauseIdxList, enable pause of {pause_second} second')

    if args.shake:
        util_func_check["enable_shake"] = True
        print(f'Enable shake')

    if args.enable_session is True or args.enable_session is False:
        print(f'Enable timed sessions to be {args.enable_session}')
        util_func_check["enable_timer"] = args.enable_session

    if args.set_session:
        global timer_setting
        print(f'Replace existing timer setting {timer_setting} to be {args.set_session}')
        timer_setting = args.set_session

    ad = initiate_axidraw(portName=portName)
    ad.penup()
    ad.update()

    if args.resume:
        restart_line = args.resume
        print(f"Resume at index {restart_line}")
        run(ad,startIdx=restart_line)
    elif args.register:
        print(f'Registering according to anchorPoints')
        run(ad,mode="register")
    elif args.custom_path:
        customPath = args.custom_path
        print(f'Will draw the following paths: {customPath}')
        run(ad, mode="custom")
    elif args.ink_location:
        print(f'Will draw the following ink paths stored in inkPoints')
        run(ad,mode="ink")
    else:
        print("Run")
        run(ad,startIdx=0)

    seconds = time.time() - starttime
    h, m, s = format_time(seconds)
    print(f'Total Running Time {int(h)}, {int(m)}, {int(s)}')



if __name__ == "__main__":
    main()

