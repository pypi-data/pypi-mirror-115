"""Auto Mouse clickpy Script. Make it look like your still online with Python Automation."""

from random import randint
from time import sleep
from typing import Optional

import pyautogui
import typer

# Disable FailSafeException when mouse is in screen corners.
# I don't need a failsafe for this script.
pyautogui.FAILSAFE = False


def auto_click(
    fast_click: Optional[bool] = None, print_debug: Optional[bool] = None
) -> None:
    """Click function will pause current thread for a random intervaul, then click the mouse."""
    # get a time between 1 second and 3 minutes
    # to make clicks look a little more 'natural'
    sleep_time = 1 if fast_click else randint(1, 180)

    if print_debug and not fast_click:
        print(f"Random thread sleep for {sleep_time} seconds.")

    # pause the current thread
    sleep(sleep_time)

    # it's that easy to click a mouse with python :)
    pyautogui.click()

    if print_debug:
        print("Clicked")


def _main(
    debug: Optional[bool] = typer.Option(None, "--debug", "-d"),
    fast_click: Optional[bool] = typer.Option(None, "--fast-click", "-f"),
) -> None:
    """Auto Mouse clickpy Script. Make it look like your still online with Python Automation." """
    print("Running clickpy. Enter ctrl+c to stop.")

    if debug and fast_click:
        print(
            "fast_click flag passed in. Using thread.sleep(1), instead of a random interval."
        )

    while True:
        try:
            auto_click(fast_click=fast_click, print_debug=debug)
        except KeyboardInterrupt:
            msg = (
                "KeyboardInterrupt thrown and caught. Exiting script"
                if debug
                else "Back to work!"
            )
            print(f"\n{msg}")
            break


def run() -> None:
    """Common entry point. A wrapper around main function, that setups typer and executes main(...)."""
    typer.run(_main)


if __name__ == "__main__":
    run()  # pragma: no cover
