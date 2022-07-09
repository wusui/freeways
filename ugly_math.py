# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Math routines
"""
import math
import pyautogui

BIGNUM = 100000000000.0
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

def draw_arc(arc_info, fwy_info):
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
    fwy_info.butt_stat[0] = True
    cstep = 3
    if not arc_info["clockwise"]:
        cstep = -3
    print(indx, arc_info["arc_end"], cstep)
    for ival in range(indx, arc_info["arc_end"], cstep):
        pyautogui.moveTo(arc_info["origin"][0] +
                         arc_info["radius"] * math.cos(math.radians(ival)),
                         arc_info["origin"][1] +
                         arc_info["radius"] * math.sin(math.radians(ival)))

def get_equation(line_def):
    """
    Given a line segment that is defined by from and to points, return a line
    equation with a slope and y-intercept value
    """
    a_x = line_def['from'][0]
    a_y = line_def['from'][1]
    diffx = line_def['to'][0] - a_x
    diffy = line_def['to'][1] - a_y
    if diffx == 0:
        return {'slope': BIGNUM, 'yintercept': a_x}
    slope = diffy / diffx
    yintercept = a_y - slope * a_x
    print("equation", slope, yintercept)
    return {'slope': slope, 'yintercept': yintercept}

def get_perpendicular(equation, point):
    """
    Get the equation of the line perpendicular to the line equation passed
    in at the point passed in
    """
    if equation['slope'] == 0:
        return {'slope': BIGNUM, 'yintercept': point[0]}
    slope = -1 / equation['slope']
    yintercept = point[1] - point[0] * slope
    if abs(slope) < .0000000001:
        slope = 0
    return {'slope': slope, 'yintercept': yintercept}

def fixed_x(xval, equationy):
    """
    Find intersection of line with an x-coordinate (vertical line)
    """
    return [xval, xval * equationy['slope'] + equationy['yintercept']]

def get_intersection(equation1, equation2):
    """
    Find the point where two lines intersect
    """
    if equation1['slope'] == BIGNUM:
        return fixed_x(equation1['yintercept'], equation2)
    if equation2['slope'] == BIGNUM:
        return fixed_x(equation2['yintercept'], equation1)
    numerator = equation2['yintercept'] - equation1['yintercept']
    denominator = equation1['slope'] - equation2['slope']
    xval = numerator / denominator
    yval = equation1['slope'] * xval + equation1['yintercept']
    return [xval, yval]

def get_direction(this_line, other_line, fwy_info):
    """
    return x and y values of direction toward the inside of the curve
    (given as + or - 1 values)
    """
    retv = [-1, -1]
    mval = fwy_info.equation[this_line]['slope']
    bval = fwy_info.equation[this_line]['yintercept']
    if mval == BIGNUM:
        if fwy_info.line_table[other_line]['from'][0] < bval:
            return [-1, -1]
        return [1, 1]
    if mval == 0:
        tval = BIGNUM
    else:
        tval = (fwy_info.line_table[other_line]['to'][1] - bval) / mval
    if tval < fwy_info.line_table[other_line]['to'][0]:
        retv[0] = 1
    tval = fwy_info.line_table[other_line]['to'][0] * mval + bval
    if tval < fwy_info.line_table[other_line]['to'][1]:
        retv[1] = 1
    return retv

def get_parallel_line_offset(o_line, dirv, radius, fwy_info):
    """
    Get parallel line to find origin.
    """
    slope = fwy_info.equation[o_line]['slope']
    if slope == BIGNUM:
        x_offset = radius * dirv[0]
        yintercept = fwy_info.line_table[o_line]['to'][0] + x_offset
        return {'slope': slope, 'yintercept': yintercept}
    mval = fwy_info.equation[o_line]['slope']
    o_angle = math.acos(1 /  math.sqrt(mval * mval + 1))
    x_offset = math.cos(math.pi / 2 - o_angle) * dirv[0] * radius
    y_offset = math.sqrt(radius * radius - x_offset * x_offset) * dirv[1]
    print(x_offset, y_offset)
    x_offset = fwy_info.line_table[o_line]['from'][0] + x_offset
    y_offset = fwy_info.line_table[o_line]['from'][1] + y_offset
    yintercept = y_offset - slope * x_offset
    if slope == BIGNUM:
        yintercept = x_offset
    return {'slope': slope,  'yintercept': yintercept}

def get_radii_angle(slope, origin, fwy_info, parms, indx):
    """
    Get radius angle in degrees (0 is East).  Calculate the number of
    degrees from the last point the circle intersected an x or y axis
    """
    angle = 0
    if slope in (0, BIGNUM):
        return 0
    if origin[0] > fwy_info.line_table[parms[indx]]['to'][0]:
        angle = math.pi
    angle += math.atan(slope)
    if angle < 0:
        angle +=  math.pi / 2
    dangle = angle * 180 / math.pi
    dangle = int(dangle + .5)
    while dangle > 0:
        dangle -= 90
    return dangle + 90

def get_circle_pt_data(fwy_info, oline, dirv):
    """
    Find points on the circle for an arc
    """
    slopev = fwy_info.equation[oline]["slope"]
    if slopev == 0:
        if dirv[1] == 1:
            return 270
        return 90
    if slopev == BIGNUM:
        if dirv[1] == 1:
            return 180
        return 0
    quadrant = 0
    if slopev > 0:
        quadrant += 90
    if slopev * dirv[0] < 0:
        quadrant += 180
    return quadrant
