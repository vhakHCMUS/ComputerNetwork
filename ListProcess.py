import wmi
 
# List all running processes
def ListGet():
    res = []
    f = wmi.WMI()
    for process in f.Win32_Process():
        res.append([process.ProcessId, process.Name])
    return res