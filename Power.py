import os

def shutdown():
    return os.system("shutdown /s /t 1")
 
def restart():
    return os.system("shutdown /r /t 1")
 
def logout():
    return os.system("shutdown -l")