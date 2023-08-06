"""Definition of SupportsClick Protocol."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsClick(Protocol):  # pylint: disable=R0903
    """
    Definition of SupportsClick Protocol.

    Any object with a `click(self)` method can be considered a structural sub-type of SupportsClick.
    """

    def click(self) -> None:
        """
        Protocol method for the auto_click function.

        Any Clicking Strategy should implement a '__click__' method.
        """
