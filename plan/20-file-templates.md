# 20 — File & Project Templates (F2)

## Goal

PhpStorm "New → PHP Class" flow: correct namespace from PSR-4, proper file name, plus project scaffolds.

## Parity checklist

- [ ] New PHP Class / Interface / Trait / Enum: dialog (name, kind, extends, implements, final/abstract, strict_types) (must)
- [ ] Namespace computed from `composer.json` `autoload.psr-4` (+ `autoload-dev`) for the target directory (must)
- [ ] New from project panel context menu (target dir = selected dir) (must)
- [ ] Templates for: PHPUnit/Pest test, Laravel controller/model/migration (prefer `artisan make:*` when available), WP plugin main file (header), WP theme files, Gutenberg block (`block.json` + index), TS/React component (must)
- [ ] User templates: `~/.config/zenith/templates/` + project `.zed/templates/` (must)
- [ ] Variables: `${NAME}`, `${NAMESPACE}`, `${DATE}`, `${USER}`, `${PACKAGE}`, `${TEXT_DOMAIN}` (WP), custom prompts (must)
- [ ] Import PhpStorm file templates (`.idea/fileTemplates`, Velocity syntax subset) — see 31 (later)
- [ ] Project scaffolds: WP plugin, WP theme, Laravel package (later)

## UX

- Project panel right-click → "New ▸" submenu listing templates for this context (PHP dir → PHP templates first).
- Action `zenith_templates::NewFromTemplate` (`cmd-n` in project panel, like JetBrains `alt-insert`/`cmd-n`).
- Modal: template picker → fields form → preview path → Create → opens file with cursor at `${CURSOR}`.

## Architecture

- Crate `zenith_templates`.
- Template format: folder per template:
  ```
  php-class/
    template.toml   # name, applies_to (glob/lang), file_name = "${NAME}.php", prompts = [...]
    content.php     # body with ${VARS}, ${CURSOR}
  ```
  Simple `${VAR}` + `{{#if}}`-style conditionals (use a small existing engine like `minijinja` if already a Zed dep; else tiny custom).
- PSR-4 resolver from `zenith_core::detect::composer`: longest-prefix match dir → namespace; warn if dir isn't PSR-4-mapped.
- Built-in templates shipped in `assets/zenith/templates/`.
- Framework generators: if Laravel detected and template has `generator = "php artisan make:controller ${NAME}"`, run via `zenith_core::process` (with interpreter prefix from 11), then open created file.

## Milestones

1. Template engine + PSR-4 resolver + New PHP Class/Interface/Trait/Enum.
2. Project panel menu + user templates.
3. Test/WP/Laravel/TS templates; artisan generators.
4. Project scaffolds.

## Tests

PSR-4 resolution fixtures (multiple prefixes, autoload-dev, nested); template rendering golden tests.

## Effort

1 week (+3 days scaffolds).
