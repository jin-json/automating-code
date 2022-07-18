import os
import sys
import json
import struct
import serial
import pyodbc
import binascii
import tkinter as tk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, Label, filedialog
from tkinter.scrolledtext import ScrolledText
OUTPUT_PATH=Path(__file__).parent
ASSETS_PATH=OUTPUT_PATH/Path('./assets')
def relative_to_assets(path:str)->Path:return ASSETS_PATH/Path(path)

#code from https://stackoverflow.com/questions/68198575/how-can-i-displaymy-console-output-in-tkinter
class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass

#https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller/42615559#42615559
def resource_path(config_name):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        running_mode = 'Frozen/executable'
    else:
        try:
            app_full_path = os.path.realpath(__file__)
            application_path = os.path.dirname(app_full_path)
            running_mode = "Non-interactive (e.g. 'python myapp.py')"
        except NameError as e:
            application_path = os.getcwd()
            running_mode = 'Interactive'
            print(e)
    return(os.path.join(application_path, config_name))

#Setup root window
window=Tk()
window.geometry('650x550')
window.configure(bg='#FFFFFF')

#Load the data and read it into global string var for future use.
file = open(resource_path("info.json"), "r")
file_text = file.read()
file.close()
data = json.loads(file_text)

serial_num = tk.StringVar()
port = tk.StringVar(value=data.get('port'))
filepath = tk.StringVar(value=data.get('filepath'))
horvolt = tk.StringVar(value=data.get('horvolt'))
horvolt2 = tk.StringVar(value=data.get('horvolt2'))
vertvolt = tk.StringVar(value=data.get('vertvolt'))
vertvolt2 = tk.StringVar(value=data.get('vertvolt2'))
samploptpow = tk.StringVar(value=data.get('samploptpow'))
diffvolt = tk.StringVar(value=data.get('currdetdiffvolt'))

debounce = tk.BooleanVar(value=True)

canvas=Canvas(window,bg='#FFFFFF',height=550,width=650,bd=0,highlightthickness=0,relief='ridge')
canvas.place(x=0,y=0)

frame = Frame(window)
frame.place(x=55,y=370.0)
#frame.pack()

log_widget = ScrolledText(frame, height=8, width=90, font=("consolas", "8", "normal"))
log_widget.pack()
#log_widget.grid(column = 0, pady = 200, padx = 10)
#text_area.grid(column = 0, pady = 10, padx = 10)

logger = PrintLogger(log_widget)
sys.stdout = logger
sys.stderr = logger

entry_image_1=PhotoImage(file=resource_path('entry_1.png'))
entry_bg_1=canvas.create_image(218.5,132.0,image=entry_image_1)
entry_8=Entry(bd=0,bg='#F7F7F7',highlightthickness=0)
entry_8.place(x=139.0,y=112.0,width=159.0,height=38.0)
entry_8.config(textvariable=serial_num)

entry_image_2=PhotoImage(file=resource_path('entry_2.png'))
entry_bg_2=canvas.create_image(428.5,132.0,image=entry_image_2)
entry_9=Entry(bd=0,bg='#F7F7F7',highlightthickness=0)
entry_9.place(x=349.0,y=112.0,width=159.0,height=38.0)
entry_9.config(textvariable=port)

canvas.create_text(178.0,79.0,anchor='nw',text='Serial #',fill='#191919',font=('Inter SemiBold',18*-1))
canvas.create_text(448.0,231.0,anchor='nw',text='Sample Optical Pow',fill='#191919',font=('Inter SemiBold',15*-1))
canvas.create_text(56.0,312.0,anchor='nw',text='Horizontal Voltage 2',fill='#191919',font=('Inter SemiBold',15*-1))
canvas.create_text(61.0,231.0,anchor='nw',text='Horizontal Voltage',fill='#191919',font=('Inter SemiBold',15*-1))
canvas.create_text(467.0,312.0,anchor='nw',text='CurrDetDiffVolt',fill='#191919',font=('Inter SemiBold',15*-1))
canvas.create_text(263.0,312.0,anchor='nw',text='Vertical Voltage 2',fill='#191919',font=('Inter SemiBold',15*-1))
canvas.create_text(270.0,231.0,anchor='nw',text='Vertical Voltage',fill='#191919',font=('Inter SemiBold',15*-1))
canvas.create_text(411.0,79.0,anchor='nw',text='Port',fill='#191919',font=('Inter SemiBold',18*-1))
canvas.create_text(55.0,344.0,anchor='nw',text='Output Log',fill='#191919',font=('Inter SemiBold',18*-1))

