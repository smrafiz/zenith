# Zenith engineers

Fifteen Claude Code subagents for building Zenith (the Zed fork, its language
servers and extensions, and zed-kit). Claude picks one from its `description`;
you can also name it ("use lead-engineer to plan 04").

## Setup (once)

1. **Install the hooks.** A Supercharger guard refused to let the agent that
   wrote these files create `.claude/hooks/`, so the scripts are staged in
   `.claude/hooks-pending/`. Read them, then move them:
   ```sh
   cd ~/GithubRepos/zenith && mkdir -p .claude/hooks && mv .claude/hooks-pending/* .claude/hooks/ && rmdir .claude/hooks-pending && chmod +x .claude/hooks/writer-gate.sh
   ```
   Until you do this, read-only agents can still run every Bash command and
   writer agents are not gated. Each hook reports a missing script as a
   non-blocking error and does nothing else.
2. **Trust the folder.** Hooks defined in a project agent's frontmatter run only
   after you accept the workspace trust dialog.
3. **Using them in the fork.** Project agents load from `.claude/agents/` between
   the working directory and the repo root. Sessions started in
   `~/GithubRepos/zed` won't see them. Pick one:
   - start sessions in `~/GithubRepos/zenith` (agents reach the fork by
     absolute path, `git -C ~/GithubRepos/zed …`), or
   - symlink into the fork and keep the links out of git:
     `ln -s ~/GithubRepos/zenith/.claude/agents ~/GithubRepos/zed/.claude/agents`
     (same for `hooks`), then add `.claude/agents` and `.claude/hooks` to
     `~/GithubRepos/zed/.git/info/exclude`. *Verify* that symlinked agent
     directories are discovered.
   `writer-gate.sh` checks both the project dir and the fork
   (`$ZENITH_FORK`, default `~/GithubRepos/zed`).

## Roster

| Agent | Role | Model | Read-only | Owns plan docs |
|---|---|---|---|---|
| `lead-engineer` | Architect: crate map, extension/LS-first call, upstream-hook budget, verifies *verify* APIs | opus | yes | 02, 15, 16 (A2/A3 decisions) |
| `orchestrator` | Routes a plan item or issue across engineers; gates | opus | yes (delegates via `Agent`) | README build order (routing only) |
| `code-reviewer` | Bugs + Zenith/Zed rules on a diff | opus | yes | — |
| `debugger` | Root cause of a red gate, with a probe | opus | yes | — |
| `security-engineer` | Localhost servers, process spawning, secrets, downloads | opus | yes | security sections of 06 08 11 12 22 |
| `performance-engineer` | Main-thread budget, Zenith vs stock Zed numbers | sonnet | yes | 18 A6 |
| `accessibility-engineer` | Keyboard, focus, AccessKit roles/labels in GPUI | sonnet | yes | a11y risks in 14 and every panel |
| `rust-core-engineer` | `zenith_core`, umbrella `zenith`, feature crates' non-UI logic | sonnet | no | 15, 17 A4, logic of 05 07 08 09 10 11 12 30 31 |
| `gpui-ui-engineer` | Panels, Items, title bar, stripes, status items | sonnet | no | 04 05 07 08 12 14 21 24 27 28 29 (UI) |
| `lsp-extension-engineer` | Standalone Rust LSes + Zed WASM extensions | sonnet | no | 16 A3, 19 (LS), 25 (LS), 26, 27 (LS) |
| `php-wordpress-laravel-engineer` | WP/Laravel/PHP domain rules, zed-kit, fixtures | sonnet | no | 03, 18 A7, domain of 19 20 21 25 26 31 |
| `agentic-integrations-engineer` | IDE/MCP server, ACP, Claude Code hooks, worktrees, review queue | sonnet | no | 06, 22, 23 |
| `release-ops-engineer` | Fork setup, upstream sync, build speed, bundle, CI, telemetry off | sonnet | no | 01, 13, 17 A5, 18 A8 |
| `test-engineer` | gpui/unit/integration/golden tests, release QA checklist | sonnet | no (tests only) | test sections; 13 QA checklist |
| `docs-editor` | Plan status, Implemented sections, README, CHANGELOG, CLAUDE.md | sonnet | no (Markdown only) | plan/README status, logs |

