# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Compile a program (execute drawing operations)  Technically an interpreter...
"""
import os
import pyautogui
from ugly_math import draw_arc, get_equation, get_perpendicular
from ugly_math import get_direction, get_parallel_line_offset
from ugly_math import get_intersection, get_radii_angle, get_circle_pt_data
#from ugly_math import get_radii_angle, get_arc_info

def find_solution(level, fwy_info):
    """
    Read a solution from a levels file and redraw the level

    @param integer level -- level number
    @param FreewayInfo fwy_info

    After reading the levels data, the instructions on that file are
    executed.
    """
    fname = os.sep.join(["levels", f"solution{level:02d}"])
    with open(fname, 'r', encoding="utf8") as finfo:
        prog_data = finfo.read()
    interpret(fwy_info)(prog_data)

def interpret(fwy_info):
    """
    Curry fwy_info
    """
    def fcompile(oprogram):
        """
        Execute the line drawing operations specified by the program entered

        @param oprogram string -- text of program being interpreted
        """
        fwy_info.line_table = {}
        fwy_info.equation = {}
        cmd_table = {
            'defline': {'parm_cnt': 7,
                        'command': defline},
            'line': {'parm_cnt': 7,
                     'command': do_line},
            'move': {'parm_cnt': 3,
                     'command': do_move},
            'arc': {'parm_cnt': 3,
                    'command': do_arc},
            '(': {'parm_cnt': 12,
                  'command': do_raw_arc}
        }
        short_cmd_table = {
            'clear': do_clear,
            'stopwatch': do_stopwatch,
            'rbd': do_rbutdown,
            'rbu': do_rbutup,
            ';': do_endcmd
        }
        program = ""
        for pline in oprogram.split('\n'):
            if pline.strip().startswith("#"):
                continue
            program += "\n" + pline
        mod_prog = program
        for punct in [",", ";", "(", ")", "$"]:
            sp_punct = f' {punct} '
            mod_prog = mod_prog.replace(punct, sp_punct)
        tokens = mod_prog.split()
        stack = []
        stack_cnt = 0
        orig_cmd = ''
        for word in tokens:
            if stack_cnt > 0:
                stack.append(word)
                stack_cnt -= 1
                if stack_cnt == 0:
                    cmd_table[orig_cmd]['command'](stack, fwy_info)
                continue
            if word in cmd_table:
                orig_cmd = word
                stack = []
                stack_cnt = cmd_table[word]['parm_cnt']
            else:
                short_cmd_table[word](fwy_info)

    return fcompile

def defline(parms, fwy_info):
    """
    Define a line from two points and a label.
    """
    if parms[1] != "," or parms[4] !=  ",":
        print("Syntax error: Comma expected in line command")
    badname = True
    if parms[6] >= 'A' and parms[6] <= 'Z':
        badname = False
    if parms[6] == '$':
        return
    if badname:
        print("Illegal line name")
    fwy_info.line_table[parms[6]] = {'from': [int(parms[0]), int(parms[2])],
                                     'to': [int(parms[3]), int(parms[5])]}
    fwy_info.equation[parms[6]] = get_equation(fwy_info.line_table[parms[6]])

def do_line(parms, fwy_info):
    """
    Handle line command and actually draw a line
    """
    defline(parms, fwy_info)
    pyautogui.moveTo(x=fwy_info.bounds[0] + int(parms[0]),
                     y=fwy_info.bounds[1] + int(parms[2]))
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + int(parms[3]),
                     y=fwy_info.bounds[1] + int(parms[5]), duration=1)

def do_move(parms, fwy_info):
    """
    Move the mouse to a new point
    """
    if parms[1] != ",":
        print("Syntax error: Comma expected in move command")
    pyautogui.moveTo(x=fwy_info.bounds[0] + int(parms[0]),
                     y=fwy_info.bounds[1] + int(parms[2]), duration=1)

def do_arc(parms, fwy_info):
    """
    Draw an arc between two points orthogonally on a circle
    """
    for indx in range(0, 2):
        if parms[indx] not in fwy_info.line_table:
            print(f"parameter {parms[indx]} missing")
            return
    eq_a = get_perpendicular(fwy_info.equation[parms[0]],
                                fwy_info.line_table[parms[0]]['to'])
    eq_b = get_perpendicular(fwy_info.equation[parms[1]],
                                fwy_info.line_table[parms[1]]['from'])
    dir_a = get_direction(parms[0], parms[1], fwy_info)
    dir_b = get_direction(parms[1], parms[0], fwy_info)
    print(dir_a, dir_b, eq_a, eq_b)
    radius = int(parms[2])
    peq_a = get_parallel_line_offset(parms[0], dir_a, radius, fwy_info)
    peq_b = get_parallel_line_offset(parms[1], dir_b, radius, fwy_info)
    origin = get_intersection(peq_a, peq_b)
    print("DEBUG:", origin, radius, eq_a, eq_b)
    degrees_a = get_radii_angle(eq_a["slope"], origin, fwy_info, parms, 0)
    degrees_b = get_radii_angle(eq_b["slope"], origin, fwy_info, parms, 1)
    arc_data = {}
    arc_data["radius"] = radius
    #arc_data["origin"] = origin
    #arc_data["start"] =  0
    #arc_data["arc_end"] =  359
    adata = get_circle_pt_data(fwy_info, parms[0], dir_a)
    arc_data["start"] = adata + degrees_a
    adata = get_circle_pt_data(fwy_info, parms[1], dir_b)
    arc_data["arc_end"] = adata + degrees_b
    origin = [int(origin[0] + .5) + fwy_info.bounds[0],
              int(origin[1] + .5) + fwy_info.bounds[1]]
    arc_data["origin"] = origin
    if abs(arc_data["start"] - arc_data["arc_end"]) > 180:
        if arc_data["start"] > 270:
            if arc_data["arc_end"] < arc_data["start"]:
                arc_data["arc_end"] += 360
        if arc_data["start"] < 90:
            if arc_data["arc_end"] > arc_data["start"]:
                arc_data["arc_end"] -= 360
    arc_data["clockwise"] = False
    if arc_data["start"] < arc_data["arc_end"]:
        arc_data["clockwise"] = True
    draw_arc(arc_data)
    print("do_arc_info", origin, parms, arc_data)

def do_raw_arc(parms, fwy_info):
    """
    Draw an arc as specified by the () commands
    """
    arc_data = {}
    arc_data["clockwise"] = True
    if parms[10] == "counterclockwise":
        arc_data["clockwise"] = False
    arc_data["start"] = int(parms[6])
    arc_data["arc_end"] = int(parms[8])
    arc_data["radius"] = int(parms[0])
    arc_data["origin"] = (fwy_info.bounds[0] + int(parms[2]),
                          fwy_info.bounds[1] + int(parms[4]))
    draw_arc(arc_data)
    pyautogui.mouseUp(button='left')

def do_clear(fwy_info):
    """
    Start over
    """
    fwy_info.clear_level()

def do_stopwatch(fwy_info):
    """
    Check out the score of a completed level
    """
    fwy_info.stopwatch()

def do_rbutdown(_):
    """
    Handle arbd command (right button down)
    """
    pyautogui.mouseDown(button='right')

def do_rbutup(_):
    """
    Perform rbu command (right button up)
    """
    pyautogui.mouseUp(button='right')

def do_endcmd(_):
    """
    Handle a semi-colon
    """
    pyautogui.mouseUp(button='left')
