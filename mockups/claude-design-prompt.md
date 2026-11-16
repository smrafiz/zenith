# Claude Design prompt — Zenith IDE (target look = mockups/zenith-v2.html)

Paste everything below the line into Claude Design.

---

Design high-fidelity desktop UI mockups for **Zenith**, a native code editor (written in Rust, GPU-rendered, very fast) built for professional PHP, WordPress, Laravel and JavaScript/TypeScript developers. Zenith aims for full PhpStorm/WebStorm feature parity — plus first-class AI coding agents — while staying much faster. It must look like a modern JetBrains IDE ("New UI" with the **Islands** theme), never like Zed or VS Code. Nothing anywhere may say "Zed".

## 1. Deliverables (artboards)

Make these artboards, each a full macOS app window at **1600 × 1000** (window 1568 × ~930 with 12 px rounded corners, on a near-black backdrop `#131416`, soft shadow `0 30px 80px rgba(0,0,0,.55)`):

1. **Editing** — calm everyday moment.
2. **Debugging** — Xdebug paused at a breakpoint.
3. **Agent review** — reviewing what an AI agent changed.
4. **Agent popover** — Editing scene with the title-bar agent popover open.
5. **Search Everywhere** — Editing scene dimmed with the search dialog open.
6. **Inline agent edit** — Editing scene with `Rest.php` open, showing an agent's pending change inline in the editor.
7. **Hook hover** — Editing scene with the WordPress hook hover card open.
8. **Run** — Editing scene with the bottom Run panel showing a finished PHPUnit run.
9. **Tool windows sheet** — every left/right tool-window panel (listed in §8) drawn as standalone 280–340 px panels on one board.
10. **Narrow** — the Editing scene at 900 px wide (side panels become overlays) and at 500 px.
11. **Component sheet** — buttons, pills, tabs, stripe buttons, status items, agent chip, review hunk card, diff rows, tree rows, inlay hint, inline value, diagnostic, breakpoint, hook gutter icon, run gutter icon.

Above each window, outside it, show a small segmented control "Editing · Debugging · Agent review" with the current scene selected and one line of grey caption describing the moment (texts in §7).

## 2. Brand and identity rules

- **App icon / logo** (top-left of title bar, 22 px, 5 px radius): a rounded square with a vertical gradient `#1b1446` → `#2a1d6b` (60%) → `#ff7a3d`; a white mountain peak line (inverted V, thick, round joins) across the lower half, a second smaller peak at 45% white opacity in front, and a warm pale sun dot `#fff4d6` above the peak.
- **Colour meaning (the core identity rule):** **blue = the IDE**, **orange = agents**. Orange `#ff7a3d` appears *only* where an AI agent is involved: the title-bar agent chip, the agent stripe button and its dot, the dot on an editor tab whose file has pending agent changes, agent-changed lines in the editor, the inline agent lens, the Agents panel's primary button, the review tab, "Accept all" and "Merge" in review, the agent node in Local History, and the "agent" marker in the project tree. Never use orange for anything else.
- Accent blue for selection, focus, active tab underline, primary buttons: `#538af9` (accent), `#71a1fe` (accent text), `#3574f0` (primary button fill).
- Tone: calm, dense, professional; information at a glance; no decoration, no gradients except the logo, no emoji.

## 3. Theme — "Driftwood" (dark only; exact values)

Chrome and panels:
- Window/chrome background and tool-window panels: `#2b2d30`
- Editor island and tab strip: `#282c34`; secondary surface (search field, file headers): `#31343a`
- Island edge: 1 px `#1e1f22` (draw as an outer ring on every island)
- Borders/dividers: `#393b40`; editor dividers: `#3b4048`
- Hover: white at 8%; selection: `#2a4371`; active tab background: `#233558`
- Text `#dfe1e5`, secondary `#b4b7be`, muted `#8c8f96`; code foreground `#abb2bf`; line numbers `#495162`; current-line background `#2c313c`
- Success `#6db083` (bg `#203b2a`), warning `#ff8c00` (bg `#44321d`), error `#f44747`
- Diff added bg `#2d4134`, deleted bg `rgba(224,108,117,.14)`; VCS modified text `#80cbc4`, added text `#c3e887`
- Debug execution line bg `#2d3f60`; breakpoint dot `#db5c5c`
- Inlay hint pill bg `#363c44`, text `#7f8794`
- Agent orange `#ff7a3d`; agent tint `rgba(255,122,61,.14)`; agent line bg `rgba(255,122,61,.10)`
- Scrollbars: thumb white 13%, no track.

