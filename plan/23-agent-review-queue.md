# 23 — Agent Review Queue (F5)

## Goal

Every change an agent makes — via Zed Agent Panel, ACP agents, the IDE server (06), or a CLI agent writing files directly — lands in one review queue, backed by local-history checkpoints (05), so nothing is applied blind and everything is revertible.

## Parity checklist

- [ ] Capture sources: Agent Panel edits, IDE-server `open_diff`, external file writes during an active agent session (must)
- [ ] Checkpoint before each agent turn (local history label `agent:<session>:<turn>`) (must)
- [ ] Queue panel: grouped by session → turn → file, with +/− counts (must)
- [ ] Per hunk: accept / reject; per file; per turn ("revert everything this turn did") (must)
- [ ] Run inspections/tests on the pending set (21/07) (must)
- [ ] Annotate: why-comment from agent message linked to each turn (later)
- [ ] Policy: "auto-accept paths matching glob" (e.g. tests) (later)

## Architecture

- Crate `zenith_agent_review`, depends on `zenith_local_history`.
- Session tracking: session started by (a) Agent Panel thread start (*verify event*), (b) IDE server client connect, (c) 22 task start, (d) manual "Start agent session".
- External writes: worktree FS events during an active session → attribute to session; diff vs last checkpoint.
- Accept = mark reviewed (content stays); Reject = restore hunk from checkpoint via buffer edit (undoable).
- Zed already has an agent diff review UI — reuse/extend it for Agent Panel edits; queue unifies sources (*verify* reusability).

## UX

Right-stripe "Review" panel (or tab inside 22's Agents panel). Badge with pending count in title bar.

## Milestones

1. Sessions + checkpoints per turn (requires 05).
2. External-write capture + queue panel + file/turn revert.
3. Hunk-level accept/reject.
4. Run checks on pending set; policies.

## Risks

Attribution ambiguity when the user edits during an agent session — show "mixed" marker, never auto-revert user edits.

## Effort

1–2 weeks.
