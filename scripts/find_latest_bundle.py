#!/usr/bin/env python3
import pathlib


def main() -> int:
    candidates = []
    for directory in (pathlib.Path.home() / "Downloads", pathlib.Path.home() / "Desktop"):
        if directory.exists():
            candidates.extend(directory.glob("PageParcel-*.zip"))
    if not candidates:
        print("No PageParcel Trace Bundle ZIP found in Downloads or Desktop.")
        return 1
    print(max(candidates, key=lambda path: path.stat().st_mtime))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
