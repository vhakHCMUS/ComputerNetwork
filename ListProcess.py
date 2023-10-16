import wmi
import utils
 
# List all running processes
def ListGet():
    res = {'Id':[],'Name':[]}
    f = wmi.WMI()
    for process in f.Win32_Process():
        res['Id'].append(process.ProcessId)
        res['Name'].append(process.Name)
    table = utils.dicToHTML(res)
    return table