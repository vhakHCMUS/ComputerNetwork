import subprocess
import os
import utils
import winapps

def ListApp(command):
    ans = {
        'Description': []
    }
    if '-version' in command:
        ans['FileVersion'] = []
    if '-path' in command:
        ans['Path'] = []

    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select '
    for attribute in ans:
        run = cmd + attribute
        proc = subprocess.Popen(run, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            item = line.decode().rstrip()
            ans[attribute].extend([item])
        ans[attribute] = ans[attribute][3:]
    table = utils.dicToHTML(ans)
    return table

def ListAllApp(command):
    ans = {
        'Applications':[]
    }
    if '-version' in command:
        ans['Version'] = []
    if '-path' in command:
        ans['Path'] = []

    for item in winapps.list_installed():
        appName = item.name
        version = item.version
        path = item.install_location
        ans['Applications'].append(appName)
        if (command == '-version'):
            ans['Version'].append(version)
        elif (command == '-path'):
            ans['Path'].append(path)
    table = utils.dicToHTML(ans)
    return table

def OpenApp(path):
    # eg path: C:\Users\Admin\Desktop\ComputerNetwork\app_name.exe
    os.startfile(path)

def StopApp(executeFile):
    # eg executeFile: app_name.exe
    subprocess.call(["taskkill","/F","/IM", executeFile])