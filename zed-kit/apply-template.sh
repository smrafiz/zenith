#!/usr/bin/env bash
# Copy a zed-kit project template into a project. Never overwrites existing files.
# Usage: zed-kit/apply-template.sh <wordpress|laravel|node> <project-dir>
set -euo pipefail

kit="$(cd "$(dirname "$0")" && pwd)"
type="${1:?usage: apply-template.sh <wordpress|laravel|node> <project-dir>}"
dest="${2:?usage: apply-template.sh <wordpress|laravel|node> <project-dir>}"
src="$kit/templates/$type"
[ -d "$src" ] || { echo "unknown template: $type (have: $(ls "$kit/templates" | tr '\n' ' '))" >&2; exit 2; }
[ -d "$dest" ] || { echo "not a directory: $dest" >&2; exit 2; }

cd "$src"
find . -type f | sed 's#^\./##' | while read -r f; do
  if [ -e "$dest/$f" ]; then echo "skip $f (exists)"
  else mkdir -p "$dest/$(dirname "$f")"; cp "$f" "$dest/$f"; echo "add  $f"; fi
done
[ "$type" = wordpress ] && echo "note: set text_domain and prefixes in phpcs.xml.dist"
exit 0
