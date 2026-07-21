#!/usr/bin/env python3
import json
import pathlib
import re
import sys

REQUIRED_PERMISSIONS = {"activeTab", "scripting", "storage", "unlimitedStorage", "downloads"}
BANNED_SOURCE = {
    "chrome.storage.sync": r"chrome\.storage\.sync",
    "fetch": r"\bfetch\s*\(",
    "XMLHttpRequest": r"\bXMLHttpRequest\b",
    "WebSocket": r"\bWebSocket\b",
    "sendBeacon": r"\bsendBeacon\b",
    "Defuddle async extraction": r"\b(parseAsync|fetchAsyncVariables)\s*\(",
}


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parents[1] / "assets/extension").resolve()
    errors: list[str] = []
    manifest = json.loads((root / "manifest.json").read_text())
    if manifest.get("manifest_version") != 3:
        errors.append("manifest_version must be 3")
    permissions = set(manifest.get("permissions", []))
    if permissions != REQUIRED_PERMISSIONS:
        errors.append(f"permissions differ: {sorted(permissions)}")
    if manifest.get("host_permissions") != []:
        errors.append("host_permissions must be empty")
    csp = manifest.get("content_security_policy", {}).get("extension_pages", "")
    for required in ("script-src 'self'", "connect-src 'self'", "object-src 'none'", "frame-src 'none'"):
        if required not in csp:
            errors.append(f"CSP missing {required}")
    if "unsafe-eval" in csp or "unsafe-inline" in csp:
        errors.append("CSP contains an unsafe script allowance")

    source_root = root / "src"
    for path in source_root.rglob("*"):
        if path.suffix not in {".ts", ".tsx", ".js", ".jsx"}:
            continue
        text = path.read_text(errors="replace")
        for label, pattern in BANNED_SOURCE.items():
            if re.search(pattern, text):
                errors.append(f"{path.relative_to(root)} uses banned {label}")

    build_module = (root / "src/pack/build.ts").read_text()
    if "useAsync: false" not in build_module or ").parse()" not in build_module:
        errors.append("Defuddle must be configured for synchronous local parsing")

    if errors:
        print("SECURITY AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("SECURITY AUDIT PASSED")
    print(f"- permissions: {', '.join(sorted(REQUIRED_PERMISSIONS))}")
    print("- host permissions: none")
    print("- first-party network APIs: none")
    print("- Defuddle: synchronous local parse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
