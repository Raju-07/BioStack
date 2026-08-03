# Modern Profile Editing Changes

## Summary

This update improves login routing, section grouping, public-profile owner editing, and mobile responsiveness for the modern theme.

## Changes Made

- Login and signup now redirect to the dashboard only when the user has an active profile.
- Users without an active profile are sent to the profile list so they can create or activate one.
- Section order remains database-backed through `ProfileSection.order`.
- Dragging section items no longer lets content move into the wrong section type list.
- Public profile rendering now groups same-type content together, so new items appear inside their chosen section.
- The modern theme profile photo hover/glow effect was removed.
- The modern theme has tighter mobile spacing, smaller mobile avatar/header sizing, and smaller mobile cards so more content appears on screen.
- Profile owners now see add buttons on each visible section in the modern theme.
- Profile owners can add or update sections from the public profile page with a modal form.
- Owner-only public editing saves through a secure authenticated endpoint that checks profile ownership.

## Files Updated

- `accounts/views.py`
- `profiles/views.py`
- `profiles/urls.py`
- `templates/profiles/sections.html`
- `templates/profiles/themes/modern.html`

## Notes

- Save Order is stored in the database, not only in browser storage.
- The section modal reuses the same field names as the existing dashboard section form, so saved data follows the existing `ProfileSection.data` JSON structure.
- Owner-only controls are hidden from visitors and only appear when the logged-in user owns the profile being viewed.
