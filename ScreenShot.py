import pyautogui
import datetime

def capture(): 
    # Get the current date and time to use in the screenshot filename
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")

    # # Specify the filename for the screenshot
    screenshotFilename = f"screenshot_{timestamp}.png"

    # # Take a screenshot of the entire screen and save it
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshotFilename)

    print(f"Screenshot saved as {screenshotFilename}")
    return screenshotFilename