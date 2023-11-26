import tkinter as tk
import threading
import time
import os
import EmailHandler as em
import KeyLogger as keyl
import ListApp as app
import ListProcess as proc
import ScreenShot
import Power
from tkinter import *
from functools import partial
import MailList as mlist

DEFAULT_KEYLOG_TIME = 300

BG_COLOR = 'brown'

mailList = mlist.MailList()
email = em.EmailHandler()
RunningMainLoop = False
Executing = False
def run_main_loop():
    global RunningMainLoop
    global Executing
    global text_box
    global stop_button
    RunningMainLoop = True
    waitCounter = 0
    idler = ['   ', '.  ', '.. ', '...']
    while RunningMainLoop:
        command = email.readLastestEmail()
        cmd = command[1].split()
        print(f'Waiting for next command{idler[waitCounter]}\r', end='')
        waitCounter = 0 if waitCounter == 3 else waitCounter + 1 
    
        result = ''
        image = None
        shutd = restart = logout = False
        
        if 'EMPTY' in cmd:
            Executing = False
            continue
        os.system('cls')
        Executing = True
        text_box.configure(state="normal")
        text_box.delete(1.0, tk.END)
        if command[2] not in mailList.data:
            text_box.insert(1.0, "Received unregistered mail")
            result = 'You are not register, please contact the server admin'

        elif cmd[0] == 'screenshot':
            result = 'Screenshot captured'
            text_box.insert(1.0, "Executing screenshot\n")
            image = ScreenShot.capture()
            text_box.insert(tk.END, "\nExecuted screenshot\n\n")

        elif cmd[0] == 'keylog':
            keylTime = DEFAULT_KEYLOG_TIME
            if '-t' in cmd:
                keylTime = int(cmd[cmd.index('-t') + 1])
            keylog = keyl.Keylogger(keylTime)
            print('Capturing...')
            text_box.insert(1.0, "Executing keylogger\n")
            stop_button['state'] = tk.DISABLED
            keys = keylog.run()
            stop_button['state'] = tk.NORMAL
            text_box.insert(tk.END, "\nExecuted keylogger\n\n")
            print('Finished')
            if '-both' in cmd:
                result += keys
                result += f'<br>Log: {keylog.getLog()}'
            elif '-l' in cmd:
                result += f'<br>Log: {keylog.getLog()}'
            else:
                result += keys
            

        elif cmd[0] == 'app':
            text_box.insert(1.0, "Executing app list\n")
            if cmd[1] == 'list':
                if '-all' in cmd:
                    appList = app.ListAllApp(cmd)
                else:
                    appList = app.ListApp(cmd)
                result += appList
            elif cmd[1] == '-end':
                app.StopApp(cmd[2])
                result = 'Stopped'
            else:
                app.OpenApp(cmd[2])
                result = 'Opened'
            text_box.insert(tk.END, "Executed app list\n")

        elif cmd[0] == 'proc':
            text_box.insert(1.0, "Executing process list\n")
            if cmd[1] == 'list':
                procList = proc.ListGet()
                result += procList
            text_box.insert(tk.END, "Executed process list\n")

        elif cmd[0] == 'shutdown':
            shutd = True
            result = 'Shutdown'
        
        elif cmd[0] == 'restart':
            restart = True
            result = 'Restarted'
        
        elif cmd[0] == 'logout':
            logout = True
            result = 'Logged out'

        else:
            print('Error: Command not found')
            result = 'Error: Command not found'
        
        sender = command[2]
        if result != '':
            email.sendMail(sender, 'Your request has been executed', result, image)
        time.sleep(1)
        if shutd:
            Power.shutdown()
        elif restart:
            Power.restart()
        elif logout:
            Power.logout()
        text_box.configure(state="disabled")

# Function to start the main loop in a separate thread
def start_main_loop():
    global main_loop_thread
    main_loop_thread = threading.Thread(target=run_main_loop)
    main_loop_thread.daemon = True  # Allows the thread to be terminated when the application is closed
    main_loop_thread.start()