Read-only = `disallowedTools: Write, Edit, NotebookEdit` plus the
`read-only-bash.mjs` PreToolUse hook (only readers, `git` reads, `git -C <dir>`,
`cargo check/test/nextest/clippy/bench`, `script/clippy`, `bash -n`,
`shellcheck`, and `gh run|issue|pr|release list|view|diff`). Writers get
`guard-push.mjs` (pushes must be plain `git push` so a person approves) and the
`writer-gate.sh` Stop hook. The gate blocks a writer's report up to twice while
`cargo check/test` of each changed zenith crate, `bash -n` of changed scripts, or
the zed-kit self-check fails.

Models: opus for planning, review, debugging and security. Sonnet for
implementation. Performance and accessibility also run on sonnet, because they
measure and check against a checklist rather than make design calls. Raise
either to opus if their findings turn out shallow. No agent runs on haiku:
none of the work is purely mechanical.

## Routing guide

| Phase / situation | Start with | Then |
|---|---|---|
| Phase 0: 01 fork setup, 17 build | `release-ops-engineer` | `docs-editor` (build-log) |
| Phase 0: 02/15 `zenith_core` | `lead-engineer` | `rust-core-engineer` → `test-engineer` → `code-reviewer` + `performance-engineer` |
| Phase 0: 03 + 18 A7 (stock Zed) | `php-wordpress-laravel-engineer` | `code-reviewer` |
| Phase 1: 04 14 05 20 27 28 | `lead-engineer` | `rust-core-engineer` ∥ `gpui-ui-engineer` → `test-engineer` → `code-reviewer` + `accessibility-engineer` + `performance-engineer` |
| Phase 2: 06 23 22 | `lead-engineer` | `agentic-integrations-engineer` → `test-engineer` → `security-engineer` + `code-reviewer` |
| Phase 3: 19 25 26 (LS parts) | `lead-engineer` (LS vs fork split) | `php-wordpress-laravel-engineer` (rules, fixtures) ∥ `lsp-extension-engineer` → `gpui-ui-engineer` (panels) |
| Phase 3–5: 21 07 08 24 09 10 11 12 29 30 31 | `lead-engineer` | `rust-core-engineer` + `gpui-ui-engineer` (+ `security-engineer` for 08 11 12) |
| Weekly upstream merge (13) | `release-ops-engineer` | `debugger` for any zenith crate that broke → its owner |
| Upstream PR for a hook (16 A2) | `lead-engineer` | `rust-core-engineer` or `gpui-ui-engineer`. Zed PR rules: discuss first, one thing per PR, tests, title `crate: Imperative title` (no conventional prefix), `Release Notes:` section, CLA, human-written description |
| A gate is red | `debugger` | the owner it names |
| Feature done | `docs-editor` | — |
| Multi-specialism item, unplanned, run unattended | `orchestrator` | — |

One-file fixes need no agent. Already-planned chunks go straight to one
implementer; skip the orchestrator.

## Where each agent came from

