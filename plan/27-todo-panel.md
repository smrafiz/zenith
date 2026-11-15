# 27 — TODO Panel (F9)

## Goal

JetBrains TODO tool window: find all TODO-style comments, grouped, navigable.

First: check whether upstream Zed or an extension already highlights/lists TODOs.

## Parity checklist

- [ ] Patterns (configurable regex, case-insensitive): `TODO`, `FIXME`, `HACK`, `XXX`, `shortcut:` (ponytail debt), `@todo` (must)
- [ ] Scopes: project / current file / changed files (git) (must)
- [ ] Group by file / by pattern; counts (must)
- [ ] Click → jump; live update on save (must)
- [ ] Highlight in editor (colour per pattern) (must — via LS hint diagnostics or tree-sitter highlights query)
- [ ] Filter by author (git blame) / age (later)
- [ ] Warn on commit if new TODOs added (later)

## Architecture

- Crate `zenith_todo`; scan only comments: ripgrep-style search (Zed's project search engine — *verify* reusable API) then confirm with tree-sitter that match is inside a comment node.
- Incremental: rescan file on save via `zenith_core::jobs`; full scan on panel open (respect `.gitignore`, `file_scan_exclusions`).
- Highlighting: extension-provided highlights query `(comment) @comment.todo` with injection, or LS emitting `Hint` diagnostics (16).

## Settings

```json
"zenith": { "todo": { "patterns": ["\\bTODO\\b", "\\bFIXME\\b", "\\bHACK\\b", "shortcut:"], "scope": "project" } }
```

## Effort

2–3 days.
