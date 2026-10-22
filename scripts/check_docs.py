"""Check that relative Markdown links and images resolve to tracked files."""

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    missing = []
    for document in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "reports"} for part in document.parts):
            continue
        for target in LINK.findall(document.read_text(encoding="utf-8")):
            target = target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            if not (document.parent / unquote(target)).exists():
                missing.append(f"{document.relative_to(ROOT)}: {target}")
    for link in missing:
        print(link)
    print(f"Relative Markdown links: {'FAIL' if missing else 'OK'}")
    return bool(missing)


if __name__ == "__main__":
    raise SystemExit(main())
