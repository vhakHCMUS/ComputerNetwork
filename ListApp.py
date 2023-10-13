import subprocess
import os

def ListApp(path):
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    if path:
        cmd += ',Path'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ans = []
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            ans.append(line.decode().rstrip())
    ans.append("end")
    return ans

def OpenApp(path):
    # eg path: C:\Users\Admin\Desktop\ComputerNetwork\app_name.exe
    os.startfile(path)

def StopApp(executeFile):
    # eg executeFile: app_name.exe
    subprocess.call(["taskkill","/F","/IM", executeFile])