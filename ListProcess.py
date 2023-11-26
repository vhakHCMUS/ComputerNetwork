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