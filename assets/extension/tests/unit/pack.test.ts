import { describe, expect, it } from 'vitest';
import { computeImageSegments, safeFileStem } from '../../src/shared/pack';

describe('computeImageSegments', () => {
  it('keeps bounded pages in one image', () => {
    expect(computeImageSegments(1200, 24000)).toEqual([{ startY: 0, height: 1200 }]);
  });

  it('splits tall pages without gaps or overlap', () => {
    expect(computeImageSegments(50001, 24000)).toEqual([
      { startY: 0, height: 24000 },
      { startY: 24000, height: 24000 },
      { startY: 48000, height: 2001 },
    ]);
  });

  it('rejects an invalid segment height', () => {
    expect(() => computeImageSegments(10, 0)).toThrow('maxHeight must be positive');
  });
});

describe('safeFileStem', () => {
  it('removes filename metacharacters and bounds length', () => {
    expect(safeFileStem('  A / B: report?  ')).toBe('A _ B_ report_');
    expect(safeFileStem('line\u0000break\u001f')).toBe('line_break_');
    expect(safeFileStem('x'.repeat(100))).toHaveLength(80);
  });
});
