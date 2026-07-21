# Source provenance

PageParcel 0.2.0 is a pinned local-first fork of OpenScreenShot at commit `7c8a2a9`, retained under its MIT license.

Direct runtime components:

- OpenScreenShot capture and editor base, MIT.
- Defuddle 0.19.1, MIT. Used only through synchronous `parse()` with `useAsync: false`.
- Turndown 7.2.4, MIT.
- fflate 0.8.3, MIT.
- Preact, MIT, inherited from the base.

The extension source retains the upstream `LICENSE` and adds `THIRD_PARTY_NOTICES.md`. Dependency versions are locked in `package-lock.json`. Re-run unit tests, build, audit, and manual capture checks before accepting upgrades.
