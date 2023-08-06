"""Clicking Strategies Directory.

`clickers` was shorter than `clicking_strategies`, and other
abbreviations would have caused more confusion.
"""

from .basic_clicks import BasicRandomClickStrategy, FastClickStrategy
from .click_protocol import SupportsClick

__all__ = ["BasicRandomClickStrategy", "FastClickStrategy", "SupportsClick"]
# TODO: Need to test this directory
