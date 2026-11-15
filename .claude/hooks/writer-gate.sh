#!/usr/bin/env bash
# Stop gate for Zenith's writer agents (frontmatter `Stop`, which runs as
# SubagentStop): the agent may not report back while what it changed fails its
# checks. Exit 2 sends the agent back to work with the failure on stderr.
# Adapted from radius-bundles/.claude/hooks/writer-gate.sh.
# shortcut: it checks the whole dirty tree, so another session's broken files
# also block; the agent reports those under Issues instead of fixing them.
set -u

input=$(cat)
# Two blocks per agent run, then the report goes through so a stuck agent can
# still say what is broken.
id=$(printf "%s" "$input" | jq -r '.agent_id // "x"' 2>/dev/null || echo x)
blocks_file="${TMPDIR:-/tmp}/zenith-writer-gate-$id.blocks"
blocks=$(cat "$blocks_file" 2>/dev/null || echo 0)
[ "$blocks" -ge 2 ] && exit 0

fork="${ZENITH_FORK:-$HOME/GithubRepos/zed}"
fail=""
log=$(mktemp)

check_repo() {
    local root=$1
    git -C "$root" rev-parse --git-dir >/dev/null 2>&1 || return 0
    local changed
    changed=$(git -C "$root" status --porcelain --untracked-files=all | awk '{print $NF}')
    [ -z "$changed" ] && return 0

    # Shell scripts parse.
    for f in $(printf '%s\n' "$changed" | grep -E '(\.sh$|(^|/)bin/[^/.]+$)' || true); do
        [ -f "$root/$f" ] || continue
        head -1 "$root/$f" | grep -qE '^#!.*(ba)?sh' || continue
        bash -n "$root/$f" 2>"$log" || fail+=$'\n## bash -n failed: '"$root/$f"$'\n'"$(head -5 "$log")"
    done

    # zed-kit formatter wrapper keeps its self-check green.
    if printf '%s\n' "$changed" | grep -qE '^zed-kit/bin/'; then
        "$root/zed-kit/bin/test-zed-php-fmt.sh" >"$log" 2>&1 || fail+=$'\n## zed-kit/bin/test-zed-php-fmt.sh failed\n'"$(grep -E 'FAIL|expected|got' "$log" | head -20)"
    fi

    if [ -d "$root/crates/zed" ]; then
        # The fork: check and test only the zenith crates that changed.
        local crates args=""
        crates=$(printf '%s\n' "$changed" | sed -nE 's#^crates/(zenith[a-z0-9_]*)/.*#\1#p' | sort -u)
        for c in $crates; do args+=" -p $c"; done
        if [ -n "$args" ]; then
            # shellcheck disable=SC2086
            (cd "$root" && cargo check --quiet $args) >"$log" 2>&1 || fail+=$'\n## cargo check'"$args"$' failed\n'"$(grep -E '^(error|warning: unused)' -A4 "$log" | head -40)"
            # shellcheck disable=SC2086
            [ -z "$fail" ] && { (cd "$root" && cargo test --quiet $args) >"$log" 2>&1 || fail+=$'\n## cargo test'"$args"$' failed\n'"$(tail -30 "$log")"; }
        fi
    elif [ -f "$root/Cargo.toml" ] && printf '%s\n' "$changed" | grep -qE '(\.rs$|Cargo\.(toml|lock)$)'; then
        # A standalone language server repo (wp-hooks-ls, …).
        (cd "$root" && cargo test --quiet) >"$log" 2>&1 || fail+=$'\n## cargo test failed in '"$root"$'\n'"$(tail -30 "$log")"
    fi
}

check_repo "${CLAUDE_PROJECT_DIR:-$PWD}"
[ "$(cd "$fork" 2>/dev/null && pwd -P)" != "$(cd "${CLAUDE_PROJECT_DIR:-$PWD}" && pwd -P)" ] && check_repo "$fork"

rm -f "$log"
if [ -n "$fail" ]; then
    printf 'Checks failed on the uncommitted tree. Fix what you changed and send your report again; if a failure is in a file you did not touch, report it under Issues instead.%s\n' "$fail" >&2
    echo $((blocks + 1)) > "$blocks_file"
    exit 2
fi
exit 0
