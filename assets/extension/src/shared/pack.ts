export interface ImageSegment {
  startY: number;
  height: number;
}

export const MAX_SEGMENT_HEIGHT_PX = 24_000;
export const MAX_BUNDLE_HEIGHT_PX = 160_000;

export function computeImageSegments(
  totalHeight: number,
  maxHeight = MAX_SEGMENT_HEIGHT_PX,
): ImageSegment[] {
  if (!Number.isFinite(totalHeight) || totalHeight <= 0) return [];
  if (!Number.isFinite(maxHeight) || maxHeight <= 0) throw new Error('maxHeight must be positive');
  const segments: ImageSegment[] = [];
  for (let startY = 0; startY < totalHeight; startY += maxHeight) {
    segments.push({ startY, height: Math.min(maxHeight, totalHeight - startY) });
  }
  return segments;
}

export function safeFileStem(value: string): string {
  const cleaned = value
    .normalize('NFKC')
    .replace(/[\\/:*?"<>|]/g, '_')
    .split('')
    .map((character) => (character.charCodeAt(0) <= 31 ? '_' : character))
    .join('')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 80);
  return cleaned || 'capture';
}

export function hex(bytes: ArrayBuffer): string {
  return Array.from(new Uint8Array(bytes), (b) => b.toString(16).padStart(2, '0')).join('');
}

export async function sha256(data: Uint8Array): Promise<string> {
  const copied = new Uint8Array(data);
  return hex(await crypto.subtle.digest('SHA-256', copied.buffer));
}
