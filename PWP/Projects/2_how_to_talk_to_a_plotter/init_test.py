from pyaxidraw import axidraw

ad = axidraw.AxiDraw()
ad.interactive()
portName="ducky"
default_options = {
    "port_config": 2,
    "port": portName,#name of the USB port. Omit if there's only one plotter.
    "model": 2,# 1 for SE/A4, 2 for SE/A3, 5 for SE/A1
    #"penlift": 3,# If the plotter has the brushless servo upgrade, use 3. Otherwise, omit this or use default value 1.
    "pen_pos_up": 80,# Pen height when the pen is up (Z axis). 0-100.
    "pen_pos_down": 0, #Pen height when the pen is down (Z axis). 0-100.
    "pen_rate_lower": 10,# Rate for z-axis movement (0-100)
    "pen_rate_raise": 10,# Rate for z-axis movement (0-100)
    "accel": 90,#accelerate rate(1-100)
    "unit": 0,#0 for inch, 1 for cm, 2 for mm. Default 0
    "speed_pendown": 80, #Maximum XY speed when the pen is down (0-100)
    "speed_penup": 80 #Maximum XY speed when the pen is up (0-100)
}

for key in default_options:
    setattr(ad.options, key, default_options[key])

ad.connect()
ad.update()
ad.penup()
ad.pendown()
ad.penup()
ad.moveto(1,1)
ad.disconnect()