| Agent | Source | What was kept / changed |
|---|---|---|
| lead-engineer | plinth | "plan, don't implement" and "state the decision first". Plinth's three-layer rule became crate boundaries, extension/LS-first and the upstream-hook budget |
| orchestrator | plinth | Team table, parallel dispatch, gate order, "verify, don't relay". Gates are now cargo/clippy, and it got a read-only hook |
| code-reviewer | plinth + radius-bundles | Radius's ≥ 80% confidence, MUST/SHOULD report block and twin-path idea, plus Zed `.rules` traps and the upstream-touch count |
| debugger | plinth + radius-bundles | Probe-before-claim, grep every caller, root-cause report block. Next.js and Shopify causes replaced with gpui/LS/merge causes |
| security-engineer | plinth + radius-bundles | Radius's threat-model table and confidence ≥ 8/10, rewritten for localhost servers, repo-controlled commands, keychain, downloads |
| performance-engineer | plinth | "A number without a method is not a finding" and the medians/cold-warm rules. Web Vitals and DB content replaced by plan 18's budgets |
| accessibility-engineer | plinth | Now read-only (the user's rule). Axe/WCAG web checks replaced with GPUI AccessKit (`_accessibility.rs`) and keyboard/action reachability |
| test-engineer | plinth test-engineer + qa-engineer, radius-bundles qa-engineer | "tests only, source bugs go back", "a test never seen failing is not a test", count before/after, plus plan 13's QA checklist |
| docs-editor | plinth docs-editor + radius-bundles doc-engineer/changelog-engineer | Minimal edits, evidence per claim, never invent, CHANGELOG traced to shas. Raised from haiku to sonnet because it verifies claims |
| release-ops-engineer | radius-bundles ops-engineer (+ changelog-engineer's no-unasked-tags rule) | "User runs the risky command", pinned actions and the report block, rewritten for fork sync/bundle/telemetry |
| rust-core-engineer | new (format from radius-bundles rust-functions-engineer) | "Rules the code won't show you", check list and report block |
| gpui-ui-engineer, lsp-extension-engineer, php-wordpress-laravel-engineer, agentic-integrations-engineer | new | — |

Hooks: `read-only-bash.mjs` and `guard-push.mjs` come from plinth.
`read-only-bash.mjs` swaps pnpm checks for cargo/script/clippy/gh and
`git -C`, and only lets the `RUST_LOG` / `RUST_BACKTRACE` / `CARGO_TERM_COLOR`
env prefixes through. `writer-gate.sh` comes from radius-bundles. It now runs
as a frontmatter `Stop` hook instead of the `PreToolUse(SubagentHandback)`
setting radius uses, with cargo/zed-kit checks in place of tsc/jest/Liquid.
*Verify* it fires in your sessions. If it doesn't, add radius's settings.json
matcher.

Dropped: plinth backend, frontend, builder, content, react-specialist,
design-engineer and seo-specialist. Radius-bundles backend, frontend,
storefront, graphql, shopify-integration, translation and the Shopify parts of
rust-functions. radius `verify.sh` (tsc+jest) has no Zenith equivalent beyond
the writer gate. Not copied: settings.local.json, handoffs, memory files.

Skills: only skills present in `~/.claude/skills` are preloaded:
`owasp-top-10` (security) and `technical-writing` (docs). Implementers get the
context7 MCP tools for library docs instead. Writers use `memory: project`
(`.claude/agent-memory/<agent>/`) to keep verified Zed API facts. Read-only
agents have no memory, because memory auto-enables Write/Edit.

## Open points

- **Commit prefix conflict.** `CLAUDE.md` says conventional commits (a hook
  rejects others). plan/02 and plan/16 say `zenith(<feature>): …` /
  `zenith(hook): …`, which a conventional-commit hook would reject. The agents
  use conventional commits with the crate as scope, e.g.
  `feat(zenith_scratches): …`. Settle it and have docs-editor fix the plans.
- Agents commit only when the caller asks and never push.
- The user-level `~/.claude/agents/debugger.md` shares a name with ours; the
  project one wins inside this repo.

## Research (checked 2026-11-15)

**Claude Code subagents**: [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)
- Confirmed frontmatter fields: `name`, `description` (required). Optional:
  `tools`, `disallowedTools`, `model` (`sonnet`/`opus`/`haiku`/`fable`/full id/
  `inherit`), `permissionMode` (`default`, `acceptEdits`, `auto`, `dontAsk`,
  `bypassPermissions`, `plan`), `maxTurns`, `autoCompactWindow`, `skills`
  (full content preloaded), `mcpServers`, `hooks`, `memory`
  (`user`/`project`/`local`), `background`, `omitClaudeMd`, `effort`
  (`low`…`max`, model-dependent), `isolation: worktree`, `color` (red, blue,
  green, yellow, purple, orange, pink, cyan), `initialPrompt`, `experimental`.
  Unknown fields are ignored silently (`claude --debug` reports them).
- `disallowedTools` is applied before `tools`; a specifier such as
  `Bash(git push *)` removes the whole tool, so command-level limits need a
  hook or a `permissions.deny` rule. That is why read-only agents use a hook.
- Frontmatter hooks support `PreToolUse`, `PostToolUse` and `Stop` (which runs
  as `SubagentStop`). They are ignored for plugin agents and need folder trust.
- `memory` auto-enables Read/Write/Edit and injects the first 200 lines / 25 KB
  of `MEMORY.md`.
- Delegation is driven by `description`. "Use proactively" encourages it. Keep
  descriptions short, because they all sit in context (warning above 15k
  tokens).
- The Task tool was renamed `Agent` (v2.1.63). Subagents may nest up to 3
  levels. Leaving `Agent` out of `tools` prevents nesting. Background subagents
  keep only a subset of built-in tools.
- Precedence: managed > `--agents` > project `.claude/agents/` > user > plugin.

**Hooks**: [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)
- PreToolUse input has `tool_input.command`. Exit 2 blocks, with stderr as the
  reason. Exit 2 from SubagentStop keeps the subagent working. Use
  `$CLAUDE_PROJECT_DIR` in quotes.

**Zed**
- Coding rules for agents: [zed `.rules`](https://raw.githubusercontent.com/zed-industries/zed/main/.rules).
  No `unwrap`, `?` / `.log_err()`, never `let _ =`. A dropped `Task` cancels.
  `cx.spawn` vs `cx.background_spawn`. `window` before `cx`; inner `cx` in
  `update`. `cx.notify()`. Keep `Subscription`s. `actions!` / `#[derive(Action)]`
  doc comments are user-visible. gpui tests use `background_executor().timer`.
  No `mod.rs`; `[lib] path`. Run `./script/clippy`, not `cargo clippy`. PR
  title `crate: Imperative`, `Release Notes:` section.
- Contribution policy: [CONTRIBUTING.md](https://raw.githubusercontent.com/zed-industries/zed/main/CONTRIBUTING.md).
  Discuss first, ≤ 3 open PRs, tests required, CLA. Autonomous agent PRs are not
  accepted, so a human must own upstream PRs.
- GPUI: [crates/gpui/README.md](https://raw.githubusercontent.com/zed-industries/zed/main/crates/gpui/README.md)
  (entities, `Render`, elements, actions, executors, `#[gpui::test]` /
  `TestAppContext`), and `crates/gpui/src/_accessibility.rs` (AccessKit:
  `.id()` + `.role()`, stable unique ids, `text!` id footgun, `on_a11y_action`).
- macOS build: [docs/src/development/macos.md](https://raw.githubusercontent.com/zed-industries/zed/main/docs/src/development/macos.md).
  Xcode + cmake, `cargo run`, `cargo test --workspace`, `cargo nextest` for
  "too many open files", `script/bundle-mac` (Xcode 26 SDK).
- Scripts in `script/` (GitHub API listing): `bootstrap`, `clippy` (adds
  `--workspace` unless `-p`; `--release --all-targets --all-features -D
  warnings`), `new-crate` (GPL-3.0-or-later default, AGPL refused,
  `[lib] path`), `bundle-mac`, `setup-sccache`, `check-licenses`,
  `check-todos`. The root `Cargo.toml` lists workspace `members` explicitly, so
  each new crate costs an upstream line.
- Extensions: [developing-extensions](https://zed.dev/docs/extensions/developing-extensions)
  (`extension.toml`, `cdylib`, `zed_extension_api`, `register_extension!`,
  target `wasm32-wasip2`, no `cfg` / `std::env::var`, `zed: install dev
  extension`), [languages](https://zed.dev/docs/extensions/languages)
  (`[language_servers.<id>]`, `languages`, `opt_in_languages`,
  `language_server_command`), and
  [mcp-extensions](https://zed.dev/docs/extensions/mcp-extensions)
  (`[context_servers.<id>]`, `context_server_command`; slated for deprecation
  in favour of the MCP registry). crates.io: `zed_extension_api` 0.7.0.
- ACP: [agentclientprotocol.com](https://agentclientprotocol.com/overview/introduction).
  JSON-RPC over stdio for local agents, reusing MCP JSON shapes. The fork pins
  `agent-client-protocol` in its workspace.

**Rust language servers**
- [tower-lsp-server](https://docs.rs/crate/tower-lsp-server/latest/source/README.md):
  community fork of tower-lsp, 0.23.0, `tower_lsp_server::ls_types`, Tokio
  default, `async fn` trait methods. Used by Oxc and Biome
  ([lemonadern notes](https://scrapbox.io/lemonadern/tower-lsp_%E3%81%A8_tower-lsp-server_%E3%81%AE%E9%96%A2%E4%BF%82)).
- [lsp-server](https://docs.rs/crate/lsp-server/latest): rust-analyzer's sync,
  crossbeam-based scaffold, 0.10.0.
- MCP in Rust: `rmcp` 3.10.0 on crates.io (2026-11).

Not verified (marked *verify* in agent bodies): the Claude Code IDE lockfile
protocol, Zed's `Panel` / `Item` trait shapes and the panel-registration call
site, the `db` migration macro name, the virtual list element names, the gpui
test keystroke helpers, `script/bundle-mac` flags and bundle-id handling,
extension publishing/licence rules, and discovery of symlinked agent
directories.
