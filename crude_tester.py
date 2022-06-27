# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Once the Freeways.exe file has been running and some freeway_input tests have
been run, the following can be run FROM THE LEVEL TO TEST in order to speed
up drawing turn around
"""
from freeway_input import FreewayInfo
from compiler import interpret

def crudetest(number):
    """
    Quick test

    @param number -- String representation of the solution file number.
    """
    fwy = FreewayInfo()
    with open(f"levels/solution{number}", 'r', encoding='utf8') as fdesc:
        data = fdesc.read()
    interpret(fwy)(data)

if __name__ == "__main__":
    crudetest("01")