Syntax (PHP-tuned One Dark, "Driftwood"):
- keyword `#c88da2` *italic* (public, function, final, class, namespace, return, void, int, string, bool, true, false, echo, new, use, extends, self, if)
- declared function/method names `#4fb3be`; function/method calls `#61afef`
- strings `#98c379`; variables `#ffb98b`; `$this` `#d4886a`
- comments `#6b7280`; numbers and constants (`LUMEN_URL`, `LUMEN_VERSION`) `#d19a66`
- types/classes `#649fc4`; namespaces `#63b7c0`; properties after `->` `#34848d` italic
- **Rainbow brackets** by depth: `#d8b860`, `#6cb463`, `#50a8ff`, `#e2a5b8` (cycle).
- **Indent guides**: 1 px vertical line `#3b4048` at each 4-character indent level, slightly brighter on the current/exec line.
- WordPress hook-name strings (e.g. `'wp_enqueue_scripts'`) get a dotted underline in `#d19a66`.

## 4. Typography

- UI: **Inter** 13 px (panel titles 12.5 px semibold, section labels 10.5 px semibold uppercase with 0.08em tracking, meta 11.5 px).
- Code and terminals: **JetBrains Mono** 13.5 px, **line height 24 px (≈1.8)**, ligatures on, italics used for keywords.
- Tabular numbers in line numbers, timings and counts.

## 5. Icons

- **File and folder icons: Atom Material style** (as in the "Atom Material Icons" JetBrains plugin): each file type is one solid, saturated glyph at 16 px with no page outline — PHP purple elephant-oval "php" badge, JS yellow square "JS", TS blue square "TS", JSON ochre braces, composer.json a conductor/music mark, package.json red npm box, phpcs.xml.dist a shield, phpunit.xml.dist a purple PHPUnit mark, readme.txt a book, Markdown blue "M↓". Folders are solid coloured folders with a lighter emblem: `includes` (open, light-blue with code emblem), `Core` (open, with core emblem), `Admin` (teal with shield/admin emblem), `src` (indigo), `build` (dimmed red/dist), `tests` (open, green with check), default folder grey, `External Libraries` green library folder.
- **Tool-window, toolbar and status icons:** thin outline icons (Lucide-like, 1.7 px stroke, round caps), 15–17 px, grey `#b4b7be`; never copy JetBrains' own UI icons.
- Gutter icons 13 px: hook (orange-brown `#d19a66`), green filled play triangle for runnable tests.

## 6. Layout (Islands)

Window grid: **title bar 42 px** / main area / **status bar 26 px**. No borders around the title bar, stripes or status bar.

Main area columns: **left stripe 40 px** · left panel (280 px, optional) · center (fills) · right panel (330 px, optional) · **right stripe 40 px**, with **5 px gaps** between islands. Every panel, the editor and the bottom panel are separate **islands**: 10 px radius, 1 px `#1e1f22` ring, no other borders.

### 6.1 Title bar (left → right)
- macOS traffic lights (11 px, `#ff5f57`, `#febc2e`, `#28c840`, 7 px apart), then the Zenith logo.
- **Project widget**: 20 px rounded square badge "LG" (white on `#4a5b8c`) + **lumen-gallery** (semibold) + chevron.
- **Branch widget**: branch icon + `feat/column-override` + chevron (opens Commit panel).
- Flexible space; **Search Everywhere** field centered (≈340 px, `#31343a`, 7 px radius): search icon, "Search everywhere", keycap `⇧⇧` on the right.
- Flexible space; **run widget**: PHPUnit icon + "AssetsTest" + chevron; green play ▶ (Run), green bug (Debug; shows a `#203b2a` background while debugging), red square Stop (only visible while running/debugging).
- **Agent chip** (pill, orange tint background, orange text): bot icon + "1 running · review" + count badge "2" (orange fill, dark text). When nothing awaits review: "1 running", no badge.
- Settings gear.

