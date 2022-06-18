# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Useful routines that are pretty much not dependent on other files.
"""
import math
import pyautogui

def num_to_location(map_no):
    """
    Convert a map number to a location on the world map grid.  Treat the
    world map like a 9x9 array.  Return the corresponding x, y coordinates

    @param map_no integer -- range is 0 to 80.  0 corresponds to the first
                             warm up map.
    @return (x,y) tuple map coordinate
    """
    if map_no > 80 or map_no < 0:
        return (-1, -1)
    if map_no == 0:
        return (4, 3)
    if map_no < 4:
        map_no -= 1
    diag = 1
    while diag * diag <= map_no:
        diag += 1
    diag -= 1
    if diag % 2 == 0:
        last_crn = 4 - diag // 2
    else:
        last_crn = 4 + diag // 2
    xtra = map_no - diag * diag
    if xtra < diag:
        xoff = 0
        yoff = xtra
    else:
        yoff = diag
        xoff = xtra - diag
    if diag % 2 == 0:
        xloc = last_crn + xoff
        yloc = last_crn + yoff
    else:
        xloc = last_crn - xoff + 1
        yloc = last_crn - yoff
    return (xloc, yloc)

def draw_arc(arc_info):
    """
    Draw a road as an arc of a circle based on the information in the
    arc_info dictionary.  Arc_info contains the following fields

    radius -- Radius of the circle in pixels
    origin -- X, Y coordinates of the origin of the circle
    clockwise -- True if we will draw clockwise, false if counterclockwise
    start -- starting point of the arc
    arc_end -- ending point of the arc

    The circle for the arc is measured in degrees.  0 is the east position,
    90 is the south position, 180 is the west position, and 270 is the north
    position.  Negative and greater than 360 degree values are allowed.
    """
    indx = arc_info["start"]
    pyautogui.moveTo(arc_info["origin"][0] +
                     arc_info["radius"] * math.cos(math.radians(indx)),
                     arc_info["origin"][1] +
                     arc_info["radius"] * math.sin(math.radians(indx)))
    pyautogui.mouseDown(button='left')
    cstep = 3
    if not arc_info["clockwise"]:
        cstep = -3
    for ival in range(indx, arc_info["arc_end"], cstep):
        pyautogui.moveTo(arc_info["origin"][0] +
                         arc_info["radius"] * math.cos(math.radians(ival)),
                         arc_info["origin"][1] +
                         arc_info["radius"] * math.sin(math.radians(ival)))
