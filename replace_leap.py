"""Replace the word LEAP with Leap in .pptx, .docx and .md files.

Usage:
    python replace_leap.py [ROOT] [--apply]

Without --apply it does a dry run and only reports what would change.
Matching is case-sensitive and whole-word (LEAPS or LEAPING are left alone).
Office files must be closed in PowerPoint/Word before running with --apply.
"""
import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

OLD, NEW = "LEAP", "Leap"
WORD_RE = re.compile(rf"\b{OLD}\b")
# Only touch text between tags, never tag names/attributes.
XML_TEXT_RE = re.compile(r">([^<]*)<")
OFFICE_EXTS = {".pptx", ".docx"}
# XML parts that hold visible text (slides, notes, layouts, document body, headers, comments...)
OFFICE_PART_RE = re.compile(r"^(ppt|word)/.*\.xml$")


def replace_in_xml(xml: str) -> tuple[str, int]:
    count = 0

    def sub_text(m):
        nonlocal count
        new, n = WORD_RE.subn(NEW, m.group(1))
        count += n
        return f">{new}<"

    return XML_TEXT_RE.sub(sub_text, xml), count


def process_office(path: Path, apply: bool) -> int:
    total = 0
    tmp = path.with_suffix(path.suffix + ".tmp")
    with zipfile.ZipFile(path) as zin:
        items = []
        for info in zin.infolist():
            data = zin.read(info.filename)
            if OFFICE_PART_RE.match(info.filename):
                text = data.decode("utf-8")
                new_text, n = replace_in_xml(text)
                if n:
                    total += n
                    data = new_text.encode("utf-8")
            items.append((info, data))
    if apply and total:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for info, data in items:
                zout.writestr(info, data)
        shutil.move(tmp, path)
    return total


def process_md(path: Path, apply: bool) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, n = WORD_RE.subn(NEW, text)
    if apply and n:
        path.write_text(new_text, encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".", help="folder to scan (default: current)")
    ap.add_argument("--apply", action="store_true", help="actually write changes")
    args = ap.parse_args()

    root = Path(args.root)
    files_changed = grand_total = 0
    for path in sorted(root.rglob("*")):
        ext = path.suffix.lower()
        if not path.is_file() or path.name.startswith("~$"):
            continue  # skip Office lock files
        try:
            if ext in OFFICE_EXTS:
                n = process_office(path, args.apply)
            elif ext == ".md":
                n = process_md(path, args.apply)
            else:
                continue
        except Exception as e:
            print(f"ERROR  {path}: {e}", file=sys.stderr)
            continue
        if n:
            files_changed += 1
            grand_total += n
            print(f"{n:5d}  {path}")

    mode = "Replaced" if args.apply else "Would replace"
    print(f"\n{mode} {grand_total} occurrence(s) in {files_changed} file(s).")
    if not args.apply and grand_total:
        print("Run again with --apply to make the changes.")


if __name__ == "__main__":
    main()
