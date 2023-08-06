"""Auto Mouse clickpy Script. Make it look like your still online with Python Automation."""
from .clickers import BasicRandomClickStrategy, SupportsClick


def auto_click(
    click_strategy: SupportsClick,
) -> None:
    """Redo this when you've decided on a stable(ish) api."""
    # TODO: Fix docstring when a stable api is defined
    if not click_strategy:
        click_strategy = BasicRandomClickStrategy()
    click_strategy.click()
