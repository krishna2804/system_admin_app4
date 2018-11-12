#from functions import *
from tkinter import *
from subprocess import Popen,PIPE
import subprocess
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import pandas as  pd
import numpy as np
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def password():
    passwd = simpledialog.askstring("Password","Enter your password",show="*",parent=window)
    return passwd

def manage_log():

    facility=facility_name.get()
    symbol=symbol_type.get()
    level=severity_level.get()
    file=path_type.get()
    if(file==''):
        messagebox.showinfo("WARNING: ", "enter valid log file")
    else:
        password1=password()
        command="echo "+password1+" | sudo -S touch "+file+""
        subprocess.call(command,shell=True)

    input=facility+"."+symbol+""+level+"    "+file
    print(input)
    password1=password()
    command="echo "+password1+" | sudo -S chmod 777 manage.sh"
    #subprocess.call(command)
    command2="echo "+password1+" | sudo -S ./manage.sh "+input
    print(command2)
    os.system(command)
    os.system(command2)
    #command="echo "+password1+" | sudo -S echo "+input+" >> /etc/rsyslog.d/50-default.conf"
    #subprocess.call(command,shell=True)
    messagebox.showinfo("sucess", "log file updated")


def logrotate():
    path_log=log_path.get()
    file_size=size.get()
    rotation_time=time.get()
    number=no_file.get()
    compressor=comp_type.get()
    radio1=rad1_option.get()
    radio2=rad2_option.get()
    radio3=rad3_option.get()
    timing=''
    sizer=''
    checking=''
    print(radio3)
    if int(radio3) == 1:
        print("yes")
        check_value = "notifempty"
        checking=str("    notifempty"+"\n")

    if rotation_time != "":
        timing=str("    "+str(rotation_time)+"\n")

    if file_size != "":
        sizer=str("    size "+str(file_size)+"\n")

    command2 = "rm log_entry.txt"
    print(command2)
    subprocess.call(command2, shell=True)

    file = open("log_entry.txt","w+")
    content=str(path_log)+'\n '+\
            '{\n'+\
            '    rotate '+number+'\n'+\
            timing+\
            sizer+\
            '    '+str(compressor)+'\n'+\
            checking+\
            '}\n'
    file.write(content)
    file.close()
    password1=password()

    command4 = "echo \""+password1+"\" | sudo -S touch "+path_log
    print(command4)
    subprocess.call(command4, shell=True)

    command6 = "echo \""+password1+"\" | sudo -S chmod 777 /etc/logrotate.d/rsyslog"
    print(command6)
    subprocess.call(command6, shell=True)

    command5 = "echo \""+password1+"\" | sudo -S cat log_entry.txt >> /etc/logrotate.d/rsyslog"
    print(command5)
    subprocess.call(command5, shell=True)

    messagebox.showinfo("Log rotate", "Successfully Done")


window = Tk()
window.configure(background='lavender')

window.title('SYSTEM ADMIN TOOL TO MANAGE LOG FILES')
note = ttk.Notebook(window)

tab1 = ttk.Frame(note)
tab2 = ttk.Frame(note)
#tab3 = ttk.Frame(note)
#tab4 = ttk.Frame(note)

note.add(tab1, text = "Manage rsyslog configuration")
note.add(tab2, text = "Manage log rotation")
#note.add(tab3, text = "ACESS CONTROL")
#note.add(tab4, text = "CONTROL")

note.pack(expand=1,fill="both")

