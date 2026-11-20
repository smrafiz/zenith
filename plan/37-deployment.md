# 37 — Deployment (Remote Host tool window + Deployment dialog)

Status: ⬜ NOT STARTED. Blocked on owner decisions (see end). Facts verified against fork @ b4130a774e unless marked UNVERIFIED.

## Goal

JetBrains Deployment: upload a local project to a server (FTP/FTPS/SFTP) and browse it.

## Parity checklist

- [ ] Remote Host tool window: host dropdown (`<None>`), toolbar (upload, download, sync, disconnect), remote tree (must)
- [ ] Deployment dialog: connection config — type FTP/FTPS/SFTP, host, port, user, password (Keychain), root path, web URL, passive mode (must)
- [ ] Mappings (local path to remote path) and excluded paths (must)
- [ ] Upload on save (must, off by default; see Security)
- [ ] SSH hosts: use Zed remote projects (`remote/src/transport/ssh.rs:310-379`). Gap Zenith fills: FTP/FTPS, local-to-server mirror, upload on save.

## Architecture

- Crate `zenith_deploy` (feature `deploy`): `config.rs`, `mapping.rs`, `sftp.rs` (system `sftp -b -`), `ftp.rs`, `sync.rs`, `panel.rs`, `dialog.rs`, `on_save.rs`.
- Secrets via `zenith_core::secrets` (plan 15), which uses `cx.read_credentials` / `write_credentials` / `delete_credentials` (`gpui/src/app.rs:2012/2040/2045`).
- NEVER use `zed_credentials_provider::global`: the Dev channel stores plaintext JSON (`zed_credentials_provider.rs:46-60,130-147`).

## Security (trust boundaries)

1. A cloned project's deployment file can name an attacker host with upload on save. Require per-server user confirmation; upload on save is off by default.
2. FTPS validates certificates. Plain FTP only behind an explicit insecure toggle. SFTP host keys come from OpenSSH `known_hosts`; no auto-accept.
3. Remote names reject `..`, absolute paths, NUL, and symlinks that escape the mapped root.
4. No secrets on argv; askpass or stdin only.
5. Excludes default to `.env`, `.git`, `node_modules`, `.zenith`.

## Milestones

Not planned until the owner decisions below are made.

## Tests

Not written yet. Must cover each security rule above.

## Risks

- Keychain prompts on ad-hoc-signed Dev builds — UNVERIFIED.

## Owner decisions pending

- Protocols: SFTP first?
- Approve new dependency `suppaftp` (FTP/FTPS)?
- Allow plain FTP at all?
- Server definitions: user DB or project file?

## Effort

Not estimated.
