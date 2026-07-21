#!/usr/bin/env python3
import argparse
import hashlib
import json
import pathlib
import tempfile
import zipfile


def verify(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if any(name.startswith("/") or ".." in pathlib.PurePosixPath(name).parts for name in names):
            errors.append("ZIP contains an unsafe path")
        required = {"page.md", "page-reader.md", "page.json"}
        missing = required - set(names)
        if missing:
            errors.append(f"missing required files: {sorted(missing)}")
            return errors
        pngs = sorted(name for name in names if name.endswith(".png"))
        if not pngs:
            errors.append("no PNG screenshot found")
        try:
            manifest = json.loads(archive.read("page.json"))
        except Exception as exc:
            errors.append(f"invalid page.json: {exc}")
            return errors
        if manifest.get("schema_version") != "1.0":
            errors.append("unsupported schema_version")
        if not manifest.get("security", {}).get("local_only"):
            errors.append("local_only security marker is absent")
        listed = {item.get("name"): item for item in manifest.get("artifacts", [])}
        for name in ["page.md", "page-reader.md", *pngs]:
            if name not in listed:
                errors.append(f"artifact not registered: {name}")
                continue
            data = archive.read(name)
            digest = hashlib.sha256(data).hexdigest()
            if listed[name].get("sha256") != digest:
                errors.append(f"hash mismatch: {name}")
            if listed[name].get("bytes") != len(data):
                errors.append(f"byte count mismatch: {name}")
        for name in pngs:
            if not archive.read(name).startswith(b"\x89PNG\r\n\x1a\n"):
                errors.append(f"invalid PNG signature: {name}")
        if not archive.read("page.md").strip() or not archive.read("page-reader.md").strip():
            errors.append("Markdown artifact is empty")
        if any(name.lower().endswith((".html", ".htm")) for name in names):
            errors.append("raw HTML must not be included")
    return errors


def self_test() -> pathlib.Path:
    temp = pathlib.Path(tempfile.mkdtemp()) / "PageParcel-self-test.zip"
    png = b"\x89PNG\r\n\x1a\nself-test"
    page = b"# Self test\n"
    artifacts = []
    for name, data in (("page.md", page), ("page-reader.md", page), ("page.png", png)):
        artifacts.append({"name": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    manifest = {"schema_version": "1.0", "security": {"local_only": True}, "artifacts": artifacts}
    with zipfile.ZipFile(temp, "w") as archive:
        archive.writestr("page.md", page)
        archive.writestr("page-reader.md", page)
        archive.writestr("page.png", png)
        archive.writestr("page.json", json.dumps(manifest))
    return temp


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a PageParcel Trace Bundle ZIP.")
    parser.add_argument("path", nargs="?", type=pathlib.Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    path = self_test() if args.self_test else args.path
    if path is None:
        parser.error("provide a ZIP path or --self-test")
    errors = verify(path.expanduser().resolve())
    if errors:
        print("TRACE BUNDLE INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"TRACE BUNDLE VERIFIED: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
