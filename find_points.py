# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Print mouse location.  This tool is used to find locations to drraw on
the new map
"""
import time
import pyautogui
import freeway_setup

def find_points():
    """
    This runs until the mouse is moved left or above the Freeways window.
    It prints coordinates of mouse locations evvery five seconds.
    """
    fwy_info = freeway_setup.FreewayInfo()
    print(fwy_info.bounds)
    while True:
        xval, yval = pyautogui.position()
        xval -= fwy_info.bounds[0]
        yval -= fwy_info.bounds[1]
        if xval < 0:
            break
        print(xval, yval)
        time.sleep(5)

if __name__ == "__main__":
    find_points()