### 6.2 Left stripe (top → bottom)
Project (folder icon), Commit (branch icon), Local History (history icon); flexible gap; TODO (checklist icon), WordPress (hook icon); then bottom-panel toggles: Terminal, Problems. Buttons 30 × 30, 7 px radius; selected = `#2a4371` background.

### 6.3 Right stripe
Agents (bot icon, **orange**, with a small orange dot when changes await review; selected = orange tint), Database (cylinder icon), HTTP Client (globe icon).

### 6.4 Center
- **Editor island**: tab strip 36 px (`#282c34`, bottom divider `#3b4048`); then breadcrumb row 28 px; then editor with a **minimap** (78 px wide) on the right.
- Tabs: Atom Material file icon + name; active tab = `#233558` background + 2 px `#538af9` underline; close × on hover; **orange dot** after the name when the file has pending agent changes (Rest.php). The agent review tab: bot icon + "Review: Add REST nonce check" + orange count pill, orange text, orange-tint background and orange underline when active.
- Breadcrumbs (12 px muted, chevron separators, last item medium weight): `lumen-gallery › includes › Core › Assets.php › Assets › enqueue()`.
- Gutter: line numbers right-aligned (50 px), 24 px marker column (breakpoint, hook icon, run icon).
- Minimap: 2 px bars per line at 55% opacity, indented like the code; viewport box white 5%; markers: warning line orange `#ff8c00`, agent lines agent-orange, exec line blue.
- **Bottom island** (220 px, optional): tab row 34 px with Debug (only while debugging), Run, Problems, Terminal and a close ×; selected tab `#2a4371`.

### 6.5 Status bar (only these items)
Left: warnings count (orange warning icon + "1") — or, while debugging, a blue bug icon + "Paused · Assets.php:25"; then (Editing only, when changes await review) orange bot icon + "Claude Code waiting for review". Right: docker icon + "PHP 8.5 · docker", green check + "Intelephense", cursor "13:9" (25:9 while debugging), "UTF-8", "LF", "4 spaces".

## 7. Scenes

Project used everywhere: WordPress plugin **lumen-gallery** in `~/Sites/flux/wp-content/plugins` (theme "flux"). Open tabs: `Assets.php`, `AssetsTest.php`, `Rest.php`.

### 7.1 Editing (caption: "A normal moment: one file, one warning, hook listeners in the gutter. Agents stay in the title bar until they need you.")
- Left: Project panel open. Right: closed. Bottom: closed. Active tab: Assets.php. Current line 13 highlighted (`#2c313c`).
- Editor content (`includes/Core/Assets.php`), exact, with tabs as indentation:

```php
1  <?php
2  namespace LumenGallery\Core;
3
4  final class Assets {
5
6  	public function register(): void {
7  		add_action( 'wp_enqueue_scripts', [ $this, 'enqueue' ] );
8  		add_filter( 'lumen_gallery_columns', [ $this, 'columns' ], 10, 2 );
9  	}
10
11 	public function enqueue(): void {
12 		wp_enqueue_style( 'lumen-gallery', LUMEN_URL . 'build/gallery.css', [], LUMEN_VERSION );
13 		wp_enqueue_script( 'lumen-gallery', LUMEN_URL . 'build/gallery.js', [ 'wp-element' ], LUMEN_VERSION, true );
14 	}
15
16 	public function heading( string $title ): void {
17 		echo '<h2 class="lumen-title">' . esc_html( $title ) . '</h2>';
18 	}
19
20 	/**
21 	 * Per-gallery column override from post meta.
22 	 */
23 	public function columns( int $columns, \WP_Post $post ): int {
24 		$override = get_post_meta( $post->ID, '_lumen_columns', true );
25 		return $override ? absint( $override ) : $columns;
26 	}
27 }
```

  - Lines 7 and 8: hook icon in the gutter; hook-name strings dotted-underlined.
  - Line 8: **inlay hint pills** before `10` → `priority:` and before `2` → `accepted_args:`.
  - Line 13: wavy orange underline under `true`, and at line end a warning chip (orange text on `#44321d`, 4 px radius): "⚠ WP 6.3+: pass [ 'strategy' => 'defer' ] instead of $in_footer".
