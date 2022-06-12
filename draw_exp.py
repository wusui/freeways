"""
Tool used to demonstrate line location limits.
"""
import pyautogui
import freeway_input

def draw_points():
    """
    Draw lines on Freeways screen to determine how close lines can get without
    touching
    """
    fwy_info = freeway_input.FreewayInfo()
    fwy_info.clear_level()
    print(fwy_info.bounds)
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
    pyautogui.moveTo(x=fwy_info.bounds[0] + 300,
                     y=fwy_info.bounds[1] + 200)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 507,
                     y=fwy_info.bounds[1] + 200, duration=2)
    pyautogui.mouseUp(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 800,
                     y=fwy_info.bounds[1] + 200)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 568,
                     y=fwy_info.bounds[1] + 200, duration=2)
    pyautogui.mouseUp(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 534,
                     y=fwy_info.bounds[1] + 650)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 534,
                     y=fwy_info.bounds[1] + 379, duration=2)
    pyautogui.mouseUp(button='left')
    pyautogui.moveTo(x=fwy_info.bounds[0] + 20,
                     y=fwy_info.bounds[1] + 20)
    pyautogui.leftClick()
    print("Done")

if __name__ == "__main__":
    draw_points()
