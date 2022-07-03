# Steam Freeway Game Drawing Tool
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Once the Freeways.exe file has been running and freeway_setup has
been run, the following can be run FROM THE LEVEL TO TEST in order to speed
up drawing turn around
"""
import sys
from freeway_setup import FreewayInfo
from compiler import find_solution

if __name__ == "__main__":
    DEFAULT = "1"
    if len(sys.argv) > 1:
        DEFAULT = sys.argv[1]
    find_solution(int(DEFAULT),  FreewayInfo())
