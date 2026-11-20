# 38 — Terminal Parity

Status: ⬜ not started. Facts verified against fork @ b4130a774e.

## Goal

Close the JetBrains terminal gap with config first, upstream PR for what config cannot do.

## What exists

- 24-bit colour via alacritty.
- ANSI palette comes from the theme (`theme/src/styles/colors.rs:277`).
- Font settings: `settings_content/src/terminal.rs:125`.
- No OSC 133 anywhere: `TerminalBackendEvent` (`terminal.rs:725-739`) has no prompt event, and alacritty checkout `4c12966` lacks "133".

## Plan (config only)

- Audit Driftwood `terminal.ansi.*`.
- Add a Symbols Nerd Font asset (assets auto-load: `assets/src/assets.rs:49-62`). Check licence and size first. Put the font fallback in `zenith_look`, not `default.json`.
- Autosuggestions come from user shell plugins: zsh-autosuggestions, fzf, atuin; fish has it natively.
- OSC 133 shell scripts ship in `zed-kit`.
- Agent CLIs (Claude Code, Gemini CLI, Codex) run via Zed ACP agents + tasks + plan 06 + plan 22 M4.

## Upstream PR (human-owned, uncertain)

Command blocks and jump-to-prompt: alacritty `osc_dispatch` → `TerminalBackendEvent::PromptMark` → `ScrollToPrevPrompt` / `ScrollToNextPrompt`. Listed in plan 16 A2.

## Not building

Terminal completion menu; command-block copy-output.

## Owner decisions pending

- OSC 133: upstream-only, or a fork patch?
- Autosuggest from shell plugins only?

## Effort

Config part: days. PR part: not estimated.
