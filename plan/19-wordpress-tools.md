# 19 — WordPress Tools (F1)

## Goal

Best-in-class WordPress plugin/theme development — beyond PhpStorm's WP support.

## Parity checklist

- [ ] Go to hook definition: from `add_action('init', …)` / `add_filter` → all `do_action('init')` / `apply_filters` sites (incl. WP core in `wp-includes`) (must)
- [ ] Reverse: from `do_action('x')` → all listeners (must)
- [ ] Hook name completion (core + project + installed plugins) (must)
- [ ] Hover on hook: docblock, params, since-version, source (must)
- [ ] Callback resolution: string callbacks `'my_fn'`, `[$this, 'method']`, `[Class::class, 'm']`, closures → go-to callback (must)
- [ ] Hooks panel: tree of hooks in project, listeners per hook, priority/args shown (must)
- [ ] Template hierarchy navigation: from `single-product.php` show fallback chain; `get_template_part('a','b')` → file (must)
- [ ] `wp_enqueue_script/style` handle navigation + asset file go-to (later)
- [ ] Shortcode / block (`block.json`) navigation (later)
- [ ] WPCS + PHPCompatibility via inspections (21) (must)
- [ ] `wp-cli` command runner via tasks / panel (later)
- [ ] Plugin/theme scaffolds via templates (20) (must)

## Architecture (extension-first, see 16)

- **`wp-hooks-ls`** — language server (Rust, reuse tree-sitter-php) — also usable in stock Zed:
  - Indexes `add_action|add_filter|remove_*|do_action|do_action_ref_array|apply_filters|apply_filters_ref_array|has_action|has_filter` calls with literal or simple-concatenated names (dynamic names `"save_post_{$type}"` → pattern match).
  - Index scope: project + configured WP core path (`wp_core_path` setting or detected from `ABSPATH`/`wp-config.php` / composer `johnpbloch/wordpress`) + `wp-content/plugins/*` optionally.
  - LSP features: `textDocument/definition` & `references` on hook string, completion inside hook-name string, hover with docblock.
  - Core hook docs: parse `@since`, `@param` docblocks above `do_action` (WP core is well documented).
  - Persistent index cache (`~/.cache/wp-hooks-ls/<hash>`).
- **Zenith `zenith_wordpress` crate**: Hooks panel + template hierarchy view; queries the LS via custom LSP requests (`wpHooks/list`, `wpHooks/listeners`).
- Template hierarchy: rules table from WP template hierarchy docs encoded as data; resolve against active theme + parent theme (`Template:` header in `style.css`).

## Settings

```json
"zenith": { "wordpress": { "core_path": null, "index_plugins": false, "index_vendor": false } }
```

## Milestones

1. LS: index + definition/references for literal hook names (project only).
2. WP core indexing + hover docs + completion.
3. Callback resolution.
4. Hooks panel.
5. Template hierarchy + `get_template_part`.
6. Dynamic hook names, enqueue handles, blocks.

## Tests

Fixture plugin + slice of WP core; golden tests for definitions/references; perf test: index full WP core < 5 s (target).

## Risks

- Dynamic hook names can't be fully resolved — show "pattern match" results with marker.
- Large `wp-content/plugins` — opt-in indexing.

## Effort

2–3 weeks.
