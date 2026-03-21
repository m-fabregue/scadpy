#!/usr/bin/env python3
"""Build AI_SKILLS.json from Python source files listed in pyproject.toml [tool.skills]."""

from __future__ import annotations

import ast
import json
import re
import tomllib
from pathlib import Path
from typing import Any

# Dunder → operator symbol
DUNDER_OPERATORS: dict[str, str] = {
    "__add__": "+",
    "__sub__": "-",
    "__or__": "|",
    "__and__": "&",
    "__xor__": "^",
    "__mul__": "*",
    "__truediv__": "/",
    "__floordiv__": "//",
    "__mod__": "%",
    "__pow__": "**",
    "__lshift__": "<<",
    "__rshift__": ">>",
    "__neg__": "-",
    "__pos__": "+",
    "__invert__": "~",
    "__eq__": "==",
    "__ne__": "!=",
    "__lt__": "<",
    "__le__": "<=",
    "__gt__": ">",
    "__ge__": ">=",
}


# ---------------------------------------------------------------------------
# Sphinx ref cleanup
# ---------------------------------------------------------------------------


def _strip_sphinx_refs(text: str) -> str:
    """Remove :func:`name`, :class:`name`, :meth:`name`, etc., keeping only `name`."""
    return re.sub(r":[a-z]+:`([^`]+)`", r"\1", text)


def _clean_description(text: str | None) -> str | None:
    if not text:
        return None
    # Remove "See funcname for parameter documentation." sentences
    text = re.sub(
        r"\s*See\s+\S+\s+for\s+(?:full\s+)?(?:parameter\s+)?documentation\.?",
        "",
        text,
        flags=re.IGNORECASE,
    )
    # Remove "Shortcut for funcname." sentences
    text = re.sub(r"\s*Shortcut for\s+\S+\.?", "", text, flags=re.IGNORECASE)
    text = _strip_sphinx_refs(text).strip()
    return text or None


# ---------------------------------------------------------------------------
# Annotation helpers
# ---------------------------------------------------------------------------


def _unparse_annotation(node: ast.expr | None) -> str | None:
    if node is None:
        return None
    raw = ast.unparse(node)
    # Strip quotes from string annotations (from __future__ import annotations)
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        return raw[1:-1]
    return raw


# ---------------------------------------------------------------------------
# NumPy docstring parsers
# ---------------------------------------------------------------------------


def _extract_description(docstring: str | None) -> str | None:
    if not docstring:
        return None
    lines = docstring.strip().splitlines()
    desc: list[str] = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^[A-Z][a-zA-Z ]+$", stripped) and stripped in (
            "Parameters",
            "Returns",
            "Examples",
            "Notes",
            "See Also",
            "Raises",
            "Attributes",
            "Methods",
            "Yields",
        ):
            break
        desc.append(stripped)
    while desc and not desc[-1]:
        desc.pop()
    return _clean_description(" ".join(l for l in desc if l)) or None


def _extract_numpy_params(docstring: str | None) -> dict[str, str]:
    """Return {param_name: description} from the Parameters section."""
    if not docstring:
        return {}
    m = re.search(
        r"Parameters\s*\n\s*-+\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z ]+\s*\n\s*-+|\Z)",
        docstring,
        re.DOTALL,
    )
    if not m:
        return {}

    result: dict[str, str] = {}
    current_name: str | None = None
    current_desc: list[str] = []

    for line in m.group(1).splitlines():
        # New param: "name : type" at the start of a line (not indented)
        if line and not line.startswith(" ") and not line.startswith("\t"):
            if current_name:
                result[current_name] = " ".join(current_desc).strip()
            # "name : type" or "name : type, default=x"
            param_match = re.match(r"^(\w+)\s*:", line)
            if param_match:
                current_name = param_match.group(1)
                current_desc = []
        elif current_name and line.strip():
            current_desc.append(line.strip())

    if current_name:
        result[current_name] = " ".join(current_desc).strip()

    return result


def _extract_examples(docstring: str | None) -> list[str]:
    if not docstring:
        return []
    m = re.search(
        r"Examples\s*\n\s*-+\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z ]+\s*\n\s*-+|\Z)",
        docstring,
        re.DOTALL,
    )
    if not m:
        return []

    # Group consecutive >>> / ... blocks, tracking setup lines
    examples: list[str] = []
    setup_lines: list[str] = []
    current_call: list[str] = []
    in_block = False

    for line in m.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith(">>> "):
            code = stripped[4:]
            if code.startswith(("from ", "import ", "#")):
                continue
            in_block = True
            current_call.append(code)
        elif stripped.startswith("... ") and in_block:
            current_call.append(stripped[4:])
        elif not stripped and in_block:
            # End of a block — decide if it's setup or a real example
            block = "\n".join(current_call)
            # Pure assignments with no method/function call → setup context
            if all(
                re.match(r"^\w+\s*=", l) and "(" not in l
                for l in current_call
                if l.strip()
            ):
                setup_lines = current_call[:]
            else:
                full = (
                    ("\n".join(setup_lines) + "\n" + block).strip()
                    if setup_lines
                    else block
                )
                examples.append(full)
                setup_lines = []
            current_call = []
            in_block = False

    if current_call:
        block = "\n".join(current_call)
        full = ("\n".join(setup_lines) + "\n" + block).strip() if setup_lines else block
        examples.append(full)

    cleaned: list[str] = []
    for ex in examples:
        ex = re.sub(r"\s*#\s*doctest:[^\n]*", "", ex).strip()
        if ex:
            cleaned.append(ex)

    return cleaned[:3]