- Project tree (24 px rows, 14 px indent per level, chevrons for folders):
  - lumen-gallery (open) › includes (open) › Core (open) › **Assets.php** (selected row `#2a4371`), Plugin.php, **Rest.php** (orange name + right-aligned orange "agent" label) · Admin, Front (collapsed) · src · build (55% opacity) · tests (open) › AssetsTest.php, RestTest.php · composer.json · package.json · lumen-gallery.php · phpcs.xml.dist · phpunit.xml.dist · readme.txt · External Libraries.
- Title bar agent chip shows "1 running · review" + "2". Status bar shows the orange "Claude Code waiting for review".

### 7.2 Debugging (caption: "Xdebug paused in Assets::columns(). Inline values in the editor, frames and variables below. No agent UI competes for attention.")
- Same file, scrolled so line 25 is centred. Line 25: red breakpoint dot in the gutter, execution-line background `#2d3f60`, blue line number. **Inline values** in muted italic after the code: line 24 `$override: "4"`, line 25 `$columns: 3`. No warning chip, no current-line highlight, no agent status in the status bar.
- Run widget: Debug button active (`#203b2a` background), Stop visible.
- Bottom island open on **Debug**, three equal columns divided by `#393b40`:
  - **Frames** header with toolbar (Resume ▶, Step over, Step into, Step out): `Assets->columns()` — `Assets.php:25` (selected), `AssetsTest->test_columns_override()` — `AssetsTest.php:19`, `PHPUnit\Framework\TestCase->runTest()` — `vendor` (muted).
  - **Variables**: `$columns` int `3` · `$override` string `"4"` · ▸ `$post` WP_Post `{ID: 42, post_type: "lumen_gallery", …}` (variable names `#ffb98b`, types muted, strings green, ints `#d19a66`).
  - **Console**: `› absint( $override )` then `4` (green), then an empty prompt `› ▍`.
- Status bar left: blue "Paused · Assets.php:25"; cursor "25:9".

### 7.3 Agent review (caption: "Claude Code finished in its own worktree. Its changes open as one review tab; accept per hunk, then merge the branch.")
- Left panel closed. Right: **Agents** panel open. Active tab: the orange review tab.
- Review view (padding 16/18 px, 14 px gaps):
  - Header: orange bot icon + **Add REST nonce check** (16 px semibold); under it muted: "Claude Code · `agent/rest-nonce` · turn 3 · edits checkpointed in Local History". Right side buttons: "Run tests in worktree" (flask icon, neutral), **Accept all** (orange fill, dark text, check icon), "Reject all".
  - File card 1 (`#282c34`, `#393b40` border, 8 px radius; header row `#31343a`): PHP icon, **Rest.php**, muted `includes/Core/Rest.php`, right `+3` in green mono. Hunk header row "@@ permission() · line 14". Diff rows (line number column, sign column, code with full syntax colouring and rainbow brackets):
    ```
    15     $nonce = $request->get_header( 'X-WP-Nonce' );
    16 +   if ( ! wp_verify_nonce( $nonce, 'wp_rest' ) ) {
    17 +       return false;
    18 +   }
    19     return current_user_can( 'read' );
    ```
    Added rows `#2d4134` with green `+`. Footer: "✓ Accept" (green text), "× Reject" (red text), "Open in editor".
  - File card 2: PHP icon, **RestTest.php**, muted `tests/RestTest.php`, right "new · +9". Hunk "@@ new test · line 22":
    ```
    22 + public function test_rejects_missing_nonce(): void {
    23 +     $request  = new \WP_REST_Request( 'GET', '/lumen/v1/galleries/42' );
    24 +     $response = rest_do_request( $request );
    25
    26 +     $this->assertSame( 403, $response->get_status() );
    27 + }
    ```
    Same footer buttons.
  - Also draw the **after** state on the same board: both hunks collapsed to "✓ Accepted · Undo" rows, and above them a merge banner (orange 35% border, orange 10% background, 8 px radius): merge icon + "Review done. Merge **agent/rest-nonce** into **feat/column-override**?" + **Merge** (orange) + "Discard worktree".
