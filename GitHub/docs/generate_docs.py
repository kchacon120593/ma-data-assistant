from __future__ import annotations
import inspect
import pkgutil
from pathlib import Path
import importlib
import re

def _clean(s: str) -> str:
    return re.sub(r'\n{3,}', '\n\n', s).strip()

def generate_module_docs(package: str, out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pkg = importlib.import_module(package)
    pkg_path = Path(pkg.__file__).parent

    modules = []
    for m in pkgutil.walk_packages([str(pkg_path)], prefix=package + "."):
        if m.ispkg:
            continue
        modules.append(m.name)

    index_lines = [f"# Documentation for `{package}`\n"]
    for mod_name in sorted(modules):
        mod = importlib.import_module(mod_name)
        md_name = mod_name.replace(".", "_") + ".md"
        index_lines.append(f"- {md_name}")

        lines = [f"# `{mod_name}`\n"]
        mod_doc = inspect.getdoc(mod) or ""
        if mod_doc:
            lines.append(_clean(mod_doc) + "\n")

        funcs = []
        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if obj.__module__ != mod_name:
                continue
            funcs.append((name, obj))

        if funcs:
            lines.append("## Functions\n")
            for name, fn in funcs:
                doc = inspect.getdoc(fn) or ""
                sig = str(inspect.signature(fn))
                lines.append(f"### `{name}{sig}`\n")
                lines.append(_clean(doc) + "\n" if doc else "_No docstring._\n")

        Path(out_dir / md_name).write_text("\n".join(lines), encoding="utf-8")

    Path(out_dir / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    generate_module_docs("ma_migration", Path(__file__).parent / "generated")
