from __future__ import annotations

import threading
import webbrowser
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Lazy: IPython (~0.6s) is heavy; used only as a type annotation here
    # (from __future__ import annotations makes all annotations strings at runtime).
    from IPython.core.display import HTML


def map_component_to_screen[Component](
    component: Component, to_html: Callable[[Component], HTML]
):
    """
    Render a component as HTML and display it in the system browser.

    Starts a one-shot local HTTP server on a random available port, opens the
    browser, and shuts the server down as soon as the page has been served.

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
    inner = str(to_html(component).data)
    html_bytes = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; background: #ffffff; }}
  #scadpy-content {{ width: min(100vw, 100vh); height: min(100vw, 100vh); }}
  #scadpy-content svg {{ width: 100%; height: 100%; }}
</style>
</head>
<body><div id="scadpy-content">{inner}</div></body>
</html>""".encode("utf-8")
    served = threading.Event()

    class _OneShot(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)
            served.set()

        def log_message(self, format: str, *args: object) -> None:
            pass  # suppress request logs

    server = HTTPServer(("127.0.0.1", 0), _OneShot)
    port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    webbrowser.open(f"http://127.0.0.1:{port}")

    served.wait()
    server.shutdown()
