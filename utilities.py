# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Useful routines that are pretty not dependent on other files.
"""

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
