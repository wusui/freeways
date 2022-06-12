"""
Manual solution for level 1
"""
import pyautogui
import freeway_input

def draw_level1():
    """
    Draw level 1 solution
    """
    fwy_info = freeway_input.FreewayInfo()
    fwy_info.clear_level()
    print(fwy_info.bounds)
    pyautogui.moveTo(x=fwy_info.bounds[0] + 68,
                     y=fwy_info.bounds[1] + 421)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 1058,
                     y=fwy_info.bounds[1] + 421, duration=2)
    pyautogui.mouseUp(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 1058,
                     y=fwy_info.bounds[1] + 346)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 68,
                     y=fwy_info.bounds[1] + 346, duration=2)
    pyautogui.mouseUp(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 534,
                     y=fwy_info.bounds[1] + 86)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 534,
                     y=fwy_info.bounds[1] + 324, duration=2)
    pyautogui.mouseUp(button='left')
    fwy_info.ramp_up()
    fwy_info.ramp_down()
    pyautogui.mouseDown(button='left')
    pyautogui.move(1, 1)
    pyautogui.mouseUp(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 534,
                     y=fwy_info.bounds[1] + 246)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 434,
                     y=fwy_info.bounds[1] + 346, duration=2)
    pyautogui.mouseUp(button='left')
    fwy_info.stopwatch()
    print("Done")

if __name__ == "__main__":
    draw_level1()
