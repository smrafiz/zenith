# 09 — Advanced Refactoring

> **Status (2026-11-21):** code in `crates/zenith_refactor`, merged into fork `zenith` @ `7ef1dc7da2` (from `feat/external-libraries` @ `3ec7baecab`); built + reviewed (code + security, 2 rounds, fixes landed), UNWIRED: workspace member only, no init/umbrella feature, so its actions/panels are unreachable in the app. Wiring = its own reviewed task. Milestone ✅ below means code and tests only.

## Goal

PhpStorm-level refactorings for PHP (and TS where tsserver allows), with preview before apply.

## Parity checklist

| Refactoring | Backend | Priority |
|---|---|---|
| Rename symbol (incl. file rename for classes) | Intelephense premium / Phpactor | must |
| Move class (namespace + file + update usages) | Phpactor `class:move` | must |
| Rename/move file/dir updating namespaces | Phpactor | must |
| Extract method / variable / constant | Phpactor code actions | must |
| Inline variable / method | Phpactor (partial) | later |
| Change signature (add/remove/reorder params, update callers) | **none ready** — build on Phpactor's reference finder or custom | must (hardest) |
| Safe delete (warn on usages) | find-references + delete | must |
| Generate constructor / getters / setters / implement interface | Phpactor | must |
| Pull members up / push down | none — custom | later |
| Introduce parameter / field | Phpactor partial | later |
| TS: move to file, extract, rename file updates imports | tsserver / vtsls | must |

## UX

- `Refactor This…` menu (`ctrl-t`, JetBrains binding): context-aware list.
- Every multi-file refactor shows a **Preview** Item: tree of affected files + per-file diff, checkboxes to exclude, Apply / Cancel. (Zed's project-search-like multibuffer may serve; *verify*.)
- Undo: whole refactor = one undo group across buffers (Zed multibuffer transactions — *verify*); plus local history label "Before refactor" (feature 05).

## Architecture

- Crate `zenith_refactor`.
- Backend abstraction: `trait RefactorProvider { fn available(ctx) -> Vec<RefactorKind>; fn plan(kind, args) -> WorkspaceEdit; }`
  - `LspProvider`: LSP code actions / `workspace/executeCommand` → `WorkspaceEdit`.
  - `PhpactorCliProvider`: shells out (`phpactor class:move --dry-run`?) and converts results to edits (*verify Phpactor CLI dry-run/JSON output support*).
  - `NativeProvider` (later): change signature / safe delete implemented using LSP references + tree-sitter edits.
- Apply `WorkspaceEdit` through Zed's existing LSP edit application path (handles renames/creates/deletes).

## Change signature (design sketch)

1. Parse target function with tree-sitter PHP → params list.
2. Dialog: reorder/add (name, type, default)/remove.
3. Find references via LSP.
4. For each call site: tree-sitter locate argument list, rewrite args (insert default for added, drop removed, reorder).
5. Named arguments, spread `...$args`, callables as strings → mark "needs manual review" in preview.

## Safe delete

References via LSP → if none, delete; else show usages in preview with "Delete anyway".

## Progress (crate `zenith_refactor`)

| Step | State | Commit |
|---|---|---|
| M1 Core Restructuring Engine | ✅ `RefactorThis` action menu bindings; `derive_psr4_namespace` calculator; `plan_move_class` updating `namespace` and rewriting all `use` imports and qualified usages across project files; `plan_safe_delete` analyzing symbol usage counts and reporting all call sites with warnings; `plan_change_signature` reordering parameters, inserting default values, and rewriting caller argument lists; `RefactorPlan` diff preview applicator with per-file exclusions; clippy clean; sabotage tested. | `1e2ec762a5` |
| M2 Multi-Buffer Diff Preview UI | ✅ `RefactorPreviewModal` implementation with `ModalView`, `EventEmitter<DismissEvent>`, and `Focusable`; split view with file tree, individual inclusion/exclusion checkboxes, All/None batch selectors, diff cards with old/new deletion/creation highlights (`cx.theme().status().deleted` / `created`); atomic disk applicator `apply_to_disk` with source file cleanup on move; clippy clean; sabotage tested. | `cde3ba1b23` |

## Milestones

1. `Refactor This` menu wired to existing LSP code actions + preview UI.
2. Phpactor CLI provider: move class, move file/dir.
3. Safe delete.
4. Change signature v1 (positional args only).
5. Change signature v2 (named args), pull up/push down.

## Tests

- Fixture PHP projects with expected post-refactor snapshots.
- Preview exclusion respected.

## Risks

- Correctness: a bad refactor corrupts code — preview + local history mandatory; never apply without preview for multi-file edits.
- Phpactor/Intelephense disagreement on references (dynamic PHP) — show both counts if they differ.

## Effort

4–6 weeks.