#original labels
# image_image_1=PhotoImage(file=resource_path('image_1.png'))
# image_1=canvas.create_image(326.0,452.0,image=image_image_1)

image_image_2=PhotoImage(file=resource_path('image_2.png'))
image_2=canvas.create_image(130.0,203.0,image=image_image_2)
image_image_3=PhotoImage(file=resource_path('image_3.png'))
image_3=canvas.create_image(325.0,203.0,image=image_image_3)
image_image_4=PhotoImage(file=resource_path('image_4.png'))
image_4=canvas.create_image(521.0,203.0,image=image_image_4)
image_image_5=PhotoImage(file=resource_path('image_5.png'))
image_5=canvas.create_image(130.0,285.0,image=image_image_5)
image_image_6=PhotoImage(file=resource_path('image_6.png'))
image_6=canvas.create_image(325.0,285.0,image=image_image_6)
image_image_7=PhotoImage(file=resource_path('image_7.png'))
image_7=canvas.create_image(130.0,285.0,image=image_image_7)
image_image_8=PhotoImage(file=resource_path('image_8.png'))
image_8=canvas.create_image(325.0,285.0,image=image_image_8)
image_image_9=PhotoImage(file=resource_path('image_9.png'))
image_9=canvas.create_image(520.0,285.0,image=image_image_9)
button_image_1=PhotoImage(file=resource_path('button_1.png'))

hor_lab = Label(bg = 'white', width = 20, text = "", font=10)
hor_lab.place(x=57,y=185,width=145,height=36.0)
hor2_lab = Label(bg = 'white', width = 20, text = "", font=10)
hor2_lab.place(x=57,y=265,width=145,height=36.0)
vert_lab = Label(bg = 'white', width = 20, text = "", font=10)
vert_lab.place(x=253,y=185,width=145,height=36.0)
vert2_lab = Label(bg = 'white', width = 20, text = "", font=10)
vert2_lab.place(x=253,y=265,width=145,height=36.0)
opt_lab = Label(bg = 'white', width = 20, text = "", font=10)
opt_lab.place(x=449,y=185,width=145,height=36.0)
volt_lab = Label(bg = 'white', width = 20, text = "", font=10)
volt_lab.place(x=449,y=265,width=145,height=36.0)

def starting():
    if debounce.get() == False:
        print("Currently handling process.")
        return
    debounce.set(False)

    sample_num = serial_num.get() 
    try:
        sample_num = int(sample_num)
    except ValueError:
        # Handle the exception
        print('Please enter an integer for the serial number.')
        debounce.set(True)
        return
    entries = [] #these are the entries that you will send to microsoft access
    entries.append(sample_num)

    port_c = port.get()
    try:
        ser = serial.Serial()
        ser.port = port_c
    except SerialException as e:
        print(e)
        debounce.set(True)
        return
    ser.open()

    #make connection string modifiable
    conn_string = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + filepath.get()
        )
    #print(conn_string)

    addresses = [horvolt2, vertvolt2, horvolt, vertvolt, samploptpow, diffvolt]
    labels = [hor2_lab, vert2_lab, hor_lab, vert_lab, opt_lab, volt_lab]
    for i in range(len(addresses)): 
        val = addresses[i].get()
        if val == "":
            entries.append(None)
            print("Empty output.")
            continue

        ser.write(val.encode("utf-8"))
        ser.write(13)
        ser.write(10)

        try:
            data = ser.readline()
        except serial.SerialException as e:
        #There is no new data from serial port
            print(e)
            debounce.set(True)
            return None
        data = data.decode(encoding='utf-8', errors='strict')
        # error checking to ensure the output can be transcribed to float. the 
        # output usually returned from reading is "281cf;    0    x   4685C000",
        # but we only want #485C00. 
        if len(data) < 8: 
            entries.append(None)
            print("Error in output.") 
            continue
        hex_num = data[-10:]
        # we remove the last two characters because they are instructions like '\n' 
        # which are not part of the actual hexcode output.
        data = hex_num[:-2]
        # performs conversion from hexadecimal to float (single precision 32-bit)
        float_conv = struct.unpack('!f', binascii.unhexlify(data))[0]
        float_conv = abs(round(float_conv))
        entries.append(float_conv)

        labels[i].config(text = str(float_conv))

    sql_command = ''' INSERT INTO SamplerData (samplenum, horizontal2voltage, vertical2voltage, horizontalvoltage, verticalvoltage, samploptpow, currdetdiffvoltage) 
          VALUES(?,?,?,?,?,?,?) '''
        
    try:
        conn = pyodbc.connect(conn_string) 
        cursor = conn.cursor()
        cursor.execute(sql_command, tuple(entries)) 
        conn.commit()
    except Exception as e: 
        print(e)
        debounce.set(True)
        return
    print("Successfully updated database!")
    debounce.set(True)

