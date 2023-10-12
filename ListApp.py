import subprocess

def ListApp():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    listOfRunningApp = []
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            listOfRunningApp.append(line.decode().rstrip())
    listOfRunningApp.append("end")
    return listOfRunningApp