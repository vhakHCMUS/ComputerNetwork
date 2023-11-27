import wmi
import utils
import pythoncom

# List all running processes
def ListGet():
    pythoncom.CoInitialize()
    res = {'Id':[],'Name':[]}
    f = wmi.WMI()
    for process in f.Win32_Process():
        res['Id'].append(process.ProcessId)
        res['Name'].append(process.Name)
    table = utils.dicToHTML(res)
    pythoncom.CoUninitialize()
    return table

# Stop a process
def StopProc(procName):
    pythoncom.CoInitialize()
    f = wmi.WMI()
    for process in f.Win32_Process():
        if process.Name == procName:
            process.Terminate()
            pythoncom.CoUninitialize()
            return
    pythoncom.CoUninitialize()
    return