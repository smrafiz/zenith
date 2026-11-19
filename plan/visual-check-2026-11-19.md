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

## Fixes made (code only, not built or installed yet)

Fork `feat/look`:
- `792dfb4795` Search Everywhere crash: every ⇧⇧/⌘O/⌘E/⌘⇧E shortcut quit the app (panel `icon()` read the workspace mid-update). Regression test added.
- `34293c3f6f`, `7d94af7f01` Main board values: search box 340×28, radius 7, `#31343a`, ⇧⇧ key cap; 20 px `#4a5b8c` project badge; 26 px pill agent chip; rails 40 px wide, 28 px buttons, no border, window background; islands 5 px gap, 10 px radius; Driftwood `text.muted #b4b7be`, active line number `#8c93a1`, gutter `#282c34`.

Owner kept font sizes 16 / 17 / 1.8 (board: 13 / 13.5 / 24 px).

Next build: `workspace` changed ⇒ full ~2.5 h release rebuild. Build only when the owner asks.

## Still different (not done)

- Rail buttons 28 px (board 30 px): `IconButton` has no 30 px size.
- Project panel: 36 px header, 24 px rows, selected row radius 6 with 6 px inset (upstream `project_panel`).
- Tabs 36 px, breadcrumb bar 28 px / 12 px text, status bar 26 px / 12 px, 16 px item gap (upstream).
- Editor: 50 px line-number column, 24 px gutter-icon column (upstream `editor`).
- Missing features: External Libraries node, gutter hook icons, live agent counts, Database/HTTP/Local History/WordPress panels, agent message in the status bar.

## User settings to change by hand (`~/.config/zenith/settings.json`)

- PHP servers: `["intelephense", "!phpactor", "!phptools", "!phpantom", "..."]` (phpantom causes the false "Function … not found"; phpactor crashes).
- Intelephense WordPress stubs under `lsp.intelephense.settings.intelephense.stubs` (default list + `"wordpress"`).
