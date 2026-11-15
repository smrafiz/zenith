# 03 — Config Layer: PHP/JS Intelligence, Inspections, Frameworks

No fork needed. Works on stock Zed and on the fork. Existing `~/.config/zed/settings.json` must be **merged, not overwritten** (backup exists: `settings.json.backup-20261115-091435`).

## Goal

Match PhpStorm/WebStorm editor intelligence: completion, navigation, rename, diagnostics/inspections, formatting, framework awareness.

## Parity checklist

| JetBrains | Zed solution | Must |
|---|---|---|
| PHP completion/navigation | Intelephense (premium licence for rename, implementations, code folding extras) | ✅ |
| PHP refactor code actions | Phpactor alongside Intelephense (import class, extract, generate accessors, implement contracts) | ✅ |
| PHP inspections | Phpactor PHPStan/Psalm extensions publishing diagnostics | ✅ |
| WordPress awareness | Intelephense `stubs` incl. `wordpress`, `wordpress-globals`, `woocommerce` (via stubs package) | ✅ |
| Laravel awareness | Research spike: Laravel IDE Helper (`barryvdh/laravel-ide-helper`) generates stubs → Intelephense understands facades/models; check for a Laravel language server usable by Zed | ✅ |
| Blade / Twig | Zed extensions (search Extensions panel) | ✅ |
| PHP formatting | Pint or php-cs-fixer as external formatter | ✅ |
| JS/TS | built-in vtsls, ESLint, Prettier | ✅ |
| Vue/Svelte/Astro | extensions | as needed |
| Tailwind | built-in tailwindcss-language-server | ✅ |
| Spell check | `codebook` or `harper` extension | nice |
| EditorConfig | built-in | ✅ |
| Keymap | `"base_keymap": "JetBrains"` | ✅ |

## Steps

1. Inventory current `settings.json`, `keymap.json`, installed extensions.
2. Install extensions: PHP, Blade, Twig, Vue, Env, Dockerfile, SQL, Make, TOML, Neon (PHPStan config).
3. Configure language servers order for PHP: `["intelephense", "phpactor", "..."]`.
4. Phpactor config `~/.config/phpactor/phpactor.json` (or project `.phpactor.json`):
   ```json
   {
     "language_server_phpstan.enabled": true,
     "language_server_psalm.enabled": false,
     "language_server_completion.trim_leading_dollar": true
   }
   ```
   Disable Phpactor completion to avoid duplicates with Intelephense (*verify key*).
5. Intelephense stubs + licence in `lsp.intelephense.initialization_options`.
6. Formatter per project via `.zed/settings.json` (Pint for Laravel, php-cs-fixer elsewhere, WPCS via phpcbf for WP).
7. Project templates: `.zed/settings.json`, `.zed/tasks.json`, `.zed/debug.json` for Laravel, WordPress plugin, Node/TS.
8. Install script `zed-kit/install.sh`: brew + npm + composer global tools, idempotent.

## Deliverables

- `zed-kit/settings.global.json` (merge-ready snippet)
- `zed-kit/templates/{laravel,wordpress,node}/.zed/*`
- `zed-kit/install.sh`
- `zed-kit/README.md`

## Tests

Manual checklist on one Laravel app, one WP plugin, one TS project: go-to-def, find refs, rename, PHPStan error shows inline, format on save, Xdebug breakpoint hits.

## Risks / open questions

- Intelephense + Phpactor duplicate diagnostics/completions — tune which features each provides.
- Laravel: no first-class LS confirmed for Zed — may require feature work later (would become a new plan doc).
- Pint `{buffer_path}` vs stdin handling — verify formatter mode.

## Effort

Core config: 2–3 days. Laravel spike: 1 week. Templates/install script: 2 days.
