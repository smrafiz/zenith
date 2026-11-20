# 36 — Notifications Tool Window

Status: ⬜ not started. Facts verified against fork @ b4130a774e.

## Goal

JetBrains-style Notifications tool window: a history of notices that outlives the toast.

## Parity checklist

- [ ] Right-rail bell button with an unread dot (must)
- [ ] "Timeline" list, newest first (must)
- [ ] "Clear all" (must)
- [ ] Card = icon, title, time, message, action links (must)
- [ ] ⋮ menu on the tool window (must)
- [ ] Notices from upstream (workspace toasts) (see Risks: no text available)

## UX

- Bell on the right rail. Dot shows while any entry is unread; unread resets when the panel is focused.
- Panel body: header "Timeline" + "Clear all"; cards below.
- Dismissing a toast keeps its timeline entry.

## Architecture

- Crate `zenith_notifications` (feature `notifications`): `timeline.rs` (entries, unread count), `panel.rs` (the tool window), `notify(cx, Notice)` API for Zenith crates.
- Upstream facts:
  - `Workspace.notifications` holds `(NotificationId, AnyView)` (`workspace/src/notifications.rs:97-140`).
  - `MessageNotification` keeps its text only inside a closure (`:672-720`). An upstream notice cannot give its text. Fallback: show the view's type name, or keep the live view.
  - No history exists upstream.
  - `StatusToast` (`toast_layer.rs:133`) is skipped in v1.
- Upstream hook (one call-site): one call after `self.notifications.push` (~`workspace/src/notifications.rs:137`) into an observer fn-pointer global. The global and its setter go in a block appended at end of file (WelcomeOverride pattern, plan 02).

## Data & settings

Timeline lives in memory, per session, in v1. No settings in v1 beyond the `notifications` feature flag.

## Actions & keymap

`ToggleNotificationsPanel`, `ClearAllNotifications`. Keys not chosen.

## Milestones

1. `timeline.rs` + `notify` API + tests.
2. Panel + rail bell + unread dot.
3. Upstream observer hook.

## Tests

- Show a notice → one entry.
- Dismiss the toast → entry stays.
- "Clear all" → timeline empty.
- Focus the panel → unread resets.

## Risks

- Workspace churn: the hook sits in a hot upstream file.
- Upstream notices have no text (see Architecture).
- Upstream-PR candidate: a "notification shown" observer (plan 16 A2).

## Owner decisions pending

- Is a single workspace call-site OK?
- Timeline per session only in v1?

## Effort

Not estimated.
