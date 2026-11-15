# 08 — HTTP Client

## Goal

JetBrains HTTP Client parity: `.http`/`.rest` files with run gutter buttons, environments, variables, response viewer, history.

## Parity checklist

- [ ] `.http` syntax highlighting (tree-sitter grammar; check existing Zed extension first) (must)
- [ ] Run request at cursor (gutter ▶ + action) (must)
- [ ] Multiple requests separated by `###` (must)
- [ ] Variables `{{var}}`, env files `http-client.env.json` + `http-client.private.env.json` (JetBrains format) (must)
- [ ] Environment switcher (must)
- [ ] Response viewer: status, time, size, headers, pretty JSON/XML/HTML, raw (must)
- [ ] Save response to history; compare with previous (must)
- [ ] Request chaining: `> {% client.global.set("token", response.body.token) %}` response handlers (later — needs JS engine)
- [ ] Dynamic vars `{{$uuid}}`, `{{$timestamp}}`, `{{$randomInt}}` (must)
- [ ] Auth helpers: Basic, Bearer (must); OAuth2 flow (later)
- [ ] Multipart / file upload `< ./file.json` (must)
- [ ] Copy as cURL / import from cURL (must)
- [ ] GraphQL, WebSocket, gRPC (later)

## UX

- Gutter ▶ on each request line (via Zed runnables/tasks mechanism or custom gutter decoration — *verify which is extensible*).
- Response opens in a center `Item` (split right): tabs Body / Headers / Raw / Timeline; JSON rendered in a read-only editor buffer (gets highlighting + folding for free).
- Status bar: active environment selector.
- History panel: list of past responses per request, click to open, "Compare with current".

## Architecture

- Crate `zenith_http`.
- Parser: hand-written parser for the JetBrains `.http` format → `HttpRequest { method, url, headers, body, handlers, name }`. Unit-test heavily.
- Variable resolution: env files (project root or `.http` file dir), private env merged on top, `.env` optional.
- HTTP: Zed's `http_client` crate (reqwest-based? *verify*) — must support custom TLS (self-signed toggle), redirects toggle, timeouts, cookies jar per env.
- Response handlers (later): embed a JS engine (`boa` or `rquickjs`) — significant dep; decide in milestone 5.
- History: files under `.idea/httpRequests`-like `~/.local/share/zenith/http-history/<project-hash>/` (bodies on disk, index in SQLite).

## Settings

```json
"zenith": {
  "http": {
    "enabled": true,
    "default_env": "dev",
    "timeout_ms": 30000,
    "follow_redirects": true,
    "allow_insecure_tls": false,
    "history_limit": 200
  }
}
```

## Security

- Private env file auto-added to `.gitignore` suggestion; never written into history headers (mask `Authorization`, `Cookie` in history by default).
- `allow_insecure_tls` per env only, default false.

## Milestones

1. Parser + variable resolution + tests.
2. Run at cursor → response Item (body/headers/raw).
3. Environments + status bar switcher + dynamic vars.
4. History + compare; cURL import/export.
5. Response handlers (JS engine decision).
6. GraphQL/WebSocket (later).

## Tests

- Parser fixtures (JetBrains docs examples).
- Variable precedence tests.
- Local mock server (`httpmock`/`wiremock` crate if acceptable) for integration tests.

## Risks

- JS handler compatibility with JetBrains `client`/`response` API — scope a subset.
- Large responses — stream to disk, cap in-editor display (e.g. 5 MB).

## Effort

3–4 weeks (+1–2 for JS handlers).
