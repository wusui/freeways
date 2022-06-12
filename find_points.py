"""
Print mouse location.  This tool is used to find locations to drraw on
the new map
"""
import time
import pyautogui
import freeway_input

def find_points():
    """
    This runs until the mouse is moved to the extreme left side of the page.
    It prints coordinates of mouse locations evvery five seconds.
    """
    fwy_info = freeway_input.FreewayInfo()
    print(fwy_info.bounds)
    while True:
        xval, yval = pyautogui.position()
        if xval < 100:
            break
        print(xval, yval)
        time.sleep(5)

if __name__ == "__main__":
    find_points()
