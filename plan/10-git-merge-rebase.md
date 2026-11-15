# 10 — Git: Merge Conflicts & Interactive Rebase

## Goal

JetBrains-grade conflict resolution and history tooling on top of Zed's existing `git_ui`.

First step: audit what current Zed already ships (git panel, inline conflict markers, branch picker, blame, stash) — only build gaps.

## Parity checklist

- [ ] Conflicts list: all conflicted files, Accept Yours / Theirs / Merge… (must)
- [ ] 3-way merge view: Left (ours) | Result | Right (theirs), per-chunk accept arrows, auto-merge non-conflicting chunks (must)
- [ ] Interactive rebase editor: list commits, reorder (drag), pick/squash/fixup/reword/drop/edit (must)
- [ ] Log view: graph, filters (branch, author, path, text), commit details, diff (must — check Zed's state first)
- [ ] Cherry-pick, revert commit from log (must)
- [ ] Compare branches / compare with revision (must)
- [ ] File history (git log for file) with diff (must)
- [ ] Shelve (stash) UI with partial apply (later)
- [ ] Partial commits (hunks/lines) (check Zed — likely exists)

## UX

- Merge view = new center `Item` with three synced editors (read-only sides, editable centre), gutter arrows `>>` / `<<` / `x`, top bar: Accept Left / Accept Right / Apply / Abort.
- Rebase editor = modal/center Item driven by `GIT_SEQUENCE_EDITOR` hook: Zed writes the todo file on Apply.
- Log = bottom panel: graph lane rendering + commit table + details split.

## Architecture

- Prefer extending inside `git_ui` only via new modules; if not possible, new crate `zenith_git_merge` depending on `git`/`git_ui`.
- Conflict data: `git ls-files -u` stages 1/2/3 → base/ours/theirs content; compute chunks with a diff3 algorithm (`similar` crate or Zed's diff utils — *verify*).
- Interactive rebase: run `git rebase -i` with `GIT_SEQUENCE_EDITOR` = small helper binary/script that hands the todo file path to Zed via the IDE server (feature 06) or a socket, waits for result.
- Log graph: `git log --format=... --topo-order` parsed; lane assignment algorithm; virtualized list for large repos.

## Milestones

1. Audit current Zed git features; update this doc's checklist.
2. Conflicts list + accept ours/theirs.
3. 3-way merge view.
4. Log + graph + file history (if missing).
5. Interactive rebase editor.
6. Cherry-pick/revert/compare.

## Tests

- diff3 chunking fixtures.
- Temp git repos created in tests (`git init`, scripted conflicts).

## Risks

- Upstream `git_ui` changes often → merge conflicts in our fork. Keep our code in separate modules/crate.
- Upstream may ship these features — re-audit each upstream release; drop ours if equivalent.

## Effort

3–4 weeks.
