#!/usr/bin/env bash
# Zenith zed-kit installer. Idempotent; never overwrites existing config.
# Usage: zed-kit/install.sh [--dry-run] [--with-xdebug]
set -euo pipefail

kit="$(cd "$(dirname "$0")" && pwd)"
dry=0; xdebug=0
for a in "$@"; do
  case "$a" in
    --dry-run) dry=1 ;;
    --with-xdebug) xdebug=1 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done

run() { if [ $dry = 1 ]; then echo "  would run: $*"; else "$@"; fi; }
ok() { [ $dry = 1 ] && echo "dry  $*" || echo "ok   $*"; }
todo() { echo "TODO $*"; }

echo "== Requirements"
for t in php composer node npm; do
  command -v "$t" >/dev/null && ok "$t" || todo "$t missing (brew install $t)"
done

echo "== Formatter wrapper"
mkdir -p "$HOME/.local/bin"
target="$HOME/.local/bin/zed-php-fmt"
if [ "$(readlink "$target" 2>/dev/null)" = "$kit/bin/zed-php-fmt" ]; then ok "zed-php-fmt linked"
elif [ -e "$target" ]; then todo "$target exists and is not ours; left untouched"
else run ln -s "$kit/bin/zed-php-fmt" "$target"; ok "linked $target"; fi

echo "== Phpactor global config"
pa="$HOME/.config/phpactor/phpactor.json"
if [ -e "$pa" ]; then todo "$pa exists; merge $kit/phpactor/phpactor.json by hand"
else run mkdir -p "$(dirname "$pa")"; run cp "$kit/phpactor/phpactor.json" "$pa"; ok "installed $pa"; fi

echo "== PHPCS / WordPress standard"
if command -v phpcs >/dev/null && phpcs -i 2>/dev/null | grep -q WordPress; then ok "phpcs + WordPress"
else todo "composer global require wp-coding-standards/wpcs dealerdirect/phpcodesniffer-composer-installer"; fi

echo "== PATH"
for d in "$HOME/.local/bin" "$HOME/.composer/vendor/bin"; do
  case ":$PATH:" in *":$d:"*) ok "$d on PATH" ;; *) todo "add to ~/.zshrc: export PATH=\"$d:\$PATH\"" ;; esac
done

echo "== Xdebug"
if php -m 2>/dev/null | grep -qi xdebug; then ok "xdebug loaded"
elif [ $xdebug = 1 ]; then run pecl install xdebug
else todo "Xdebug not loaded (rerun with --with-xdebug, or use Herd/Valet's PHP)"; fi

echo "== Intelephense premium"
[ -f "$HOME/intelephense/licence.txt" ] && ok "licence found" || todo "optional: put licence key in ~/intelephense/licence.txt"

echo
echo "Next: merge $kit/settings.global.jsonc into ~/.config/zed/settings.json"
echo "      apply a project template: $kit/apply-template.sh <wordpress|laravel|node> <project-dir>"
