import tkinter as tk
from tkinter import ttk
import serial
import sys
from threading import Timer
import time

try:
    ser = serial.Serial("/dev/ttyACM1",115200,timeout=2)
except:
    print("Couldn't open the serial port")
    sys.exit(0)

window = tk.Tk()

x = tk.StringVar(window) # initial turn
f = tk.StringVar(window) # distance
y = tk.StringVar(window) # final turn


# to rename the title of the window
window.title("Teleop")
window.minsize(800,500)
# pack is used to show the object in the window

# You will create two text labels namely 'username' and 'password' and and two input labels for them
tk.Label(window, text = "Controls", font=("", 24)).grid(row = 0, column = 0, sticky = '', pady = 10) #'username' is placed on position 00 (row - 0 and column - 0)
tk.Label(window, text = "Parameters", font=("", 24)).grid(row = 0, column = 2, sticky = '', pady = 10)

window.columnconfigure(0,weight=1)
window.columnconfigure(2,weight=4)
window.rowconfigure(0, weight = 0)
window.rowconfigure(2, weight = 1)
window.rowconfigure(3, weight = 4)

controls_frame = tk.Frame(window,name="controls_frame")
controls_frame.grid(row = 1, column = 0, sticky = 'NSEW')
params_frame = tk.Frame(window,name="params_frame")
params_frame.grid(row = 1, column = 2, sticky = 'NSEW')
wp_frame = tk.Frame(window,name="wp_frame")
wp_frame.grid(row = 3, column = 2, sticky = 'NSEW')

ttk.Separator(window, orient='vertical').grid(column=1, row=0, rowspan=2, sticky='NS')
ttk.Separator(window, orient='horizontal').grid(column=0, row=2, columnspan=4, sticky='NSEW')

# 'Entry' class is used to display the input-field for 'username' text label
btn_w = tk.Button(controls_frame, text = "W", width = 1, height = 2, name = 'btn_w')
btn_w.grid(row = 0, column = 1, sticky = 'S')

btn_a = tk.Button(controls_frame, text = "A", width = 1, height = 2, name = 'btn_a')
btn_a.grid(row = 1, column = 0, sticky = 'E')

btn_s = tk.Button(controls_frame, text = "S", width = 1, height = 2, name = 'btn_s')
btn_s.grid(row = 2, column = 1, sticky = 'N')

btn_d = tk.Button(controls_frame, text = "D", width = 1, height = 2, name = 'btn_d')
btn_d.grid(row = 1, column = 2, sticky = 'W')

movement_buttons = {'w': btn_w, 'a': btn_a, 's': btn_s, 'd': btn_d}

param_types = ["f","l","s","h","u","d","p"]

params = {
    "Walk": {
        "f": 0.8,
        "l": 0.15,
        "s": 0.06,
        "h": 0.18,
        "u": 0.03,
        "d": 0.03,
        "p": 0.5
    },
    "Trot": {
        "f": 0.8,
        "l": 0.15,
        "s": 0.06,
        "h": 0.18,
        "u": 0.03,
        "d": 0.03,
        "p": 0.5
    },
    "Pronk": {
        "f": 2,
        "l": 2,
        "s": 2,
        "h": 2,
        "u": 2,
        "d": 2,
        "p": 0.5
    },
    "Bound": {
        "f": 2,
        "l": 2,
        "s": 2,
        "h": 2,
        "u": 2,
        "d": 2,
        "p": 0.5
    }
}

controls_frame.columnconfigure(0,weight=1)
controls_frame.columnconfigure(1,weight=0)
controls_frame.columnconfigure(2,weight=1)
controls_frame.rowconfigure(0,weight=1)
controls_frame.rowconfigure(1,weight=0)
controls_frame.rowconfigure(2,weight=1)

GaitMode = tk.StringVar(window)
GaitMode.set("Walk")

tk.Label(params_frame, text="Gait").grid(row=0,column=0)
tk.OptionMenu(params_frame,GaitMode,"Walk","Trot","Pronk","Bound","Waypoint").grid(row=0,column=1,sticky='EW',padx=10,pady=(10,0))

