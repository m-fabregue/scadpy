from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    # Lazy: IPython (~0.6s) is heavy; used only as a type annotation here
    # (from __future__ import annotations makes all annotations strings at runtime).
    from IPython.core.display import HTML


def map_component_to_html_file[Component](
    component: Component, path: str, to_html: Callable[[Component], HTML]
) -> int:
    """
    Export a component to an HTML file.

    This function uses dependency injection for the HTML conversion, making it
    suitable for any component type that can be represented as HTML. The HTML
    is written to the specified file path.

    Parameters
    ----------
    component : Component
        The component to export.
    path : str
        The file path where the HTML will be written.
    to_html : Callable[[Component], HTML]
        Function that converts the component to an IPython HTML object.

    Returns
    -------
    int
        The number of characters written to the file.

    Examples
    --------
    >>> from IPython.core.display import HTML
    >>> from scadpy import map_component_to_html_file
    ...
    >>> map_component_to_html_file(
    ...     "Hello, World!",
    ...     "test.html",
    ...     to_html=lambda c: HTML(f"<h1>{c}</h1>")
    ... ) > 0 # doctest: +SKIP
    True
    """
    return open(path, "w", encoding="utf-8").write(cast(str, to_html(component).data))
