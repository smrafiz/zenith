#!/usr/bin/env bash
# Self-check for zed-php-fmt. Run: zed-kit/bin/test-zed-php-fmt.sh
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
fmt="$here/zed-php-fmt"
fail=0
work="$(mktemp -d)"; trap 'rm -rf "$work"' EXIT
cd "$work"

check() { if [ "$1" = "$2" ]; then echo "ok   - $3"; else echo "FAIL - $3"; echo "  expected: $2"; echo "  got:      $1"; fail=1; fi; }

# 1. Fake tool in vendor/bin: proves stdin -> file -> stdout wiring and vendor/bin preference.
mkdir -p vendor/bin
printf '#!/usr/bin/env bash\nf="${@: -1}"; sed -i.bak "s/BAD/GOOD/" "$f"\n' > vendor/bin/pint && chmod +x vendor/bin/pint
out="$(printf '<?php echo "BAD";\n' | "$fmt" pint)"
check "$out" '<?php echo "GOOD";' "pint via vendor/bin rewrites buffer"

# 2. Unknown tool fails loudly.
printf '#!/bin/sh\n' > vendor/bin/foo && chmod +x vendor/bin/foo
printf 'x' | "$fmt" foo >/dev/null 2>&1; check "$?" "2" "unsupported tool exits 2"

# 3. Missing tool exits 127.
printf 'x' | PATH=/usr/bin:/bin "$fmt" php-cs-fixer >/dev/null 2>&1; check "$?" "127" "missing tool exits 127"

# 4. Real phpcbf with WordPress standard (skipped if not installed).
if command -v phpcbf >/dev/null && phpcbf -i 2>/dev/null | grep -q WordPress; then
  out="$(printf '<?php\nfunction a(){return 1;}\n' | "$fmt" phpcbf --standard=WordPress 2>/dev/null)"
  case "$out" in *"function a() {"*) check ok ok "phpcbf WordPress formats";; *) check "$out" "function a() {...}" "phpcbf WordPress formats";; esac
  out="$(printf '<?php\n$a = 1;\n' | "$fmt" phpcbf --standard=WordPress)"
  check "$out" $'<?php\n$a = 1;' "phpcbf clean input passes through (exit 0)"
else
  echo "skip - phpcbf with WordPress standard not on PATH"
fi

exit $fail
