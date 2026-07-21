#!/usr/bin/env bash
set -euo pipefail

skill_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
extension_root="$skill_root/assets/extension"
dist_root="$skill_root/assets/extension-dist"

cd "$extension_root"
npm ci
npm test
npm run build
python3 "$skill_root/scripts/security_audit.py" "$extension_root"

mkdir -p "$dist_root"
rsync -a --delete "$extension_root/dist/" "$dist_root/"
echo "Built unpacked extension: $dist_root"
