# Security contract

PageParcel is a local-first, explicitly invoked browser extension.

## Invariants

- Manifest V3.
- Permissions are limited to `activeTab`, `scripting`, `storage`, `unlimitedStorage`, and `downloads`.
- `host_permissions` is empty. Access to a page begins only after the user invokes the extension.
- Extension CSP permits scripts and connections only to the extension itself. It forbids objects, frames, media, inline script, and `unsafe-eval`.
- No analytics, telemetry, remote logging, upload service, remote PDF service, or hosted screenshot viewer.
- No `chrome.storage.sync`. Pending capture data uses local extension storage and is deleted after ZIP construction.
- Defuddle is invoked synchronously with `useAsync: false`. Do not call `parseAsync` or `fetchAsyncVariables`.
- Page image sources are removed from the captured DOM before Markdown generation. The extension must not fetch remote page assets.
- Script, style, embedded object, iframe HTML, event attributes, and executable raw HTML are excluded from the ZIP.
- Password fields and fields whose descriptors resemble secrets, tokens, authorization, API keys, or payment cards are redacted from Markdown. This does not redact the visual screenshot.
- ZIPs are downloaded locally. No bundle is sent anywhere by the extension.

## Required gate

Run `python3 scripts/security_audit.py assets/extension` after code changes. A failed audit blocks installation.

Any change to permissions, host access, CSP, networking, or data retention requires an explicit security review before release.
