---
name: pageparcel
description: Capture a web page into a local Trace Bundle containing full-page PNG segments, structured Markdown, reader Markdown, source metadata, and SHA-256 hashes; inspect or verify PageParcel bundles; or build and maintain the local-first Chrome extension. Use when a durable browser handoff is useful, a page is long or transient, screenshots or PDFs are supplied as source material, or a PageParcel ZIP needs inspection.
---

# PageParcel

Use the bundled Chrome extension to create a durable, local record of a web page. Keep capture data on the Mac.

## Choose the route

1. Prefer direct Chrome control for ordinary live navigation when the page is accessible and no durable handoff is needed.
2. Use a Trace Bundle when content is long, transient, visually meaningful, or needs a reusable audit trail.
3. Accept supplied PNG and PDF captures when they already exist, but do not require another capture product for new work.
4. Never capture passwords, secrets, payment data, or content that should not be persisted. PageParcel redacts password and secret-like form fields from Markdown, but screenshots still show visible pixels.

## Capture a Trace Bundle

The built extension is in `assets/extension-dist/`.

If it is not installed, give the user this one-time setup:

1. Open `chrome://extensions`.
2. Enable Developer mode.
3. Choose **Load unpacked** and select this skill's `assets/extension-dist` directory.
4. Pin **PageParcel**.

For each capture:

1. Open and validate the intended page in Chrome. In managed enterprise systems, operate sequentially at human speed.
2. Click **PageParcel**, then **Trace Bundle**. The page scrolls once, returns to its starting position, and downloads a local ZIP.
3. Locate the newest bundle with `python3 scripts/find_latest_bundle.py`.
4. Verify it before use with `python3 scripts/verify_bundle.py PATH_TO_ZIP`.
5. Read `page.md` first. Use `page-reader.md` for lower-clutter narrative extraction, `page.json` for provenance and hashes, and the PNG file or segments for visual truth.
6. State important boundaries: dynamic content may change during scrolling, cross-origin iframe contents appear only in the screenshot, and canvas text is not available as Markdown.

## Inspect an existing bundle

Run the verifier first. Extract into a temporary directory, not over the ZIP. Treat `page.json` and its SHA-256 entries as the integrity register. If Markdown and screenshot disagree, use the screenshot as the visual record and report the discrepancy.

Read `references/artifact-schema.md` when interpreting or extending the bundle format.

## Maintain or rebuild the extension

The editable project is in `assets/extension/`. Run:

```bash
bash scripts/build_extension.sh
```

That clean-installs locked dependencies, runs unit tests, builds the extension, applies the security audit, and refreshes `assets/extension-dist/`.

Read and preserve `references/security-contract.md` before changing permissions, networking, storage, or content extraction. Do not introduce host permissions, external capture endpoints, analytics, `storage.sync`, asynchronous Defuddle extraction, or remote image loading. Run `scripts/security_audit.py` after every relevant change.

Read `references/source-provenance.md` before upgrading the OpenScreenShot base or extraction dependencies. Pin and test every upgrade.