# ---------------------------------------------------------------------------
# Project-wide function index (for param doc merging)
# ---------------------------------------------------------------------------


def _build_function_index(root: Path) -> dict[str, str]:
    """Scan all .py files (excluding .venv) and index {func_name: docstring}."""
    index: dict[str, str] = {}
    for py_file in root.rglob("*.py"):
        if ".venv" in py_file.parts:
            continue
        try:
            tree = ast.parse(py_file.read_text())
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                doc = ast.get_docstring(node)
                if doc and node.name not in index:
                    index[node.name] = doc
    return index


def _referenced_func(description: str | None) -> str | None:
    """Extract the first :func:`name` reference from a raw description."""
    if not description:
        return None
    m = re.search(r":func:`([^`]+)`", description)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# AST extraction
# ---------------------------------------------------------------------------


def _extract_params(func: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, Any]]:
    params: list[dict[str, Any]] = []
    args = func.args
    defaults_start = len(args.args) - len(args.defaults)

    for i, arg in enumerate(args.args):
        if arg.arg in ("self", "cls"):
            continue
        p: dict[str, Any] = {"name": arg.arg}
        if arg.annotation:
            p["type"] = _unparse_annotation(arg.annotation)
        di = i - defaults_start
        if di >= 0:
            p["default"] = ast.unparse(args.defaults[di])
        params.append(p)

    for i, arg in enumerate(args.kwonlyargs):
        p = {"name": arg.arg}
        if arg.annotation:
            p["type"] = _unparse_annotation(arg.annotation)
        kw_default = args.kw_defaults[i]
        if kw_default is not None:
            p["default"] = ast.unparse(kw_default)
        params.append(p)

    return params


def _build_signature(
    name: str, params: list[dict[str, Any]], returns: str | None, is_property: bool
) -> str:
    if is_property:
        sig = name
    else:
        parts = []
        for p in params:
            s = p["name"]
            if "type" in p:
                s += f": {p['type']}"
            if "default" in p:
                s += f" = {p['default']}"
            parts.append(s)
        sig = f"{name}({', '.join(parts)})"
    if returns:
        sig += f" -> {returns}"
    return sig


def _parse_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    func_index: dict[str, str],
    is_method: bool = False,
) -> dict[str, Any]:
    decorator_names = [
        (
            d.id
            if isinstance(d, ast.Name)
            else d.attr
            if isinstance(d, ast.Attribute)
            else ""
        )
        for d in node.decorator_list
    ]
    is_property = "cached_property" in decorator_names or "property" in decorator_names
    is_classmethod = "classmethod" in decorator_names

    if is_property:
        kind = "property"
    elif is_classmethod:
        kind = "classmethod"
    else:
        kind = "method" if is_method else "function"

    raw_docstring = ast.get_docstring(node)
    returns = _unparse_annotation(node.returns)
    params = [] if is_property else _extract_params(node)

    # Merge param descriptions from referenced standalone function
    ref_func = _referenced_func(raw_docstring)
    if ref_func and ref_func in func_index:
        param_descs = _extract_numpy_params(func_index[ref_func])
        for p in params:
            if p["name"] in param_descs and param_descs[p["name"]]:
                p["description"] = param_descs[p["name"]]

    entry: dict[str, Any] = {
        "kind": kind,
        "signature": _build_signature(node.name, params, returns, is_property),
        "description": _extract_description(raw_docstring),
        "examples": _extract_examples(raw_docstring),
    }
    if params:
        entry["params"] = params
    if returns:
        entry["returns"] = returns
    if node.name in DUNDER_OPERATORS:
        entry["operator"] = DUNDER_OPERATORS[node.name]

    return entry


def _parse_class(node: ast.ClassDef, func_index: dict[str, str]) -> dict[str, Any]:
    methods: dict[str, dict[str, Any]] = {}
    for item in ast.iter_child_nodes(node):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods[item.name] = _parse_function(item, func_index, is_method=True)

    return {
        "kind": "class",
        "description": _extract_description(ast.get_docstring(node)),
        "methods": methods,
    }


def parse_file(path: Path, func_index: dict[str, str]) -> dict[str, Any]:
    tree = ast.parse(path.read_text())
    result: dict[str, Any] = {}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            result[node.name] = _parse_class(node, func_index)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name] = _parse_function(node, func_index)
    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    root = Path(__file__).parent.parent.parent

    with open(root / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)

    cfg = config.get("tool", {}).get("skills", {})
    output_path = root / cfg.get("output", "AI_SKILLS.json")
    sources: list[str] = cfg.get("sources", [])

    print("Indexing project functions for param merging…")
    func_index = _build_function_index(root)
    print(f"  {len(func_index)} functions indexed")

    skills: dict[str, Any] = {}
    for src in sources:
        p = root / src
        if p.is_dir():
            py_files = sorted(p.rglob("*.py"))
        elif p.is_file():
            py_files = [p]
        else:
            print(f"  WARNING: {src} not found, skipping")
            continue
        for py_file in py_files:
            if py_file.name == "__init__.py":
                continue
            skills.update(parse_file(py_file, func_index))

    output_path.write_text(json.dumps(skills, indent=2))
    total = sum(
        len(v.get("methods", {})) if v.get("kind") == "class" else 1
        for v in skills.values()
    )
    print(
        f"Generated {output_path.name} — {len(skills)} classes/functions, {total} entries total"
    )


if __name__ == "__main__":
    main()
