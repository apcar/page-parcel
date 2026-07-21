#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
version="$(node -p "require('$root/assets/extension/package.json').version")"
out="$root/release"
archive="$out/PageParcel-$version.zip"

if [[ -n "${GITHUB_REF_NAME:-}" && "${GITHUB_REF_NAME#v}" != "$version" ]]; then
  echo "Release tag $GITHUB_REF_NAME does not match package version $version" >&2
  exit 1
fi

mkdir -p "$out"
rm -f "$archive" "$archive.sha256"

(
  cd "$root/assets/extension-dist"
  zip -qr "$archive" .
)

(
  cd "$out"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$(basename "$archive")" > "$(basename "$archive").sha256"
  else
    shasum -a 256 "$(basename "$archive")" > "$(basename "$archive").sha256"
  fi
)

echo "Packaged $archive"
