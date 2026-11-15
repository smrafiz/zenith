# 06 — Zed as IDE/MCP Server for External Agents

## Goal

Let external CLI agents (Claude Code, Codex, Gemini CLI) *drive Zed* the way Claude Code drives PhpStorm/WebStorm today via their MCP servers: read open files, selection, diagnostics, symbols; open files; show diffs for approval.

Note: Zed already *hosts* agents (Agent Panel, ACP). This feature is the reverse direction — Zed *serves* context to agents running in a terminal.

## Parity checklist (vs JetBrains MCP server / Claude Code IDE integration)

- [ ] Current file + selection + open tabs (must)
- [ ] Diagnostics for file/project (must)
- [ ] Open file at line (must)
- [ ] Show proposed edit as diff, user accepts/rejects in Zed (must)
- [ ] Find symbol / references / definition via LSP (must)
- [ ] Run task / run configuration (later)
- [ ] Search in project (later; agents usually grep)
- [ ] Execute terminal command in Zed terminal (later)
- [ ] Local history query (after 05) (later)

## Two protocol targets

1. **Generic MCP server** (streamable HTTP or SSE on localhost) — any MCP client (`claude mcp add zed http://127.0.0.1:<port>/mcp`).
2. **Claude Code IDE integration**: Claude Code discovers IDEs through lockfiles in `~/.claude/ide/` and connects over a local WebSocket speaking MCP; provides `openDiff`, `getDiagnostics`, selection notifications (*verify current protocol from Claude Code source/docs and existing VS Code/JetBrains extension behaviour before building*).

Build 1 first; add 2 as an adapter over the same tool implementations.

## Architecture

- Crate `zenith_ide_server`: starts on workspace open, binds `127.0.0.1` random port, auth token in lockfile/env (never listen on 0.0.0.0).
- MCP tools implemented as async fns with access to `Workspace`/`Project` entities via a handle on the main thread (`cx.spawn` + `update`).
- Rust MCP: use the `rmcp` crate if already in Zed's dependency tree or acceptable; otherwise minimal JSON-RPC (Zed has `context_server` client code to reuse types — *verify*).
- Diff approval: open a diff `Item` (reuse agent-panel diff review UI if reusable) — result returned to the tool call (accept/reject + final text).
- One server per window; lockfile includes workspace folders so the agent picks the right window.

## Tools

| Tool | Returns |
|---|---|
| `get_active_editor` | path, language, selection ranges, selected text |
| `get_open_files` | list |
| `get_diagnostics(path?)` | LSP diagnostics |
| `open_file(path, line?)` | ok |
| `open_diff(path, new_content)` | accepted/rejected + content |
| `find_definition/references(path, line, col)` | locations |
| `workspace_symbols(query)` | symbols |
| `run_task(label)` | exit code + output tail |

## Settings

```json
"zenith": { "ide_server": { "enabled": true, "port": 0, "claude_code_lockfile": true } }
```

## Security

- Localhost only, per-session random token, lockfile mode 0600.
- `run_task` / terminal tools off by default (setting).
- Log every tool call to an "IDE Server" log view.

## Milestones

1. Server skeleton + `get_active_editor`, `get_open_files`, `open_file`.
2. Diagnostics + LSP navigation tools.
3. `open_diff` with approval UI.
4. Claude Code lockfile adapter; test with `claude` in Zed terminal → `/ide`.
5. Optional tools behind settings.

## Tests

- Tool unit tests against `FakeFs` project.
- Integration: spawn server, call via MCP client test harness.

## Risks

- Claude Code IDE protocol undocumented/changing — keep adapter thin.
- Main-thread access from server threads — all workspace access via gpui async context.

## Effort

2–3 weeks.
