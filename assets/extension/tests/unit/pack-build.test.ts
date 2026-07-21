import { beforeAll, describe, expect, it } from 'vitest';
import { DOMParser as LinkedomParser } from 'linkedom';
import type { CapturePackDraft } from '../../src/shared/types';
import { buildStructuredMarkdown } from '../../src/pack/build';

beforeAll(() => {
  globalThis.DOMParser = LinkedomParser as unknown as typeof DOMParser;
});

const draft: CapturePackDraft = {
  snapshot: {
    title: 'Account Overview',
    url: 'https://example.test/account',
    language: 'en',
    description: 'Fixture',
    capturedAt: '2026-07-20T12:00:00.000Z',
    truncated: false,
    html: `<!doctype html><html><body>
      <h2>Orders</h2>
      <table><tr><th>ID</th><th>Status</th></tr><tr><td>42</td><td>Ready</td></tr></table>
      <a href="javascript:alert(1)">Unsafe link</a>
      <input aria-label="Customer" value="Andrew">
      <img alt="Chart">
    </body></html>`,
  },
  segments: [],
  pageWidth: 100,
  pageHeight: 200,
  devicePixelRatio: 2,
  captureMethod: 'full-page-scroll-stitch',
};

describe('structured Markdown', () => {
  it('preserves useful structure and removes executable URLs', () => {
    const markdown = buildStructuredMarkdown(draft);
    expect(markdown).toContain('# Account Overview');
    expect(markdown).toContain('| ID | Status |');
    expect(markdown).toContain('| 42 | Ready |');
    expect(markdown).toContain('[Customer: Andrew]');
    expect(markdown).toContain('[Image: Chart]');
    expect(markdown).not.toContain('javascript:');
  });
});
