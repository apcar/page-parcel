# Contributing to PageParcel

Thank you for helping make web captures more portable, inspectable, and private by default.

## Before opening a change

1. Open an issue or discussion for changes that affect permissions, networking, storage, bundle structure, or extraction behavior.
2. Keep the permission surface narrow. PageParcel must remain explicitly invoked and active-tab only.
3. Preserve source attribution and third-party notices.

## Development setup

PageParcel uses Node.js 22, npm, and Python 3.

```bash
cd assets/extension
npm ci
npm test
npm run build
cd ../..
python3 scripts/security_audit.py assets/extension
python3 scripts/verify_bundle.py --self-test
```

Run `bash scripts/build_extension.sh` to execute the full gate and refresh the checked-in unpacked extension.

## Pull requests

- Keep changes focused and explain the user-facing behavior.
- Add or update tests for logic changes.
- Include manual capture notes for UI, scrolling, extraction, or export changes.
- Do not add analytics, telemetry, remote capture, remote image loading, sync storage, or broad host permissions.
- Update the bundle schema and verifier together when changing artifact structure.

## Security-sensitive changes

Changes to permissions, CSP, networking, data retention, redaction, DOM sanitization, or archive construction need explicit security review. The automated audit is a minimum gate, not a substitute for review.
