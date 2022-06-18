# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Code to make sure currently executing Freeways location data is correct.
A json file (layout.json) is kept in the current directory storing the
window information.  This will get updated upon creation of a FreewayInfo
object whenever the currently executing Freeways window is newer than
the json file.  Current data stored there are page image related data used
to determine which page we are on, and gray scale pixel count to find where
the menu button is for a given level.
"""
import time
from os.path import exists
import datetime
import json
import pathlib
import wmi
import dateutil.parser
import pyautogui

import win32gui
import win32api
import win32process
from PIL import ImageGrab

from win32con import PROCESS_QUERY_INFORMATION, PROCESS_VM_READ

GAME = "Freeways.exe"
SAVED_INFO_FILE = "cmpvalues.json"

class FreewayException(Exception):
    """
    Exception thrown when attempting to collect Freeway info while
    Freeways game is not running.
    """

def get_gm_window():
    """
    Look through all process and find the pid of the Freeways game.

    @param processId int -- process id of Freeways, -1 if not running
    """
    fwmi = wmi.WMI()
    for process in fwmi.Win32_Process():
        if process.Name == GAME:
            return process.ProcessId
    return -1

def set_saved_data():
    """
    Collect data and set values for the cmpvalues.json file.  Values are
    the distribution of colors at the start of a world map, and a graycount
    for the menu area.
    """
    fw_info = get_freeway_winfo()
    retv = {}
    retv['wef_info'] = get_wef_colors(fw_info[2])
    xcoord = fw_info[1][0] + 20
    ycoord = fw_info[1][1] + 20
    pyautogui.moveTo(x=xcoord, y=ycoord)
    pyautogui.click()
    time.sleep(2)
    fw_info = get_freeway_winfo()
    retv['graycount'] = get_graycount(0, fw_info[2])
    with open(SAVED_INFO_FILE, "w", encoding="utf8") as outfile:
        json.dump(retv, outfile)

def check_saved_data():
    """
    Set saved data if the file does not exist, or if the file is older
    that the current running Freeway.exe
    """
    mask = PROCESS_QUERY_INFORMATION | PROCESS_VM_READ
    gm_wind = get_gm_window()
    if gm_wind < 0:
        return
    handle = win32api.OpenProcess(mask, False, gm_wind)
    data = win32process.GetProcessTimes(handle)
    wtime = dateutil.parser.parse(str(data['CreationTime']))
    if not exists(SAVED_INFO_FILE):
        set_saved_data()
        return
    file_time = pathlib.Path(SAVED_INFO_FILE).stat().st_mtime
    ftime = datetime.datetime.fromtimestamp(file_time,
                                            tz=datetime.timezone.utc)
    if wtime > ftime:
        set_saved_data()

def get_freeway_winfo():
    """
    Extract information from a game window.

    Returns:
        hwnd -- The handle of the freeway window
        bounds -- The left, top, right, bottom bounds of the window
        img -- a PIL image grabbed from the screen
    """
    time.sleep(2)
    desktp = win32gui.GetDesktopWindow()
    dbbox = win32gui.GetWindowRect(desktp)
    hwnd = win32gui.FindWindow(None, "Freeways")
    if hwnd == 0:
        raise FreewayException("Freeways is not running")
    win32gui.SetForegroundWindow(hwnd)
    bounds = list(win32gui.GetWindowRect(hwnd))
    bounds[0] += 8
    bounds[1] += 32
    big_image = ImageGrab.grab()
    print("bounds", bounds)
    num1 = round(bounds[1] * big_image.size[1] / dbbox[3])
    num3 = round(bounds[3] * big_image.size[1] / dbbox[3])
    num0 = round(bounds[0] * big_image.size[0] / dbbox[2])
    num2 = round(bounds[2] * big_image.size[0] / dbbox[2])
    img = big_image.crop((num0, num1, num2, num3))
    return hwnd, bounds, img

BIG_MAP_PATTERN = ((0, 0, 380, 38), ((90, 124, 202), (118, 255, 92)))

def get_wef_colors(img):
    """
    Test to see if certain numbers of certain pixels are on the page.

    pat_desc tuple[0] -- information that describes a part of the
                            window that indicates something. Passed
    pat_desc tuple[1] -- tuple of tuples that lists rgb values of
                            pixels we expect to find
     @return distribution of pixels with these rgb values
    """
    pat_desc = BIG_MAP_PATTERN
    image_res = img.crop(pat_desc[0])
    wef_cols = [0] * len(pat_desc[1])
    for j in range(0, pat_desc[0][3] - pat_desc[0][1]):
        for i in range(0, pat_desc[0][2] - pat_desc[0][0]):
            for count, pixl in enumerate(pat_desc[1]):
                pval = image_res.getpixel((i,j))
                if (abs(pixl[0] - pval[0]) < 5 and
                        abs(pixl[1] - pval[1]) < 5 and
                        abs(pixl[2] - pval[2]) < 5):
                    wef_cols[count] += 1
    return wef_cols

def get_graycount(section, img):
    """
    Get number of gray characters in a section of the image. Used to find
    menu areas.

    @param section -- Area to scan (1/3 of possible menu locations)
    @param img -- image being scanned

    @return int number of specific shade of gray pixels found in section
    """
    psize = round(img.size[0] / 3)
    start_pt = section * psize
    end_pt = (section + 1) * psize
    reg = img.crop((start_pt, round(img.size[1] * .9),
        end_pt, img.size[1]))
    graycnt = 0
    for j in range(0, reg.size[1]):
        for i in range(0, reg.size[0]):
            if reg.getpixel((i, j)) == (160, 160, 160):
                graycnt += 1
    return graycnt

def load_layout():
    """
    Save layout innformation to json file.
    """
    with open(SAVED_INFO_FILE, 'r', encoding="utf8") as fload:
        return json.load(fload)

if __name__ == "__main__":
    check_saved_data()