# Function to stop the main loop
def stop_main_loop():
    global RunningMainLoop
    RunningMainLoop = False
    if main_loop_thread and main_loop_thread.is_alive():
        main_loop_thread.join()  # Stop the main loop thread
        os.system('cls')
        print("Main loop successfully stopped.")

# Function to add new email
def addMail(newEmail):
    if newEmail.get() in mailList.data:
        return
    mailList.addMail(newEmail.get())
    mail_list_box.configure(state="normal")
    mail_list_box.insert(tk.END,f'{newEmail.get()}\n')
    mail_list_box.configure(state="disabled")
# Create the main Tkinter window
root = tk.Tk()
root.title("Main Loop Control")
root.configure(bg=BG_COLOR)

# status
statusLabel = tk.Label(root, text='Status:', bg=BG_COLOR, fg='white', font='Helvetica 10 bold')
statusLabel.grid(row=0,column=0, padx=(10,0), pady=(10,0), sticky='w')
# Create "Start" button
start_button = tk.Button(root, text="Start", command=start_main_loop, width=10)
start_button.grid(row=1, column=2, padx=(10,10), pady=(0,0))

# Create "Stop" button
stop_button = tk.Button(root, text="Stop", command=stop_main_loop, width=10)
stop_button.grid(row=2, column=2, padx=(10,10), pady=(0,0))

# Create "Status" label
text_box = tk.Text(root, height=4, width=50, font='Helvetica')
text_box.grid(row=1, column=0, rowspan=2, columnspan=2, padx=(10,10), pady=(0,0))

# Email label and text entry box
def focus_out_entry_box(widget, widget_text):
    if widget['fg'] == 'Black' and len(widget.get()) == 0:
        widget.delete(0, END)
        widget['fg'] = 'Grey'
        widget.insert(0, widget_text)

def focus_in_entry_box(widget):
    if widget['fg'] == 'Grey':
        widget['fg'] = 'Black'
        widget.delete(0, END)

newEmail = tk.StringVar()
emailEntry = tk.Entry(root, textvariable=newEmail, width=50, fg='Grey', font='Helvetica')
emailEntry.insert(0,'input new email here')
emailEntry.bind("<FocusIn>", lambda args: focus_in_entry_box(emailEntry))
emailEntry.bind("<FocusOut>", lambda args: focus_out_entry_box(emailEntry, 'input new email here'))
emailEntry.grid(row=3, column=0, columnspan=2, sticky='w', pady=(10,10), padx=(10,10))
addMail = partial(addMail,newEmail)
 
# add mail button
addButton = tk.Button(root, text="Add Email", command=addMail, width=10)
addButton.grid(row=3, column=2, padx=(10,10), pady=(10,10)) 

listLabel = tk.Label(root, text='Email list:', bg=BG_COLOR, fg='white', font='Helvetica 10 bold')
listLabel.grid(row=4,column=0, padx=(10,0), sticky='w')
# Showing email list
mail_list_box = tk.Text(root, height=20, width=62, font='Helvetica')
mail_list_box.grid(row=5, column=0, columnspan=3, padx=(10,10), pady=(0,15))

def update_text():
    global RunningMainLoop
    global Executing
    text_box.configure(state="normal")
    if not Executing:
        if RunningMainLoop:
            text_box.delete("end-1c linestart", "end")
            text_box.insert(tk.END, "\nThe server is running.")
        else:
            text_box.delete("end-1c linestart", "end")
            text_box.insert(tk.END, "\nThe server is not running.")
    text_box.configure(state="disabled")

    root.after(1000, update_text)  # Update the text every 1000 milliseconds (1 second)
# Start the Tkinter main loop
update_text()
for line in mailList.data:
    mail_list_box.insert(tk.END,f'{line}\n')
mail_list_box.configure(state="disabled")
root.resizable(False,False)
os.system('cls')
root.mainloop()