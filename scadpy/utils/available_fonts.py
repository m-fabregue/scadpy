from __future__ import annotations

from matplotlib import font_manager as fm


def available_fonts() -> list[str]:
    """Return a sorted list of font family names available on the system.

    Only TrueType (.ttf) and OpenType (.otf) fonts are included.
    Fonts that cannot be parsed are silently ignored.

    The default font used by :func:`~scadpy.d2.shape.primitives.text.text`
    (DejaVu Sans) is always available regardless of what this function returns,
    as it is bundled with matplotlib.

    Returns
    -------
    list[str]
        Sorted list of font family names.

    Examples
    --------
    >>> from scadpy import available_fonts
    >>> fonts = available_fonts()
    >>> isinstance(fonts, list)
    True
    >>> all(isinstance(f, str) for f in fonts)
    True
    """
    names: set[str] = set()
    for path in fm.findSystemFonts():  # type: ignore[reportUnknownMemberType]
        if not path.lower().endswith((".ttf", ".otf")):
            continue
        try:
            name = fm.FontProperties(fname=path).get_name()
            if name:
                names.add(name)
        except Exception:
            continue
    return sorted(names)
