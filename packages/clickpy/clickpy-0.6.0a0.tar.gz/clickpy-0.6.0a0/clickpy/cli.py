"""Contains all the cli specific methods for clickpy project."""

from typing import Optional

# mypy doesn't like pyautogui, and I can't find its py.types
import pyautogui  # type: ignore
import typer

from .clickers import BasicRandomClickStrategy, FastClickStrategy
from .clickpy import auto_click

# Disable FailSafeException when mouse is in screen corners.
# I don't need a failsafe for this script.
pyautogui.FAILSAFE = False


def _main(
    debug: Optional[bool] = typer.Option(None, "--debug", "-d"),
    fast_click: Optional[bool] = typer.Option(None, "--fast-click", "-f"),
) -> None:
    """Auto Mouse clickpy Script. Make it look like your still online with Python Automation."""
    print("Running clickpy. Enter ctrl+c to stop.")

    if debug and fast_click:
        print("fast_click flag passed in. Using thread.sleep(1), instead of a random interval.")

    click_strategy = (
        BasicRandomClickStrategy(print_debug=debug)
        if not fast_click
        else FastClickStrategy(print_debug=debug)
    )
    while True:
        try:
            auto_click(click_strategy)
        except KeyboardInterrupt:
            msg = (
                "KeyboardInterrupt thrown and caught. Exiting script" if debug else "Back to work!"
            )
            print(f"\n{msg}")
            break


def run() -> None:
    """
    CLI entry point.

    A wrapper around main function, that setups typer and executes main(...).
    """
    typer.run(_main)


if __name__ == "__main__":
    run()  # pragma: no cover
