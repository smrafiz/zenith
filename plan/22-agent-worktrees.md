# 22 — Agent Worktree Manager (F4)

## Goal

Run several coding agents (Claude Code, Codex, Gemini CLI, Zed Agent) in parallel, each isolated in its own git worktree, and manage them from one panel: status, diff, test, merge, discard.

First: audit upstream Zed — it may already have parallel agent threads/worktree support; build only the gaps.

## Parity checklist (no JetBrains equivalent — Zenith differentiator)

- [ ] New agent task: prompt + agent type + base branch → creates worktree `../<repo>.wt/<slug>` on branch `agent/<slug>` (must)
- [ ] Start agent in that worktree (terminal session for CLI agents; ACP thread for ACP agents) (must)
- [ ] Panel: list tasks with status (running / waiting for input / done / failed), elapsed, changed files count (must)
- [ ] Notify when an agent waits for input or finishes (must)
- [ ] Review: open diff vs base (multibuffer), run tests/inspections in that worktree (07/21) (must)
- [ ] Merge: squash-merge or rebase into base branch; or open PR (`gh pr create`) (must)
- [ ] Discard: remove worktree + branch (with confirmation) (must)
- [ ] Copy env/setup: `.env`, `vendor`/`node_modules` strategy (symlink / copy / run install) per project (must)
- [ ] Port isolation for dev servers (later)
- [ ] Cost/token display if agent exposes it (later)

## UX

- Right-stripe panel "Agents": `+ New Task`, list rows (status dot, title, agent, branch, Δ files), row actions: Open (switch Zed window to worktree or open as additional worktree), Terminal, Diff, Test, Merge, Discard.
- Task detail: prompt, log tail, changed files.

## Architecture

- Crate `zenith_agents`.
- Git ops via `git` CLI through `zenith_core::process` (`git worktree add -b`, `git worktree remove`, `git merge --squash`).
- Setup hooks: project `.zed/zenith-agents.json`:
  ```json
  { "setup": ["cp ../main/.env .env", "composer install --no-interaction", "npm ci"],
    "share": ["vendor"], "base_branch": "main" }
  ```
- Agent launch:
  - CLI agents: Zed terminal in worktree cwd running configured command (`claude "<prompt>"`, `codex "<prompt>"`).
  - ACP agents: open agent thread with project root = worktree (*verify* ACP thread per-worktree support).
- Status detection: CLI → process alive + idle-output heuristic + agent hooks (Claude Code `Stop`/`Notification` hooks can POST to Zenith IDE server (06) → precise status).
- State persisted in `zenith_core::store`.

## Safety

- Discard/merge always confirm; show uncommitted changes count.
- Never auto-merge; never force-push.
- Worktrees outside the main repo dir but next to it; path shown in UI.

## Milestones

1. Upstream audit.
2. Create/list/discard worktrees + setup hooks.
3. Launch CLI agents in terminal; status via process.
4. Claude Code hooks → precise status + notifications.
5. Review diff + tests + merge/PR.
6. ACP agents.

## Tests

Temp repo integration tests for create/merge/discard; setup-hook runner tests.

## Effort

2–3 weeks.
