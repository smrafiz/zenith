# 33 — Zenith Accounts

Status: ⬜ brief only (2026-11-16) — run `lead-engineer` with this brief before any code.

## Goal

A Zenith account, separate from zed.dev, that the editor signs in to with GitHub OAuth. It unlocks features that need a server: settings sync, licensing, and a plugin store.

## Decided (owner, 2026-11-16)

- Own service, own database. Not zed.dev, not a self-hosted copy of upstream `crates/collab`.
- **Plinth** (`~/GithubRepos/plinth`) hosts the Zenith website as a tenant (`zenith.plinthsites.com`: landing page, docs, changelog, blog). The account service is separate: Plinth's users are CMS editors, and it has no per-user blob storage, licences or plugin registry. Reuse its patterns (Next.js, Prisma, better-auth), not its database.
- Until this ships, the Zed "Sign In" button is hidden: `title_bar.show_sign_in` defaults to `false` (fork `fdb008e667`).

## Scope to design

1. **Auth:** GitHub OAuth through better-auth; the editor's browser hand-off (Zed's flow: open browser → token returned to a localhost port → verify with key pair). Decide whether to adapt the fork's `client` crate or add a `zenith_account` crate behind a hook.
2. **Settings sync:** per-user settings/keymap blobs, versioned, conflict rule (last write wins vs merge).
3. **Licensing:** free vs paid tier, offline grace period, how the editor checks.
4. **Plugin store:** registry and download API; whether to proxy or replace Zed's extension API (`zed-kit` extension ids from plan 32 chunk 7).
5. **Title bar:** a Zenith "Sign In" in place of Zed's.
6. **Privacy:** what is stored, deletion, no telemetry by default.

## Open

- Hosting for the service (Vercel + managed Postgres like Plinth, or elsewhere).
- Does licensing exist at all, or is Zenith free with paid sync?
- Plugin store before or after settings sync?
