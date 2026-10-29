# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Sadhu Shobab Bollipo
"""Check local Markdown file links. No network requests; anchors not checked."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def check(root):
    errors=[]
    root=Path(root).resolve()
    for doc in root.rglob("*.md"):
        if any(p in (".git","node_modules",".venv","__pycache__") for p in doc.parts):
            continue
        content=re.sub(r"```.*?```","",doc.read_text(encoding="utf-8"),flags=re.S)
        for raw in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)",content):
            target=raw.strip().split()[0].strip("<>")
            parsed=urlsplit(target)
            if parsed.scheme or target.startswith(("#","//")):
                continue
            filename=unquote(parsed.path)
            destination=root/filename.lstrip("/") if filename.startswith("/") else doc.parent/filename
            if filename and not destination.exists():
                errors.append(f"{doc.relative_to(root)}: missing {filename}")
    return errors


if __name__=="__main__":
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent
    failures=check(root)
    print("\n".join(failures) if failures else "Local Markdown file links passed (external URLs and anchors not checked).")
    raise SystemExit(bool(failures))
