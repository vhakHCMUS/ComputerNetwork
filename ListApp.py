import subprocess
import pandas
import os
import utils

def ListApp(havePath):
    ans = {
        'Description':[],
        'Id':[],
    }
    if havePath:
        ans['Path'] = []
    for i in ans:
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select '
        cmd += f'{i}'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            ans[i].append(line.decode().rstrip())
        ans[i] = ans[i][3:]
    table = utils.dicToHTML(ans)
    return table

def OpenApp(path):
    # eg path: C:\Users\Admin\Desktop\ComputerNetwork\app_name.exe
    os.startfile(path)

def StopApp(executeFile):
    # eg executeFile: app_name.exe
    subprocess.call(["taskkill","/F","/IM", executeFile])