button_1=Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=starting,relief='flat')
button_1.place(x=126.0,y=18.0,width=395.0,height=51.0)

def open_popup():
    #ensures that a pop-up window has not been created yet
    if any(isinstance(x, tk.Toplevel) for x in window.winfo_children()):
        return
    window2= tk.Toplevel(window)
    # top.geometry("750x250")
    # top.title("Child window2")
    # Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)

    window2.geometry('414x600')
    window2.configure(bg='#FFFFFF')
    canvas=Canvas(window2,bg='#FFFFFF',height=600,width=414,bd=0,highlightthickness=0,relief='ridge')
    canvas.place(x=0,y=0)

    entry_image_1=PhotoImage(file=resource_path('entry_3.png'))
    entry_bg_1=canvas.create_image(117.5,309.0,image=entry_image_1)
    entry_1=Entry(window2, bd=0,bg='#F7F7F7',highlightthickness=0)
    entry_1.place(x=38.0,y=289.0,width=159.0,height=38.0)
    entry_1.config(textvariable=horvolt2)

    entry_image_2=PhotoImage(file=resource_path('entry_4.png'))
    entry_bg_2=canvas.create_image(117.5,229.0,image=entry_image_2)
    entry_2=Entry(window2, bd=0,bg='#F7F7F7',highlightthickness=0)
    entry_2.place(x=38.0,y=209.0,width=159.0,height=38.0) 
    entry_2.config(textvariable=horvolt)

    entry_image_3=PhotoImage(file=resource_path('entry_5.png'))
    entry_bg_3=canvas.create_image(117.5,388.0,image=entry_image_3)
    entry_3=Entry(window2, bd=0,bg='#F7F7F7',highlightthickness=0)
    entry_3.place(x=38.0,y=368.0,width=159.0,height=38.0)
    entry_3.config(textvariable=samploptpow)

    entry_image_4=PhotoImage(file=resource_path('entry_6.png'))
    entry_bg_4=canvas.create_image(300.5,309.0,image=entry_image_4)
    entry_4=Entry(window2, bd=0,bg='#F7F7F7',highlightthickness=0)
    entry_4.place(x=221.0,y=289.0,width=159.0,height=38.0) 
    entry_4.config(textvariable=vertvolt2)

    entry_image_5=PhotoImage(file=resource_path('entry_7.png'))
    entry_bg_5=canvas.create_image(300.5,229.0,image=entry_image_5)
    entry_5=Entry(window2, bd=0,bg='#F7F7F7',highlightthickness=0)
    entry_5.place(x=221.0,y=209.0,width=159.0,height=38.0)
    entry_5.config(textvariable=vertvolt)

    entry_image_6=PhotoImage(file=resource_path('entry_8.png'))
    entry_bg_6=canvas.create_image(300.5,388.0,image=entry_image_6)
    entry_6=Entry(window2, bd=0,bg='#F7F7F7',highlightthickness=0)
    entry_6.place(x=221.0,y=368.0,width=159.0,height=38.0)
    entry_6.config(textvariable=diffvolt)

    image_image_1=PhotoImage(file=resource_path('image_10.png'))
    image_1=canvas.create_image(207.0,302.0,image=image_image_1)
    entry_image_7=PhotoImage(file=resource_path('entry_9.png'))
    entry_bg_7=canvas.create_image(117.5,148.0,image=entry_image_7)
    entry_7=Entry(window2, bd=0,bg='#F7F7F7',highlightthickness=0)
    entry_7.place(x=38.0,y=128.0,width=159.0,height=38.0)
    entry_7.config(textvariable=filepath)
    
    canvas.create_text(52.0,182.0,anchor='nw',text='Horizontal Voltage',fill='#191919',font=('Inter SemiBold',15*-1))
    canvas.create_text(46.0,267.0,anchor='nw',text='Horizontal Voltage 2',fill='#191919',font=('Inter SemiBold',15*-1))
    canvas.create_text(45.0,347.0,anchor='nw',text='Sample Optical Pow',fill='#191919',font=('Inter SemiBold',15*-1))
    canvas.create_text(243.0,182.0,anchor='nw',text='Vertical Voltage',fill='#191919',font=('Inter SemiBold',15*-1))
    canvas.create_text(86.0,103.0,anchor='nw',text='File Path',fill='#191919',font=('Inter SemiBold',15*-1))
    canvas.create_text(236.0,267.0,anchor='nw',text='Vertical Voltage 2',fill='#191919',font=('Inter SemiBold',15*-1))
    canvas.create_text(244.0,347.0,anchor='nw',text='CurrDetDiffVolt',fill='#191919',font=('Inter SemiBold',15*-1))

    def browse_files():
        filename = filedialog.askopenfilename()
        entry_7.delete(0, tk.END)
        entry_7.insert(tk.END, filename)
        window2.lift()
        window2.focus_force()
        window2.grab_set()
        window2.grab_release()

    #load entries
    # entries = [entry_9, entry_7, entry_2, entry_4, entry_1, entry_5, entry_3, entry_6]
    # entry_names = ["port", "filepath", "horvolt2", "vertvolt2", "horvolt", "vertvolt", "samploptpow", "currdetdiffvolt"]
    # for i in range(1, len(entries)): 
    #     val = data.get(entry_names[i])
    #     if val is not None:
    #         entries[i].insert(0, val)

    def save(): 
        save_vals = {}
        #fetch the addresses entered into these entries
        entries = [port, filepath, horvolt2, vertvolt2, horvolt, vertvolt, samploptpow, diffvolt]
        entry_names = ["port", "filepath", "horvolt2", "vertvolt2", "horvolt", "vertvolt", "samploptpow", "currdetdiffvolt"]
        for i in range(len(entries)): 
            val = entries[i].get()
            save_vals[entry_names[i]] = val 

        print("Save Values:")
        print(save_vals)
        file = open(resource_path("info.json"), "w")
        file.write(json.dumps(save_vals))
        file.close()

    button_image_1=PhotoImage(file=resource_path('button_3.png'))
    button_1=Button(window2, image=button_image_1,borderwidth=0,highlightthickness=0,command=save,relief='flat')
    button_1.place(x=133.0,y=40.0,width=151.0,height=37.0)

    button_image_2=PhotoImage(file=resource_path('button_4.png'))
    button_2=Button(window2, image=button_image_2,borderwidth=0,highlightthickness=0,command=browse_files,relief='flat')
    button_2.place(x=212.0,y=126.0,width=46.0,height=46.0)
    window2.resizable(False,False)
    window2.mainloop()

button_image_2=PhotoImage(file=resource_path('button_2.png'))
button_2=Button(image=button_image_2,borderwidth=0,highlightthickness=0,command=open_popup,relief='flat')
button_2.place(x=579.0,y=19.0,width=50.0,height=51.0)

window.resizable(False,False)
window.mainloop()