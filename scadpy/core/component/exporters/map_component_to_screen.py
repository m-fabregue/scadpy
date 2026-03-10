from __future__ import annotations

import sys
import tempfile
from collections.abc import Callable

from IPython.core.display import HTML
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from typeguard import typechecked


@typechecked
def map_component_to_screen[Component](
    component: Component, to_html: Callable[[Component], HTML]
):
    """
    Render a component as HTML and display it in a Qt-based window.

    Parameters
    ----------
    component : Component
        The component to export and display.
    to_html : Callable[[Component], HTML]
        Function that converts the component to an IPython HTML object.

    Examples
    --------
    >>> from IPython.core.display import HTML
    >>> from scadpy import map_component_to_screen

    >>> component = "Hello, World!"
    >>> map_component_to_screen(
    ...     component,
    ...     to_html=lambda c: HTML(f"<h1>{c}</h1>")
    ... )  # doctest: +SKIP
    """

    html = str(to_html(component).data)

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8")
    tmp.write(html)
    tmp.close()

    view = QWebEngineView()
    view.settings().setAttribute(
        QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
    )
    view.load(QUrl.fromLocalFile(tmp.name))
    view.setWindowTitle("ScadPy")
    view.resize(800, 800)
    view.show()

    view.raise_()
    view.activateWindow()

    sys.exit(app.exec())
