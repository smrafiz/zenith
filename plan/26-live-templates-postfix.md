# 26 — Live Templates & Postfix Completion (F8)

## Goal

PhpStorm live templates (abbreviation → expandable snippet with tab stops & expressions) and postfix completion (`$x.if` → `if ($x) {}`).

## Parity checklist

- [ ] Live templates per language with tab stops, defaults, `$END$` (Zed snippets already cover basics) (must)
- [ ] Template expressions: `className()`, `methodName()`, `fileNameWithoutExtension()`, `date()`, `camelCase()`, `snakeCase()` (must)
- [ ] Surround-with templates (select → wrap in `if`/`try`/`foreach`) (must)
- [ ] Postfix PHP: `.if .notnull .null .foreach .return .var .isset .empty .throw .par .not .echo .dd .dump` (must)
- [ ] Postfix JS/TS: `.if .const .let .return .log .await .forof .not .par` (must)
- [ ] Custom postfix templates (later)
- [ ] Import PhpStorm live templates XML (31) (later)

## Architecture (extension-first, 16)

- **Expressions in snippets**: Zed snippet variables are limited (*verify* supported variables). Options:
  - A. `zenith-snippets-ls`: LS that provides completions with `insertTextFormat: Snippet`, computing expression values server-side (class name via tree-sitter, file name, etc.). Works in stock Zed.
  - B. Fork-side snippet variable resolver.
  - Pick **A**.
- **Postfix**: same LS: when completion triggered after `.` on an expression, return postfix items whose `textEdit` replaces the expression range (expression found via tree-sitter: nearest complete expression ending at cursor).
- **Surround-with**: code action from LS on non-empty selection → templates list → `WorkspaceEdit`.
- Template storage: JSON per language in `~/.config/zenith/live-templates/` + built-ins.

## Milestones

1. LS skeleton + PHP postfix (`.if .foreach .var .return .dd`).
2. JS/TS postfix.
3. Live templates with expressions.
4. Surround-with.
5. Custom templates + import.

## Risks

Completion noise: postfix items must only appear after `.` on a valid expression and rank below real member completions; in PHP `.` is concatenation — trigger only when followed by a known postfix key prefix.

## Effort

1–2 weeks.
