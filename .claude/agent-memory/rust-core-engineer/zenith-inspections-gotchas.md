---
name: zenith-inspections-gotchas
description: zenith_inspections crate traps - cargo fmt reformats old code, PHPStan baseline behaviour, git facts verified 2026-11-20
metadata:
  type: project
---

- `cargo fmt -p zenith_inspections` rewrites ~20 pre-existing long lines in tests.rs and zenith_inspections.rs (crate was never fmt-clean at 8bcf87ad77). Format only new files, or revert unrelated hunks with `git apply -R --unidiff-zero` (git checkout -- is blocked by the Supercharger hook).
- PHPStan 2.1.40 (real runs, 2026-11-20): single-file runs never report unmatched baseline patterns; whole-project runs put path-scoped ones in `files[..].messages` (identifier `ignore.unmatched`, line null, ignorable false) and global ones in top-level `errors`. A real PHPStan lives at ~/GithubProjects/easy-demo-importer/vendor/bin/phpstan (php via Herd).
- git 2.54 (Apple): `git diff --merge-base --end-of-options <base> -- f` works; `ls-files --error-unmatch` exits 1 for untracked, 128 for not-a-repo.
- Disk: shared target dir compile dropped df from 33Gi to 27Gi in one test build; the >=30 GiB gate then blocks further runs.
- B2 (2026-11-20, zed-p21 feat/inspections-baseline): test recipe for git+project tests = real tempdir repo + FakeFs tree at the same path with `.git: {}` and `fake.with_git_state(&root.join(".git"), false, |s| s.default_branch_ref = Some("refs/heads/main".into()))` (crates/fs/src/fake_git_repo.rs:71) so `Repository::default_branch(true)` -> "main"; `db::AppDatabase::test_new()` as App global gives an isolated KVP. Untrusted worktree = `project::trusted_worktrees::init(Default::default(), cx)` + `Project::test_with_worktree_trust`; trust it later via `TrustedWorktreesStore::trust(&worktree_store, [PathTrust::Worktree(id)].into_iter().collect(), cx)`.
- git marker that proves git ran despite GIT_HARDENING: `.gitattributes` `*.php filter=probe` + `git config filter.probe.clean 'touch M; cat'`, and an UNCOMMITTED edit (stat-clean files are not re-read). fsmonitor marker cannot prove it (hardening disables it).
- ~12 sabotage rebuilds of the test binary cost ~6 GiB of df on the shared target; do sabotage last and check df first.