- Agents panel (right): orange primary "+ New task in worktree"; three rows (status dot, title, status pill; meta line under):
  1. orange dot · **Add REST nonce check** · orange pill "2 to review" — Claude Code · `agent/rest-nonce` · 2 files · +12 −0 · 4m
  2. pulsing blue dot · **Escape gallery output (WPCS)** · blue pill "running" — Codex · `agent/escape-output` · step 7 · 2m
  3. green dot · **Gallery block → apiVersion 3** · green pill "done" — Gemini CLI · `agent/block-v3` · tests 18/18 · 12m
  - Section "CODEX · LIVE" with a small mono log: `› reading includes/Core/Assets.php`, `› editing heading() (+1 −1)`, `› running composer lint`.
- The tab strip still shows Assets.php, AssetsTest.php, Rest.php (orange dot).

### 7.4 Agent popover (from the title-bar chip)
360 px card under the chip, `#2b2d30`, `#393b40` border, 10 px radius, big soft shadow. Label "AGENTS"; the three agent rows from 7.3 (the first with an orange "Review 2" button); footer: orange "+ New task" and neutral "Open Agents panel".

### 7.5 Search Everywhere
Window dimmed (black 45%); dialog 640 px wide, 80 px from top, 12 px radius. Tabs: All (selected), Classes, Files, Symbols, Hooks, Actions. Input row: search icon, placeholder "Classes, files, symbols, WordPress hooks, actions", `esc` keycap. Results (row icon, bold name, muted detail, right-aligned uppercase kind): Assets — LumenGallery\Core (CLASS, highlighted); Rest — LumenGallery\Core; AssetsTest — tests; phpcs.xml.dist — project root (FILE); composer.json — project root; Assets::columns() — Assets.php:23 (SYMBOL); lumen_gallery_columns — filter · 1 listener (HOOK); wp_enqueue_scripts — action · 3 listeners; New Agent Task in Worktree (ACTION); Show Local History — ⌥⇧H; Import Settings from PhpStorm. Also show the filtered state for the query "hook" (only the two HOOK rows).

### 7.6 Inline agent edit (Rest.php open)
Breadcrumb `lumen-gallery › includes › Core › Rest.php › Rest › permission()`. Code:

```php
1  <?php
2  namespace LumenGallery\Core;
3
4  final class Rest {
5
6  	public function register_routes(): void {
7  		register_rest_route( 'lumen/v1', '/galleries/(?P<id>\d+)', [
8  			'methods'             => 'GET',
9  			'callback'            => [ $this, 'show' ],
10 			'permission_callback' => [ $this, 'permission' ],
11 		] );
12 	}
13
14 	public function permission( \WP_REST_Request $request ): bool {
15 		$nonce = $request->get_header( 'X-WP-Nonce' );
16 		if ( ! wp_verify_nonce( $nonce, 'wp_rest' ) ) {
17 			return false;
18 		}
19 		return current_user_can( 'read' );
20 	}
21 }
```

Above line 16, an unnumbered **lens row** (Inter 12 px, muted): orange bot icon + "Claude Code · agent/rest-nonce" (orange, medium), "added a nonce check", then links "Accept", "Reject", "Review all". Lines 16–18 have the agent line background and a 2 px orange bar on the right edge of the line-number column; the minimap shows them in orange.

