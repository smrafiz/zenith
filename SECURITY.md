# Security Policy

## Reporting a vulnerability

Please **do not open a public issue** for security problems.

Report privately via GitHub: **Security → Report a vulnerability** on this repository
(private vulnerability reporting). Include affected component, steps to reproduce, and impact.

You can expect an acknowledgement within 7 days.

## Scope

- This repository: plan documents and `zed-kit` configuration.
- Zenith source code lives in the fork (`wp-sigmadevs/zed`, branch `zenith`) — report there once it exists.
- Vulnerabilities in upstream Zed should go to [zed-industries/zed](https://github.com/zed-industries/zed/security).

## Sensitive areas (by design)

Zenith features that need extra care: the local IDE/MCP server (plan/06 — localhost only, token auth),
database credentials (plan/12 — macOS Keychain only), HTTP client secrets (plan/08), agent worktrees (plan/22).
