# Visual check — 2026-11-19

Installed `Zenith Dev` (fork `feat/look` @ `1e536b0b39`) on `easy-demo-importer`, compared with the `Main` and `ToolWindows` mockups. Only the main window was checked: keys quit the app (see Blockers), so no tool window could be opened.

## Blockers

- Any keypress quits the app (clean exit, code 0, no panic in `~/Library/Logs/Zenith/Zenith.log`). Under investigation.

## Main window vs mockup

| Area | Mockup | Installed app |
|---|---|---|
| Title bar, left | App logo, project badge + name dropdown, branch dropdown | No logo; `ED easy-demo-importer`, `main / chore/...` (repo + branch) |
| Search Everywhere | Wide centred pill with `⇧⇧` hint | Small plain text, right of centre, no hint |
| Agents pill | `1 running · review 2` with count badge | `Agents` button only (no live state) |
| Right stripe | Agents (with dot), Database, HTTP Client | One icon only |
| Breadcrumbs | `project › folder › file › class › method` | File name only; Zed's search/action icons at right |
| Inline diagnostics | One compact pill under the line | Red end-of-line text on every line; very noisy |
| Hook gutter icons | Hook glyph beside `add_action` / `add_filter` | None |
| Status bar, left | `⚠ 1`, `Claude Code waiting for review` | Error count, `Failed to run iremote, phpactor` |
| Status bar, right | `PHP 8.5 · docker`, LS name (`Intelephense`), pos, UTF-8, LF, indent | Pos, LF, PHP, UTF-8, indent, PHP 8.5 — no LS name, no runtime |
| Project tree | `External Libraries` node at the bottom | Missing |
| Parameter hints | Small grey pills | Present, larger |
| Inline git blame | Not shown | Shown on the cursor line |

Matches: left stripe layout (3 top / 4 bottom), project panel header with `…` and `×`, coloured folder icons, tab style, run config + run/debug buttons, settings gear, minimap.

## Not the UI, but visible

- `Function 'add_action' not found` (and every WordPress function): no WordPress stubs for the PHP language server.
- `phpactor` fails to start (`Class "Amp\Failure" not found` from its phar); `iRemote` extension 404s on its release download.

## Not checked

- Tool windows (TODO, Commit, Local History, WordPress, Agents, Database, HTTP, Tests, Scratches) and Search Everywhere: need working keys.
