import textwrap
import tomllib

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx_pyproject import SphinxConfig


class RenderExample(Directive):
    option_spec = {
        "name": directives.unchanged_required,
        "example": directives.unchanged_required,
        "ghost": directives.unchanged,
        "keep-color": directives.flag,
    }

    def run(self):
        name = self.options["name"]
        example_expr = self.options["example"]
        ghost_expr = self.options.get("ghost")

        if "keep-color" in self.options:
            light_expr = example_expr
            dark_expr = example_expr
        else:
            light_expr = f"({example_expr}).color(FOREGROUND_LIGHT)"
            dark_expr = f"({example_expr}).color(FOREGROUND_DARK)"

        if ghost_expr:
            light_expr = f"({light_expr} + ({ghost_expr}).color(GHOST_LIGHT))"
            dark_expr = f"({dark_expr} + ({ghost_expr}).color(GHOST_DARK))"

        rst = f"""\
        .. testcode::
           :hide:

           {light_expr}.to_html_file("build/d2__{name}__light.html", foreground_color=FOREGROUND_LIGHT, background_color=BACKGROUND_LIGHT)
           {dark_expr}.to_html_file("build/d2__{name}__dark.html", foreground_color=FOREGROUND_DARK, background_color=BACKGROUND_DARK)

        .. raw:: html

           <div class="render-example">

        .. include-html:: build/d2__{name}__light.html
           :class: only-light

        .. include-html:: build/d2__{name}__dark.html
           :class: only-dark

        .. raw:: html

           </div>
        """

        self.state_machine.insert_input(
            textwrap.dedent(rst).splitlines(), source="render-example"
        )
        return []


class EmptyHtml(Directive):
    required_arguments = 0

    def run(self):
        centered_html = """
        <div style="display: flex; justify-content: center;">
        </div>
        """
        return [nodes.raw("", centered_html, format="html")]


class IncludeHtml(Directive):
    required_arguments = 1
    option_spec = {"class": directives.unchanged}

    def run(self):
        file_path = self.arguments[0]
        css_class = self.options.get("class", "")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        except FileNotFoundError:
            return [nodes.raw("", "", format="html")]

        centered_html = f"""
        <div class="included-html {css_class}">
            <div>
                {html_content}
            </div>
        </div>
        """
        return [nodes.raw("", centered_html, format="html")]


def check_snapshots(app, exception):
    import hashlib
    import os
    import pathlib
    import re

    if exception or app.builder.name != "doctest":
        return

    update = os.environ.get("SCADPY_UPDATE_SNAPSHOTS") == "1"
    build_dir = pathlib.Path(app.srcdir) / "build"
    snapshot_dir = pathlib.Path(app.srcdir) / "snapshots"
    snapshot_dir.mkdir(exist_ok=True)

    errors = []
    for html_path in sorted(build_dir.glob("d2__*.html")):
        stem = html_path.stem
        snap_path = snapshot_dir / f"{stem}.md5"
        html_content = html_path.read_text(encoding="utf-8")
        normalized = re.sub(r"<dc:date>[^<]*</dc:date>", "", html_content)
        normalized = re.sub(r"\b[pm][0-9a-f]{8,}\b", "X", normalized)
        normalized = re.sub(r"\bscadpy-[0-9a-f]+\b", "X", normalized)
        normalized = re.sub(
            r"-?\d+\.\d+(?:[eE][+-]?\d+)?",
            lambda m: str(round(float(m.group()), 6)),
            normalized,
        )
        digest = hashlib.md5(normalized.encode()).hexdigest()
        if not snap_path.exists() or update:
            snap_path.write_text(digest)
        else:
            stored = snap_path.read_text().strip()
            if digest != stored:
                errors.append(
                    f"Snapshot mismatch: {stem} (stored={stored!r}, got={digest!r})"
                )

    if errors:
        raise RuntimeError("\n".join(errors))


def setup(app):
    app.add_directive("render-example", RenderExample)
    app.add_directive("include-html", IncludeHtml)
    app.add_directive("empty-html", EmptyHtml)
    app.connect("build-finished", check_snapshots)


SphinxConfig("../pyproject.toml", globalns=globals())

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "content-padding": "0 12px",
        "sidebar-width": "100px",
        "toc-width": "100px",
    },
}

html_logo = "_static/logo.png"
html_favicon = "_static/logo.ico"
html_static_path = ["_static"]
html_extra_path = ["build/AI_SKILLS.txt"]
html_css_files = [
    "css/custom.css",
]

_META_DESCRIPTION = (
    "ScadPy — parametric 2D/3D CAD modeling in pure Python. "
    "Fluent API, boolean operations, path extrusion, topology queries. "
    "Built on Shapely and trimesh. OpenSCAD alternative."
)
html_meta = {
    "description": _META_DESCRIPTION,
    "keywords": (
        "cad, parametric, 3d modeling, 2d geometry, openscad, python, "
        "boolean operations, shapely, trimesh, stl, extrude, solid, mesh"
    ),
    "og:title": "ScadPy — Parametric CAD in Pure Python",
    "og:description": _META_DESCRIPTION,
    "og:type": "website",
    "og:url": "https://m-fabregue.github.io/scadpy/",
    "og:image": "https://m-fabregue.github.io/scadpy/_static/logo.png",
    "twitter:card": "summary",
    "twitter:title": "ScadPy — Parametric CAD in Pure Python",
    "twitter:description": _META_DESCRIPTION,
}

with open("../pyproject.toml", "rb") as f:
    config = tomllib.load(f)

project = config["project"]["name"]
authors = config["project"]["authors"]
release = config["project"]["version"]

autodoc_typehints = "none"
autodoc_member_order = "bysource"
autosummary_generate = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

numpydoc_class_members_toctree = False
numpydoc_xref_param_type = True
numpydoc_xref_aliases = {
    "Shape": "scadpy.d2.shape.types.shape.Shape",
    "TopologyFilter": "scadpy.core.assembly.types.topology_filter.TopologyFilter",
}

doctest_global_setup = """
from scadpy import DEFAULT_OPACITY
LIGHT = [0.168, 0.168, 0.168, DEFAULT_OPACITY]
BACKGROUND_LIGHT = [0.949, 0.949, 0.949, DEFAULT_OPACITY]
FOREGROUND_LIGHT = [0.268, 0.268, 0.268, DEFAULT_OPACITY]
DARK = [0.972, 0.972, 0.949, DEFAULT_OPACITY]
BACKGROUND_DARK = [0.168, 0.168, 0.168, DEFAULT_OPACITY]
FOREGROUND_DARK = [0.972, 0.972, 0.949, DEFAULT_OPACITY]
GHOST_DARK = [1.0, 0.64, 0.2, 0.0]
GHOST_LIGHT = [0.85, 0.468, 0.0, 0.0]
"""

# Github light background: [1.0, 1.0, 1.0, DEFAULT_OPACITY]
# Github dark background: [0.051, 0.067, 0.090, DEFAULT_OPACITY]
# Furo light background: [0.949, 0.949, 0.949, DEFAULT_OPACITY]
# Furo dark background: [0.168, 0.168, 0.168, DEFAULT_OPACITY]
