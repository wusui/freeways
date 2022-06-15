# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Compile a program (execute drawing operations)  Technically an interpreter...
"""
import os
import pyautogui
from utilities import draw_arc

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
        cmd_table = {
            'line': {'parm_cnt': 6,
                     'command': do_line},
            'move': {'parm_cnt': 3,
                     'command': do_move},
            'arc': {'parm_cnt': 7,
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
        for punct in [",", ";", "(", ")"]:
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

def do_line(parms, fwy_info):
    """
    Draw a new line
    """
    if parms[1] != "," or parms[4] !=  ",":
        print("Syntax error: Comma expected in line command")
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

def do_arc(parms, _):
    """
    Draw an arc between two points orthagonally on a circle
    """
    if parms[1] != "," or parms[4] !=  ",":
        print("Syntax error: Comma expected in arc command")
    print('TO DO -- MUST IMPLEMENT')
    print(parms)

def do_raw_arc(parms, fwy_info):
    """
    Draw an arc as specified by the () commands
    """
    offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    ioff = (0, 2, 1, 0, 3, 1, 2, 3)
    print(parms)
    arc_data = {}
    arc_data["clockwise"] = True
    indx1 = 0
    if parms[10] == "counterclockwise":
        arc_data["clockwise"] = False
        indx1 = 1
    arc_data["start"] = int(parms[6])
    arc_data["arc_end"] = int(parms[8])
    arc_data["radius"] = int(parms[0])
    indx1 += (arc_data["start"] // 45)
    factors = offsets[ioff[indx1]]
    arc_data["origin"] = (fwy_info.bounds[0] + int(parms[2])
                          + arc_data["radius"] * factors[0],
                          fwy_info.bounds[1] + int(parms[4])
                          + arc_data["radius"] * factors[1])
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

if __name__ == "__main__":
    TESTV = "clear line 68,421 1058,421;"
    TESTV += "line 1058,346 580,346 rbd move 570,346 rbu move 68,346;"
    TESTV += "line 534,86 534,180;"
    TESTV += "( 180, 534, 346, 0, 84, clockwise);"
    TESTV += "( 255, 534, 421, 180, 96, counterclockwise); stopwatch"
    # interpret(FreewayInfo())(TESTV)
    print("Done")
