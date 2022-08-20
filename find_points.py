# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Print mouse location.  This tool is used to find locations to draw on
the new map
"""
import sys
import time
import pyautogui
from pynput import mouse
import freeway_setup

def find_a_point():
    """
    Vestigial code
    """
    fwy_info = freeway_setup.FreewayInfo()
    point = [""]
    def on_clicka(xpoint, ypoint, button, pressed):
        nonlocal fwy_info
        locx = round(xpoint * 4 / 5)
        locy = round(ypoint * 4 / 5)
        xval = locx - fwy_info.bounds[0]
        yval = locy - fwy_info.bounds[1]
        point[0] = [xval, yval]
        if button | pressed:
            print("button")
        return False
    listener = mouse.Listener(on_click=on_clicka)
    listener.start()
    while True:
        time.sleep(1)
    return point[0]

def find_points():
    """
    This runs until the mouse is moved left of the Freeways window.
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

def click_points():
    """
    Use clicks to generate line code.  Data written to linedata.txt
    """
    drawing = True
    oline = ""
    fwy_info = freeway_setup.FreewayInfo()
    def on_click(xpoint, ypoint, button, pressed):
        nonlocal drawing, oline
        xvar = round(xpoint * 4 / 5)
        yvar = round(ypoint * 4 / 5)
        xval = xvar - fwy_info.bounds[0]
        yval = yvar - fwy_info.bounds[1]
        if xvar < fwy_info.bounds[0]:
            drawing = False
            return False
        if pressed:
            # oline = "line {0},{1} ".format(xval, yval)
            oline = f"line {xval},{yval} "
        else:
            # oline +="{0},{1} A;\n".format(xval, yval)
            oline += f"{xval},{yval} A;\n"
            print(oline)
            with open("linedata.txt", "a", encoding="utf8") as ofile:
                ofile.write(oline)
            oline = ""
        if button:
            print("button")
        return True
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    while drawing:
        time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        find_points()
    else:
        click_points()
