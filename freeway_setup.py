# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
FreewayInfo object is used to help identify information from the game window.
"""
import ctypes
from ctypes import wintypes
import time
import pyautogui
from ugly_math import num_to_location
from free_wind import check_saved_data, load_layout, get_freeway_winfo
from free_wind import get_wef_colors, get_graycount
from compiler import find_solution

user32 = ctypes.windll.user32

GAME = "Freeways"

ctypes.windll.user32.GetWindowRect.argtypes = [
    wintypes.HWND,
    wintypes.LPRECT]

class FreewayInfo():
    """
    Object used to extract information from a game window.  Data saved
    in this class includes:
        hwnd -- The handle of the window
        bounds -- The left, top, right, bottom bounds of the window
        img -- a PIL image grabbed from the screen
    """
    def __init__(self):
        hwnd, bounds, img = get_freeway_winfo()
        self.hwnd = hwnd
        self.bounds = bounds
        self.img = img
        self.layout = load_layout()
        self.butt_stat = [False, False]

    def match_pattern(self):
        """
        Test to see if certain numbers of certain pixels are on the page.

        @param pat_desc -- pattern passed to get_wef_colors

        @return True if this pattern matches the layout in
                self.layout['wef_info'], False if not.
        """
        wef_cols = get_wef_colors(self.img)
        for count, numbr in enumerate(self.layout['wef_info']):
            if abs(wef_cols[count] - numbr) > 5:
                return False
        return True

    def am_i_bigmap(self):
        """
        Return True if the world map is being displayed.
        False if the game display is one of the 81 levels
        """
        return self.match_pattern()

    def go_to_level(self, number):
        """
        Go to the individual map specified

        @param integer number - map number in range 0 to 80
        """
        xy_coord = num_to_location(number)
        if xy_coord[0] < 0:
            print("Invalid map number specified")
            return
        adj_header = self.bounds[3] - self.bounds[1]
        xoff = ((self.bounds[2] - self.bounds[0]) // 9) // 2
        yoff = (adj_header // 9) // 2
        xcoord = (xy_coord[0] * 2 + 1) * xoff
        ycoord = (xy_coord[1] * 2 + 1) * yoff
        xcoord += self.bounds[0]
        ycoord += self.bounds[1]
        pyautogui.moveTo(x=xcoord, y=ycoord)
        pyautogui.click()
        time.sleep(5)

    def go_to_world_map(self):
        """
        Click on the world map icon in the menu
        """
        if self.am_i_bigmap():
            return
        self.find_menu(70, True)
        time.sleep(5)

    def clear_level(self):
        """
        Click on the clear page icon in the menu
        """
        self.find_menu(140, True)

    def stopwatch(self):
        """
        Score this level
        """
        time.sleep(1)
        self.find_menu(70, False)
        time.sleep(20)
        self.find_menu(0, False)

    def ramp_up(self):
        """
        Click on the yellow up ramp
        """
        self.find_menu(140, False)

    def ramp_down(self):
        """
        Click on the yellow down ramp
        """
        self.find_menu(210, False)

    def find_menu(self, shiftsize, page_switch):
        """
        For individual pages, click on some of the menu icons.

        @param shiftsize integer -- Distance we shift to the right in order
                                    to find a new icon  to click
        """
        if self.am_i_bigmap():
            return
        print(self.bounds)
        origpos = pyautogui.position()
        pyautogui.mouseUp(button='left')
        pyautogui.mouseUp(button='right')
        bestsofar = self.layout['graycount']
        bestchunk = 0
        for chunk in range(0, 3):
            graycnt = get_graycount(chunk, self.img)
            print("DEBUG graycnt", chunk, graycnt, self.layout['graycount'])
            gcdiff = abs(graycnt - self.layout['graycount'])
            if gcdiff < 10:
                bestchunk = chunk
                break
            if gcdiff < bestsofar:
                bestsofar = gcdiff
                bestchunk = chunk
        xoffset = [34, 471, 900][bestchunk]
        xbc = self.bounds[0] + xoffset
        print ("xbc is", self.bounds[0], "plus", xoffset)
        ybc = self.bounds[3] - 40
        if page_switch:
            print("first menu click ", xbc, ybc)
            pyautogui.moveTo(x=xbc, y=ybc)
            pyautogui.click()
        xbc += shiftsize
        print("second menu click ", xbc, ybc)
        pyautogui.moveTo(x=xbc, y=ybc)
        pyautogui.click()
        pyautogui.moveTo(x=origpos[0], y=origpos[1])
        if self.butt_stat[0]:
            pyautogui.mouseDown(button='left')
        if self.butt_stat[1]:
            pyautogui.mouseDown(button='right')

def setup(level):
    """
    Find a solution for the given level number

    @param level -- number from 0 to 80
    """
    check_saved_data()
    time.sleep(5)
    fwy_info = FreewayInfo()
    fwy_info.go_to_world_map()
    fwy_info = FreewayInfo()
    fwy_info.go_to_level(level)
    fwy_info = FreewayInfo()
    find_solution(level, fwy_info)
    print("Done")

if __name__ == "__main__":
    setup(1)
