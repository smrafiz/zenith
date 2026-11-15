# 11 — Docker / Remote Interpreters

## Goal

Develop against PHP/Node running in Docker (Compose, Sail, DDEV, Lando) as smoothly as PhpStorm's remote interpreters: run, test, debug, composer — all with correct path mapping.

## Parity checklist

- [ ] Configure interpreter: Docker Compose service / container / local (must)
- [ ] Path mappings host ↔ container (must)
- [ ] Run file/script/tests inside container (must; consumed by 04, 07)
- [ ] Composer / npm / artisan commands via container (must)
- [ ] Xdebug in container with mappings (must)
- [ ] Language servers aware of container-only vendor (vendor usually mounted, so host LS fine) (check)
- [ ] Dev Containers (`.devcontainer/devcontainer.json`) open-in-container (later — check upstream Zed status first)
- [ ] Docker panel: containers, logs, start/stop, exec shell (useful)

## UX

- Status bar: "Interpreter: app (compose)" picker.
- Settings UI via `.zed/settings.json` `zenith.interpreter`.
- Docker panel (bottom): services list, logs stream, actions.

## Architecture

- Crate `zenith_interpreters` (+ `zenith_docker_panel`).
- `Interpreter` model: `{ kind: Local | ComposeService{file, service} | Container{name}, exec_prefix(), path_map }`.
- Exposed as task variables: `$ZENITH_EXEC` (e.g. `docker compose exec -T app`), `$ZENITH_REMOTE_FILE` (mapped path) so tasks/test runner/scratches use them.
- Auto-detect: `docker-compose.yml`/`compose.yaml` services with php image, `vendor/bin/sail`, `.ddev/`, `.lando.yml`.
- Debug: generate `.zed/debug.json` Xdebug config with `pathMappings` from interpreter.
- Docker panel: `docker compose ps --format json`, `docker compose logs -f`, via `bollard` crate or CLI (CLI = fewer deps; start with CLI).
- Output path rewriting: stack traces from container mapped back to host paths for click-to-open (shared with 07).

## Settings

```json
"zenith": {
  "interpreter": {
    "kind": "compose",
    "compose_file": "docker-compose.yml",
    "service": "app",
    "path_mappings": { "/var/www/html": "." }
  }
}
```

## Milestones

1. Interpreter model + detection + task variables.
2. Wire into test runner (07) + scratches (04).
3. Xdebug config generation.
4. Path rewriting in terminal output.
5. Docker panel.
6. Dev Containers (only if upstream lacks it).

## Tests

- Detection fixtures (compose, sail, ddev, lando).
- Path mapping both directions incl. nested mappings.

## Risks

- Upstream Zed dev-container work may overlap — check before milestone 6.
- Terminal link rewriting may need hooks in `terminal_view` (upstream file touch).

## Effort

4+ weeks.