tk.Label(params_frame, text="Frequency").grid(row=1,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=10,resolution=0.1,	
tickinterval=1, name="f").grid(row=1,column=1,sticky='EW',padx=10)

tk.Label(params_frame, text="Stride Length").grid(row=2,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.15,resolution=0.01,	
tickinterval=0.05, name="l").grid(row=2,column=1,sticky='EW',padx=10)

tk.Label(params_frame, text="Step Difference").grid(row=3,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.3,resolution=0.01,	
tickinterval=0.02, name="s").grid(row=3,column=1,sticky='EW',padx=10)

tk.Label(params_frame, text="Stance Height").grid(row=4,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.2,resolution=0.01,	
tickinterval=0.04, name="h").grid(row=4,column=1,sticky='EW',padx=10)

tk.Label(params_frame, text="Up Amplitude").grid(row=5,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.1,resolution=0.01,	
tickinterval=0.02, name="u").grid(row=5,column=1,sticky='EW',padx=10)

tk.Label(params_frame, text="Down Amplitude").grid(row=6,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.1,resolution=0.01,	
tickinterval=0.02, name="d").grid(row=6,column=1,sticky='EW',padx=10)

tk.Label(params_frame, text="Flight %").grid(row=7,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=1,resolution=0.05,	
tickinterval=0.2, name="p").grid(row=7,column=1,sticky='EW',padx=10)

params_frame.columnconfigure(0,weight=1)
params_frame.columnconfigure(1,weight=3)

# waypoint frame
tk.Label(wp_frame, text="Initial turn in degrees").grid(row=1, column = 2, sticky = '', padx = 20)
read_x = tk.Entry(wp_frame, textvariable = x).grid(row=7, column = 2, sticky = '', padx = 20)

tk.Label(wp_frame, text="distance to move in meters").grid(row=1, column = 3, sticky = '', padx = 20)
read_d = tk.Entry(wp_frame, textvariable = f).grid(row=7, column = 3, sticky = '', padx = 20)

tk.Label(wp_frame, text="final turn in degrees").grid(row=1, column = 4, sticky = '', padx = 20)
read_y = tk.Entry(wp_frame, textvariable = y).grid(row=7, column = 4, sticky = '', padx = 20)

btn_sendwp = tk.Button(wp_frame, text = "Send Waypoint", width = 14, height = 2, name = 'btn_sendwp')
btn_sendwp.grid(row = 7, column = 5, sticky = 'W')

tk.Label(wp_frame, text="default values are all zero").grid(row=8,column=3)

def send_all_params():
    if GaitMode.get() == "Waypoint":
        return
    for (key,value) in params[GaitMode.get()].items():
        window.nametowidget("params_frame."+key).set(value)
        ser.write(str(key + ' ' + GaitMode.get()[0] + ' ' + str(value) + '\n').encode('utf-8'))
        if GaitMode.get() == "Trot":
            ser.write(str(key + ' Y ' + str(value) + '\n').encode('utf-8'))

send_all_params()

# 'Checkbutton' class is for creating a checkbutton which will take a 'columnspan' of width two (covers two columns)
# tk.Checkbutton(window, text = "Keep Me Logged In").grid(columnspan = 2) 
def get_waypoint():
    _x = x.get()
    _f = f.get()
    _y = y.get()

    return _x, _f, _y

