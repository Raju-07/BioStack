# Profile and Section Ordering Changes

## Summary

This update improves profile activation, section ordering, and the modern public profile theme.

## Changes Made

- Auto-selects the only available profile as the active profile on the `profiles: list` route.
- Keeps the last selected active profile when multiple profiles exist.
- Ignores stale active-profile session IDs instead of failing.
- Stops section/group drag actions from saving automatically.
- Adds a `Save Order` button on the profile sections page so order changes are stored only when confirmed.
- Removes browser `localStorage` ordering from the section manager to prevent unexpected reshuffling.
- Appends newly created sections after existing sections instead of giving them the default first position.
- Restores the saved database order when the section manager loads.
- Fixes the modern theme personal-details hide action so collapsed content releases its layout space.
- Adds show more/show less behavior to the modern theme skills section.

## Performance Improvements

- Uses the active-profile helper to avoid repeated missing-session failures.
- Saves only changed profile fields for theme fallback and profile image updates.
- Uses a single filtered query plus `bulk_update()` for section order persistence.
- Fetches public profile data with `select_related()` for user, user details, and theme in one profile query.
- Limits public section fields to the values needed for rendering.

## Files Updated

- `profiles/utils.py`
- `profiles/views.py`
- `templates/profiles/sections.html`
- `templates/profiles/themes/modern.html`

## Notes

The existing `ProfileSection.order` database field is reused, so no new migration is required for these changes.
