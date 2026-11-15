# 31 — PhpStorm/WebStorm Migration Tool (F13)

## Goal

One command imports a developer's JetBrains setup and project config into Zenith.

## What to import

| Source | Location | Target |
|---|---|---|
| Keymap (custom) | `~/Library/Application Support/JetBrains/<Product><ver>/keymaps/*.xml` | `~/.config/zed/keymap.json` (map JetBrains action ids → Zed/Zenith actions; unknown → report) |
| Live templates | `.../templates/*.xml` | 26 live templates JSON |
| File templates | `.../fileTemplates/` + project `.idea/fileTemplates` (Velocity) | 20 templates (subset: `${NAME}`, `${NAMESPACE}`, `#if` basics) |
| Run configurations | project `.idea/workspace.xml` / `.run/*.run.xml` (PHPUnit, npm, PHP script, Docker) | `.zed/tasks.json`, `.zed/debug.json`, 07 test config |
| PHP interpreters / Docker | `.idea/php.xml`, `workspace.xml` | 11 interpreter settings |
| Path mappings / servers (Xdebug) | `.idea/php.xml` servers | `.zed/debug.json` pathMappings |
| Data sources | `.idea/dataSources.xml` (+ `.local.xml`) | 12 `.zed/databases.json` (no passwords; prompt to enter into Keychain) |
| HTTP client envs | `http-client.env.json` (same format — no conversion) | 08 uses as-is |
| Code style | `.idea/codeStyles/*.xml` | `.editorconfig` + formatter settings (best-effort) |
| Scopes / excluded dirs | `.idea/*.iml` excludeFolder | `file_scan_exclusions` |
| Inspection profile | `.idea/inspectionProfiles` | report only (map to 21 analyzers where obvious) |
| Plugins list | IDE config | report suggested Zed extensions |
| Bookmarks | `workspace.xml` | 28 |

## UX

Action `zenith_migrate::ImportFromJetBrains`: detects installed JetBrains products/versions → choose product + scope (global / this project) → preview of every file to be written (diff) → Apply → report (imported / skipped / unsupported).

## Architecture

- Crate `zenith_migrate` (could also ship as standalone CLI `zenith-migrate` — no UI needed for core logic).
- XML via `quick-xml` / `roxmltree`.
- Action-id mapping table `jetbrains_actions.json` (JetBrains action id → Zed action) — the big data task; start with ~150 most used.
- Never overwrite: merge into existing JSON files; backup originals (`*.backup-<date>`).
- Secrets: never imported (JetBrains stores in Keychain anyway).

## Milestones

1. Detection + run configurations + Xdebug mappings (highest value).
2. Data sources + interpreters.
3. Keymap mapping.
4. Live/file templates.
5. Code style, exclusions, reports.

## Tests

Fixture `.idea` folders from real projects (sanitized); golden output files.

## Effort

1–2 weeks (+ ongoing keymap mapping).