def button1_event(event=None,key=None,type_=None):
    if key:
        widget_name = "btn_" + key
        event_type =  "ButtonPress" if type_ == "KeyPress" else "ButtonRelease"
    else:
        widget_name = str(event.widget).split(".")[-1]
        event_type = str(event.type)

    if event_type == "ButtonPress":
        if widget_name == "btn_sendwp" and GaitMode.get() == "Waypoint":
            print("SEND ", GaitMode.get(), "Forward")
            initial_turn, distance, final_turn = get_waypoint()
            print(initial_turn, distance, final_turn)
            ser.write(str('x' + ' ' + 'L' + ' 0 ' + initial_turn + ' ' + distance + ' ' + final_turn +'\n').encode('utf-8'))
            ser.write(str('L'+'\n').encode('utf-8'))
        elif widget_name == "btn_w":
            print("SEND ", GaitMode.get(), "Forward")
            ser.write(str(GaitMode.get()[0]+'\n').encode('utf-8'))
        elif widget_name == "btn_a":
            print(str('s Y -' + str(params["Trot"]["s"]) + '\n').encode('utf-8'))
            ser.write(str('s Y -' + str(params["Trot"]["s"]) + '\n').encode('utf-8'))
            ser.write(b'Y\n')
            print("SEND Trot Left")
            # ser.write(b'\r')
        elif widget_name == "btn_s":
            print("SEND ", GaitMode.get(), "Backward")
        elif widget_name == "btn_d":
            print(str('s Y ' + str(params["Trot"]["s"]) + '\n').encode('utf-8'))
            ser.write(str('s Y ' + str(params["Trot"]["s"]) + '\n').encode('utf-8'))
            ser.write(b'Y\n')
            print("SEND Trot Right")
    elif event_type == "ButtonRelease" and (widget_name == "btn_w" or widget_name == "btn_a" or widget_name == "btn_s" or widget_name == "btn_d"):
        print("SEND Stop")
        ser.write(b'S\n')
    
    if event_type == "ButtonRelease":
        if widget_name in param_types:
            print("Setting ", widget_name, " to ", event.widget.get())
            params[GaitMode.get()][widget_name] = event.widget.get()
            ser.write(str(widget_name + ' ' + GaitMode.get()[0] + ' ' + str(event.widget.get()) + '\n').encode('utf-8'))
            if GaitMode.get() == "Trot":
                ser.write(str(widget_name + ' Y ' + str(event.widget.get()) + '\n').encode('utf-8'))
        elif widget_name == "!optionmenu":
            if GaitMode.get() == "Waypoint":
                print("Setting ", widget_name, " to ", GaitMode.get())
                print("parameters for waypoint are not changeable")
            else:
                print("Setting ", widget_name, " to ", GaitMode.get())
                print(params[GaitMode.get()])

        send_all_params()

was_pressed = {'w': False, 'a': False, 's': False, 'd': False}
            
def key_event(event):
    if event.char in was_pressed:
        if str(event.type) == "KeyPress" and not was_pressed[event.char]:
            was_pressed[event.char] = True
            movement_buttons[event.char].configure(state='active')
            button1_event(key=event.char,type_=str(event.type))
            # print(event.char, " ", event.type)
        elif str(event.type) == "KeyRelease":
            was_pressed[event.char] = False
            movement_buttons[event.char].configure(state='normal')
            button1_event(key=event.char,type_=str(event.type))
            # print(event.char, " ", event.type)

        

# btn_w.bind("<Button-1>",        event_w)
# btn_w.bind("<ButtonRelease-1>", event_w)

# btn_a.bind("<Button-1>",        event_a)
# btn_a.rbind("<ButtonRelease-1>", event_a)

# btn_s.bind("<Button-1>",        event_s)
# btn_s.bind("<ButtonRelease-1>", event_s)

# btn_d.bind("<Button-1>",        event_d)
# btn_d.bind("<ButtonRelease-1>", event_d)

def button_event(event):
    print(event)

# window.bind("<KeyPress>", button_event)
window.bind("<Button-1>", button1_event)
window.bind("<ButtonRelease-1>", button1_event)

window.bind("<KeyPress>", key_event)
window.bind("<KeyRelease>", key_event)

def on_exit():
    ser.close()
    print("Closing serial port")
    window.destroy()

window.protocol("WM_DELETE_WINDOW",on_exit)
# window.mainloop()

t = Timer(2, send_all_params)
inString = ""

while 1:
    try:
        window.update()
    except:
        sys.exit(0)
    # if (ser.in_waiting):
    #     c = ser.read()
    #     if (c == '\n'):
    #         if inString == "!!!":
    #             t.start()
    #         inString = ""
    #     else:
    #         inString = inString + c

