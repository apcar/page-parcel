// Generates the extension icons (16/48/128 px) from a single SVG source.
// Run with: npm run icons
import sharp from 'sharp';
import { mkdir } from 'node:fs/promises';

const outDir = 'public/icons';

/**
 * A page wrapped with a parcel band on a deep-blue gradient square.
 * The silhouette remains legible at Chrome's smallest icon size.
 */
function svg() {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#071426"/>
      <stop offset="1" stop-color="#174781"/>
    </linearGradient>
  </defs>
  <rect x="6" y="6" width="116" height="116" rx="28" fill="url(#bg)"/>
  <rect x="36" y="22" width="56" height="84" rx="10" fill="#ffffff"/>
  <path d="M72 22h10a10 10 0 0 1 10 10v13H72z" fill="#B8D7F0"/>
  <path d="M72 22l20 23H78a6 6 0 0 1-6-6z" fill="#DCEAF8"/>
  <rect x="29" y="57" width="70" height="28" rx="7" fill="#38BDF8"/>
  <path d="M58 57v28M70 57v28" stroke="#0B2447" stroke-width="4" opacity="0.62"/>
</svg>`;
}

await mkdir(outDir, { recursive: true });

for (const size of [16, 48, 128]) {
  await sharp(Buffer.from(svg())).png().toFile(`${outDir}/icon${size}.png`);
  console.log(`✓ generated ${outDir}/icon${size}.png`);
}

console.log('Icons generated.');
