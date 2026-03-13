#!/usr/bin/env python3
"""Jedi-based code intelligence queries for Claude."""
import sys
import json
import jedi

def find_references(file_path, line, col):
    script = jedi.Script(path=file_path)
    refs = script.get_references(line, col)
    return [{"file": str(r.module_path), "line": r.line, "col": r.column, "name": r.name} for r in refs]

def goto_definition(file_path, line, col):
    script = jedi.Script(path=file_path)
    defs = script.goto(line, col)
    return [{"file": str(d.module_path), "line": d.line, "col": d.column, "name": d.name} for d in defs]

def find_usages_of_name(project_path, name):
    project = jedi.Project(project_path)
    results = []
    import os
    for root, _, files in os.walk(project_path):
        for f in files:
            if f.endswith(".py") and ".venv" not in root:
                path = os.path.join(root, f)
                try:
                    script = jedi.Script(path=path, project=project)
                    with open(path) as fh:
                        lines = fh.readlines()
                    for i, line in enumerate(lines, 1):
                        if name in line:
                            col = line.index(name)
                            refs = script.get_references(i, col)
                            for r in refs:
                                if r.name == name:
                                    results.append({"file": path, "line": i, "col": col})
                                    break
                except Exception:
                    pass
    return results

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "refs":
        print(json.dumps(find_references(sys.argv[2], int(sys.argv[3]), int(sys.argv[4])), indent=2))
    elif cmd == "goto":
        print(json.dumps(goto_definition(sys.argv[2], int(sys.argv[3]), int(sys.argv[4])), indent=2))
    elif cmd == "usages":
        print(json.dumps(find_usages_of_name(sys.argv[2], sys.argv[3]), indent=2))
