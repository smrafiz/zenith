// PreToolUse(Bash) for Zenith's writer agents: a push only in its plain form, so
// a permission rule (or a person) sees it. Refuses `git -C . push`, `git 'push'`,
// a push in a chain or a subshell, `sh -c "git push"`, and defining an alias to
// one. Copied from plinth/.claude/hooks/guard-push.mjs. The words in a commit
// message are not a push. Exit 2 blocks the call.
import { readFileSync } from "node:fs";

// The body of a quoted heredoc (`<<'EOF'`, `<<"EOF"`) is data — the shell
// expands nothing in it — so a push written there as text is not a push.
const command = String(JSON.parse(readFileSync(0, "utf8"))?.tool_input?.command ?? "").replace(
    /<<-?\s*(['"])(\w+)\1[^\n]*\n[\s\S]*?\n\s*\2(?=\n|$)/g,
    "",
);

/// Words of one simple command, quotes removed (enough for this check).
const words = (segment) => [...segment.matchAll(/'([^']*)'|"((?:[^"\\]|\\.)*)"|(\S+)/g)].map((m) => m[1] ?? m[2] ?? m[3]);

/// git's global options that take a value: `git -C dir push` is a push.
const TAKES_VALUE = new Set(["-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"]);

function subcommandOf(tokens) {
    for (let i = 1; i < tokens.length; i++) {
        if (TAKES_VALUE.has(tokens[i])) i++;
        else if (!tokens[i].startsWith("-")) return tokens[i];
    }

    return undefined;
}

function pushesIn(text) {
    return text.split(/&&|\|\||;|\||\n/).some((segment) => {
        const tokens = words(segment.trim().replace(/^(\w+=\S*\s+)+/, ""));
        const [program = ""] = tokens;

        if (/(^|\/)git$/.test(program)) {
            const sub = subcommandOf(tokens);

            // `git config alias.p push` defines a push under another name.
            return sub === "push" || (sub === "config" && tokens.some((t) => /(^|\s|!)git push\b|^push$/.test(t)));
        }

        // A shell handed a string runs it: look inside.
        if (/(^|\/)(sh|bash|zsh|eval|xargs|env)$/.test(program)) return tokens.slice(1).some((t) => /\bgit\b/.test(t) && pushesIn(t));

        return false;
    });
}

const substitutions = [...command.matchAll(/\$\(([^)]*)\)|`([^`]*)`/g)].map((m) => m[1] ?? m[2]);
const pushes = pushesIn(command) || substitutions.some(pushesIn);
const plain = /^\s*git push(\s|$)/.test(command) && !/[;&|`\n]|\$\(/.test(command);

if (pushes && !plain) {
    process.stderr.write(
        "Refused: a git push must be a plain `git push …` command on its own, so a person approves it. Zenith agents never push (plan repo, fork or LS repos) — report and let the owner decide.\n",
    );
    process.exit(2);
}
