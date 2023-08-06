"""Auto Mouse clickpy Script. Make it look like your still online with Python Automation."""

from random import randint
from time import sleep
from typing import Optional

import pyautogui


def auto_click(
    sleep_time: Optional[int] = None, print_debug: Optional[bool] = None
) -> None:
    """Click function will pause current thread for a random intervaul, then click the mouse."""
    # get a time between 1 second and 3 minutes
    # to make clicks look a little more 'natural'
    timer = sleep_time if sleep_time else randint(1, 180)

    if print_debug:
        print(f"Random thread sleep for {timer} seconds.")

    # pause the current thread
    sleep(timer)

    # it's that easy to click a mouse with python :)
    pyautogui.click()

    if print_debug:
        print("Clicked")
