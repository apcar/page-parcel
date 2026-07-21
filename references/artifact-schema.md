# Trace Bundle schema 1.0

Every PageParcel ZIP contains:

- `page.md`: structured Markdown preserving headings, lists, links, tables, labels, buttons, and captured form state where safe.
- `page-reader.md`: a lower-clutter narrative extraction produced locally with Defuddle in synchronous mode.
- `page.json`: source context, capture geometry, security markers, artifact sizes, and SHA-256 hashes.
- `page.png`, or `page-001.png` through `page-NNN.png`: lossless vertical screenshot segments. A page is segmented when one PNG would exceed the bounded canvas height.

No raw HTML is included.

`page.json` uses `schema_version: "1.0"` and records:

- generator name and extension version;
- capture timestamp, source URL, title, language, and description;
- capture method, pixel dimensions, device pixel ratio, segment count, and whether the DOM snapshot was truncated;
- local-only and redaction security markers;
- byte length and SHA-256 for every Markdown and PNG artifact.

The JSON file does not hash itself, avoiding a recursive manifest.

## Integrity boundary

The registered hashes detect whether bundled artifacts changed after construction. They do not provide an independent trusted timestamp, cryptographic signature, or external proof that the source URL served the captured content.
