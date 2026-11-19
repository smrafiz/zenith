# Repo admin

Moved from `CLAUDE.md` (2026-11-19); needed only for account, admin or licensing tasks.

- gh accounts on this machine: `smrafiz` (default, write access) and `wp-sigmadevs` (owner). Repo settings/admin tasks: `gh auth switch -u wp-sigmadevs`, then switch back to `smrafiz`.
- Personal-account repo ⇒ collaborators can't get admin; that's fine, owner does admin tasks.
- Enabled: Discussions, private vulnerability reporting, secret scanning + push protection, Dependabot alerts.
- Licence: MIT for this repo. Fork code follows Zed licences (GPL-3.0 editor, AGPL server, Apache GPUI); new `zenith_*` crates GPL-3.0-or-later. Standalone LSes (wp-hooks-ls, etc.) MIT in own repos.

GitHub tracking: 32 issues (one per plan doc 01–31, plus #32 for plan 35), 6 milestones (Phase 0–5), labels `layer:*`, `type:*`, `continuous`.
