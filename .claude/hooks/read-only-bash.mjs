// PreToolUse(Bash) for Zenith's read-only agents (lead, orchestrator, reviewer,
// debugger, security, performance, accessibility): every command in a chain must
// be a reader or a check, and nothing may write through a redirect. Adapted from
// plinth/.claude/hooks/read-only-bash.mjs. Exit 2 blocks the call.
import { readFileSync } from "node:fs";

const command = String(JSON.parse(readFileSync(0, "utf8"))?.tool_input?.command ?? "");

// `git -C ../zed diff` reads the fork from the plan repo.
const GIT = String.raw`^git( -C \S+)? `;

const READERS = [
    new RegExp(GIT + String.raw`(status|diff|log|show|blame|grep|ls-files|rev-parse|merge-base|reflog show|worktree list|remote -v|branch( --list| -a| -v| --show-current)?)(\s|$)`),
    /^(cat|head|tail|wc|ls|find|grep|rg|sort|uniq|cut|tr|awk|jq|diff|stat|file|pwd|echo|printf|basename|dirname|realpath|tree|column|nl|comm|du|df|ps|true)(\s|$)/,
    /^sed -n(\s|$)/,
    /^cd(\s|$)/,
    // Checks. They write only build output under target/.
    /^cargo (check|test|nextest run|clippy|bench|tree|metadata|doc --no-deps)(\s|$)/,
    /^(\.\/)?script\/clippy(\s|$)/,
    /^(rustc|rustup|cargo) (--version|-V|show)(\s|$)/,
    /^(bash|sh) -n(\s|$)/,
    /^(shellcheck|php -l|node --check)(\s|$)/,
    /^(\.\/)?zed-kit\/bin\/test-zed-php-fmt\.sh$/,
    /^gh (run|issue|pr|release) (list|view|diff)(\s|$)/,
    /^(curl -s|curl -sS|curl -fsS|curl -s -o \/dev\/null)(\s|$)/,
    /^lsof(\s|$)/,
];

// Only these env prefixes; `RUSTC_WRAPPER=x cargo …` would run any binary.
const stripEnv = (part) => part.replace(/^((RUST_LOG|RUST_BACKTRACE|CARGO_TERM_COLOR)=\S*\s+)+/, "");

// Output redirects write files; `2>&1` and `>/dev/null` do not.
const writes = /(^|[^0-9&])>{1,2}(?!\s*(\/dev\/null|&1))/.test(command.replace(/2>&1|&>\/dev\/null|>\s*\/dev\/null/g, ""));
const parts = command.split(/&&|\|\||;|\||\n/).map((part) => stripEnv(part.trim())).filter(Boolean);
const refused = parts.filter((part) => !READERS.some((reader) => reader.test(part)));

// Readers that can still act: find's -delete/-exec, awk's system(), a curl
// that sends a body or another method.
const acts = /\bfind\b[^|;&]*\s-(delete|exec|execdir|ok|fprint)\b|\bsystem\s*\(|\bcurl\b[^|;&]*\s(-d|--data\S*|-X|--request|-T|--upload-file|-F|--form)\b/.test(command);

if (writes || acts || refused.length > 0 || /[`]|\$\(/.test(command)) {
    process.stderr.write(
        `Refused: this Zenith agent is read-only. Allowed: git status/diff/log/show (optionally git -C <dir>), readers (cat, grep, rg, sed -n, head…), and checks (cargo check/test/nextest/clippy/bench, script/clippy, bash -n, shellcheck, gh run/issue/pr view). ${refused.length ? `Not allowed: ${refused.join(" · ")}` : "No redirects or substitutions."}\n`,
    );
    process.exit(2);
}