### 7.7 Hook hover card
Hovering `'wp_enqueue_scripts'` on line 7 shows a 380 px card below it: header (hook icon, mono **wp_enqueue_scripts**, blue pill "action", right "3 listeners"); rows (function name in `#4fb3be` mono, location muted right-aligned): `Assets::enqueue()` — `includes/Core/Assets.php:11`; `Rest::scripts()` — `includes/Core/Rest.php:30`; `flux_assets()` — `themes/flux/functions.php:42`; footer "⌥⏎ go to listeners". For `lumen_gallery_columns`: grey pill "filter", one listener `Assets::columns()` — `includes/Core/Assets.php:23`.

### 7.8 Run panel
Bottom island on **Run**: 2 px green progress bar (full), then mono output:
```
docker compose exec app vendor/bin/phpunit tests/AssetsTest.php   (muted)
PHPUnit 11.5.2 by Sebastian Bergmann and contributors.

..                                                  2 / 2 (100%)

Time: 00:00.412, Memory: 18.00 MB

OK (2 tests, 2 assertions)                                          (green)
```
Also show `AssetsTest.php` in the editor for this board, with green play icons in the gutter on lines 6, 8 and 15:

```php
1  <?php
2  namespace LumenGallery\Tests;
3
4  use LumenGallery\Core\Assets;
5
6  final class AssetsTest extends WP_UnitTestCase {
7
8  	public function test_registers_hooks(): void {
9  		$assets = new Assets();
10 		$assets->register();
11
12 		$this->assertSame( 10, has_action( 'wp_enqueue_scripts', [ $assets, 'enqueue' ] ) );
13 	}
14
15 	public function test_columns_override(): void {
16 		$post = self::factory()->post->create_and_get( [ 'post_type' => 'lumen_gallery' ] );
17 		update_post_meta( $post->ID, '_lumen_columns', '4' );
18
19 		$this->assertSame( 4, ( new Assets() )->columns( 3, $post ) );
20 	}
21 }
```

Other bottom tabs for the component/tool sheet — **Problems**: one row, orange warning icon, mono `Assets.php:13`, "WP 6.3+: pass [ 'strategy' => 'defer' ] instead of $in_footer", source "Zenith WordPress" right. **Terminal**: `lumen-gallery feat/column-override › composer lint` (prompt green, branch muted, command white), "No coding standard violations." (green), new prompt with cursor.

## 8. Tool-window panels (board 9)

Panel header 36 px: title (12.5 px semibold) + close ×. Section labels uppercase muted.

- **Project** — as in §7.1.
- **Commit** — "CHANGES · 2": Assets.php (teal, modified) `includes/Core`; AssetsTest.php (light green, added) `tests`. Commit message box (`#282c34`, 6 px radius): "feat: per-gallery column override". Checkboxes (blue): "Run PHPCS before commit" ✓, "Run tests before commit" ✓. Buttons: **Commit** (blue fill), "Commit and Push…".
- **Local History** — timeline rows (time mono muted, 9 px node, title, small meta): "ASSETS.PHP · TODAY": 16:42 Saved (+3 −0); 16:20 blue-ring node "Before checkout feat/column-override" (automatic label); 15:58 "phpcbf (WPCS)" (+6 −6). "REST.PHP · TODAY": 16:44 **orange filled node** "Claude Code · turn 3" (agent checkpoint · +3 −0).
- **TODO** — rows with pills: orange "FIXME" cache gallery query per request — Rest.php:58; grey "TODO" lazy-load lightbox — edit.js:40; "TODO" update "Tested up to" — readme.txt:6.
- **WordPress** — "HOOKS": wp_enqueue_scripts (action · 3), rest_api_init (action · 1), lumen_gallery_columns (filter · defined), all mono with hook icons. "TEMPLATE FOR SINGLE LUMEN_GALLERY": `single-lumen_gallery.php` muted "missing"; `single.php` green "used".
- **Agents** — as in §7.3.
- **Database** — "WP_LOCAL · MYSQL 8.4 · DOCKER": ▾ wordpress (12 tables) › wp_posts 1,284 · wp_postmeta 9,731.
- **HTTP Client** — mono request `GET {{root}}/lumen/v1/galleries/42` / `X-WP-Nonce: {{nonce}}` / `Accept: application/json`; blue **Send** button; muted "200 OK · 38 ms · 412 B" and pill "env: local"; JSON response `{ "id": 42, "title": "Autumn Market", "columns": 4, "images": [ … 18 items ] }`; History rows: green "200" GET /galleries/42 now, red "401" POST /galleries 3m.