#-----------------------------tab1 content---------------------------------------
facility = ['*', 'kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'cron', 'authprev','ftp', 'mark','local0','local1','local2','local3','local4','local5','local6','local7']
symbols=['!','=',',']
severity=['*', 'none', 'emerg', 'alert', 'crit', 'err', 'warning', 'notice', 'info', 'debug']


facility_name=StringVar()
facility_name.set('kern')
symbol_type=StringVar()
symbol_type.set('=')
severity_level=StringVar()
severity_level.set('emerg')
path_type=StringVar()

timings=['daily', 'weekly', 'monthly']
compres=['compress', 'delaycompress']
log_path=StringVar()
size=StringVar()
time=StringVar()
no_file=StringVar()
comp_type=StringVar()
rad1_option=StringVar()
rad2_option=StringVar()
rad3_option=StringVar()
rad1_option.set(1)
rad2_option.set(0)
rad3_option.set(0)

def sizee():
    value=int(rad1_option.get())
    #print(value)
    if(value == 0):
        print(value)
        entry1 =Entry(tab1_frame1,textvariable=size,width=10)
        entry1.grid(row=3,column=3,padx=10,pady=5,sticky=W)
        entry1.config(state='disabled')
    else:
        print("---",value)

        entry1 =Entry(tab1_frame1,textvariable=size,width=10)
        entry1.grid(row=3,column=3,padx=10,pady=5,sticky=W)


def fileframe():

    tab1_frame1 =LabelFrame(tab1,fg="brown",font="15",bg="lavender",bd=5,width=500, height=80)
    tab1_frame1.grid(row=1, column=1,padx=50,pady=15)

    label1=Label(tab1_frame1,text="Manage log file",fg="blue",width=55,bg="pink",font="40",borderwidth=2, relief="raised")
    label1.grid(row=1,column=1,columnspan=8,padx=10,pady=5)

    label1=Label(tab1_frame1,text="Facility: ",borderwidth=2, relief="groove",width=25,anchor=W)
    label1.grid(row=2,column=1,padx=10,pady=5)
    label1=Label(tab1_frame1,text="Level:",borderwidth=2, relief="groove",width=25,anchor=W)
    label1.grid(row=3,column=1,padx=5,pady=5)
    label1=Label(tab1_frame1,text="logfile to store log entries:",borderwidth=2, relief="groove",width=25,anchor=W)
    label1.grid(row=4,column=1,padx=10,pady=5)

    option1 = OptionMenu(tab1_frame1,facility_name, *facility)
    option1.grid(row=2,column=3,columnspan=2,padx=8, pady=5)
    option1.config(font=('calibri',(10)),bg='white',width=12)
    option1['menu'].config(font=('calibri',(10)),bg='white')

    option2 = OptionMenu(tab1_frame1, symbol_type, *symbols)
    option2.grid(row=3,column=2,columnspan=1,padx=8, pady=5)
    option2.config(font=('calibri',(10)),bg='white',width=5)
    option1['menu'].config(font=('calibri',(10)),bg='white')

    option3 = OptionMenu(tab1_frame1,severity_level, *severity)
    option3.grid(row=3,column=3,columnspan=2,padx=8, pady=5)
    option3.config(font=('calibri',(10)),bg='white',width=12)
    option3['menu'].config(font=('calibri',(10)),bg='white')

    entry1 =Entry(tab1_frame1,textvariable=path_type)
    entry1.grid(row=4,column=3,padx=10,pady=5)


    button1 =Button (tab1_frame1, text='ok',bg="orange",width=3,command=manage_log)
    button1.grid(row=5,column=2,columnspan=1,padx=1,pady=5)


    button1 =Button (tab1_frame1, text='Exit',bg="red", command=window.destroy)
    button1.grid(row=5,column=3,padx=1,pady=5,sticky=W)

#-------------------------FRAME2------------IN TAB1-----------------------

tab1_frame1 =LabelFrame(tab2,fg="brown",font="15",bg="lavender",bd=5,width=500, height=80)
tab1_frame1.grid(row=1, column=1,padx=50,pady=15)
def size_enable():
    value=int(rad1_option.get())
    #print(value)
    if(value == 0):
        print(value)
        entry1 =Entry(tab1_frame1,textvariable=size,width=20)
        entry1.grid(row=3,column=3,padx=10,pady=5,sticky=W)
        entry1.config(state='disabled')
    else:
        print("---",value)

        entry1 =Entry(tab1_frame1,textvariable=size,width=10)
        entry1.grid(row=3,column=3,padx=10,pady=5,sticky=W)
def time_enable():
    value=int(rad2_option.get())
    #print(value)
    if(value == 0):
        print(value)
        option1 = OptionMenu(tab1_frame1,time ,*timings)
        option1.grid(row=4,column=3,columnspan=2,padx=8, pady=5,sticky=W)
        option1.config(font=('calibri',(10)),bg='white',width=12)
        option1['menu'].config(font=('calibri',(10)),bg='white')
        option1.configure(state="disabled")
    else:
        option1 = OptionMenu(tab1_frame1,time ,*timings)
        option1.grid(row=4,column=3,columnspan=2,padx=8, pady=5,sticky=W)
        option1.config(font=('calibri',(10)),bg='white',width=12

        )
        option1['menu'].config(font=('calibri',(10)),bg='white')

size=StringVar()

def fileframe2():

    #tab1_frame1 =LabelFrame(tab2,fg="brown",font="15",bg="lavender",bd=5,width=500, height=80)
    #tab1_frame1.grid(row=1, column=1,padx=50,pady=15)

    label1=Label(tab1_frame1,text="Log rotation",fg="blue",width=55,bg="pink",font="40",borderwidth=2, relief="raised")
    label1.grid(row=1,column=1,columnspan=8,padx=10,pady=5)

    label1=Label(tab1_frame1,text="select log file:",borderwidth=2, relief="groove",width=25,anchor=W)
    label1.grid(row=2,column=1,padx=10,pady=5)
    entry1 =Entry(tab1_frame1,textvariable=log_path)
    entry1.grid(row=2,column=3,padx=10,pady=5,sticky=W)

    label1=Label(tab1_frame1,text="Log rotation: ",borderwidth=2, relief="groove",width=25,anchor=W)
    label1.grid(row=2,column=1,padx=10,pady=5)

    radio1=Checkbutton(tab1_frame1, text='size', var=rad1_option,onvalue=1, offvalue=0,width=7,command=size_enable)
    #radio1=Radiobutton(tab1_frame1,text="size",padx =10,variable=rad1_option,value='g')
    radio1.grid(row=3,column=1,padx=5,pady=5,sticky=E)
    if(int(rad1_option.get())==0):
        entry1 =Entry(tab1_frame1,textvariable=size,width=10)
        entry1.grid(row=3,column=3,padx=10,pady=5,sticky=W)
        entry1.config(state='disabled')

    else:
        entry1 =Entry(tab1_frame1,textvariable=size,width=10)
        entry1.grid(row=3,column=3,padx=10,pady=5,sticky=W)



    radio1=Checkbutton(tab1_frame1, text='time', var=rad2_option,onvalue=1, offvalue=0,width=7,command=time_enable)
    #radio1=Radiobutton(tab1_frame1,text="time",padx =10,variable=rad2_option,value='u')
    radio1.grid(row=4,column=1,padx=10,pady=5,sticky=E)
    if(int(rad2_option.get())==0):
        option1 = OptionMenu(tab1_frame1,time ,*timings)
        option1.grid(row=4,column=3,columnspan=2,padx=8, pady=5,sticky=W)
        option1.config(font=('calibri',(10)),bg='white',width=12)
        option1['menu'].config(font=('calibri',(10)),bg='white')
        option1.configure(state="disabled")
    else:
        option1 = OptionMenu(tab1_frame1,time ,*timings)
        option1.grid(row=4,column=3,columnspan=2,padx=8, pady=5,sticky=W)
        option1.config(font=('calibri',(10)),bg='white',width=12)
        option1['menu'].config(font=('calibri',(10)),bg='white')


    label1=Label(tab1_frame1,text="number of log file:",borderwidth=2, relief="groove",width=25,anchor=W)
    label1.grid(row=5,column=1,padx=10,pady=5)
    entry1 =Entry(tab1_frame1,textvariable=no_file)
    entry1.grid(row=5,column=3,padx=10,pady=5,sticky=W)

    label1=Label(tab1_frame1,text="compression:",borderwidth=2, relief="groove",width=25,anchor=W)
    label1.grid(row=6,column=1,padx=10,pady=5)
    option2 = OptionMenu(tab1_frame1,comp_type, *compres)
    option2.grid(row=6,column=3,columnspan=2,padx=8, pady=5,sticky=W)
    option2.config(font=('calibri',(10)),bg='white',width=12)
    option2['menu'].config(font=('calibri',(10)),bg='white')

    radio1=Checkbutton(tab1_frame1, text='Do not rotate if log file empty', var=rad3_option,onvalue=1, offvalue=0,width=30,anchor=W)
    radio1.grid(row=7,column=1,padx=10,pady=5,sticky=W)

    button1 =Button (tab1_frame1, text='ok',bg="orange",width=3,command=logrotate)
    button1.grid(row=8,column=2,columnspan=1,padx=1,pady=5)

    button1 =Button (tab1_frame1, text='Exit',bg="red", command=window.destroy)
    button1.grid(row=8,column=3,padx=1,pady=5,sticky=W)

fileframe()
fileframe2()


window.mainloop()
exit()