Extra tool windows (reachable from the stripes' overflow; draw them on the same board):
- **Tests** — pills "14 passed", "1 failed", "1 paused". "PHPUNIT 11.5 · DOCKER: APP": ▾ AssetsTest 41 ms › ✓ test_registers_hooks 12 ms, ✓ test_enqueue_is_versioned 8 ms, bug icon **test_columns_override** (orange text, "paused", selected); ▾ RestTest 96 ms › × test_requires_nonce 31 ms (red), ✓ test_lists_galleries 44 ms, ✓ test_rejects_bad_id 21 ms. "JEST · @WORDPRESS/SCRIPTS": gallery/edit.test.js 9 ✓, gallery/save.test.js 2 ✓.
- **Scratches** — "+ New scratch"; scratch_meta.php (2m · run in docker: app), postmeta.sql (wp_local), rest.http (env: local), release-notes.md (yesterday), tinker.js (node 22).
- **Bookmarks** — 1 Assets.php:23 — columns override (selected); 2 Rest.php:14 — permission; A edit.js:40 — lightbox.
- **Composer & npm** — "COMPOSER": wp-coding-standards/wpcs 3.1.0 with orange update pill 3.2.0; phpunit/phpunit 11.5.2; yoast/phpunit-polyfills 3.0.0; phpstan/phpstan 2.1.4. "NPM": @wordpress/scripts 30.6.0 → pill 31.0.0; @wordpress/element 6.12.0. "SCRIPTS" with green play icons: composer test, composer lint, npm run build, npm run start.
- **Database console** — under the table tree: mono query `SELECT post_id, meta_value FROM wp_postmeta WHERE meta_key = '_lumen_columns';` (keywords coloured), blue "Run ⌘↵", "3 rows · 4 ms", result grid post_id / meta_value: 42/4, 57/2, 63/6.

## 9. Components and states (board 11)

Buttons (26 px, 6 px radius, Inter 12 px medium): neutral (`#2b2d30`, `#393b40` border; hover border `#8c8f96`), primary blue `#3574f0`, agent orange (`#ff7a3d`, text `#1e1f22`), ghost-ok (green text), ghost-bad (red text). Pills (20 px, fully rounded, 11 px): agent, ok, muted, warning, running (blue `#61afef` on 14% blue). Focus ring: 2 px `#538af9`. Hover backgrounds white 8%. Status dots: running = blue (pulsing), waiting = orange, done = green.

## 10. Narrow behaviour (board 10)

≤ 1100 px: search shows only the icon; some status items hide. ≤ 900 px: side panels float as overlays on top of the editor (shadow), minimap hidden, bottom island 170 px, branch name hidden (icon only), run configuration hidden. ≤ 560 px: agent chip shows icon + count only, keycaps hidden. The page never scrolls sideways; long code lines scroll inside the editor.

## 11. Accessibility

Every icon button has a visible tooltip/label and a keyboard focus ring; status is never shown by colour alone (pills carry words, dots sit next to text); contrast ≥ 4.5:1 for text; pulsing stops under reduced motion.

## 12. Do not

- No "Zed" text, logo or Zed-style UI; no VS Code look.
- No JetBrains product logos or copied JetBrains UI icons (Atom Material-style file icons are fine).
- No orange outside agent contexts; no light theme; no gradients except the logo; no emoji; no lorem ipsum — use the exact content above.
- Don't show every feature at once: each scene shows one moment.
