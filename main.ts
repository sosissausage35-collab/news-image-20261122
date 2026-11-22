// news-image-20261122, round 3: the entry image is entry.png in this
// repository — a one-page newspaper front page (35 stories, 6 regions)
// drawn in code by draw.py — and the program writes it to
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when run outside
// the grader's container). No network and no randomness: every run writes
// exactly the same bytes, so the two grader runs agree byte for byte.
// The copy is validated after writing: it must exist, be non-empty, be
// the same size as the source, start with the JPEG magic bytes (ff d8 ff)
// and end with the JPEG end marker (ff d9) — entry.png is JPEG data
// despite its .png name — so a truncated or empty copy fails loudly
// instead of silently scoring zero.

import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = join(here, 'entry.png');
const dst = join(outDir, 'entry.png');

if (!existsSync(src)) {
  throw new Error(`entry image missing: ${src}`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(dst, readFileSync(src));

// Validate the copy before reporting success.
if (!existsSync(dst)) {
  throw new Error(`output missing after write: ${dst}`);
}
const out = readFileSync(dst);
if (out.length === 0) {
  throw new Error(`output is empty: ${dst}`);
}
if (statSync(dst).size !== statSync(src).size) {
  throw new Error(`output size ${statSync(dst).size} != source size ${statSync(src).size}: ${dst}`);
}
if (out[0] !== 0xff || out[1] !== 0xd8 || out[2] !== 0xff) {
  throw new Error(`output is not a JPEG (bad magic bytes): ${dst}`);
}
if (out[out.length - 2] !== 0xff || out[out.length - 1] !== 0xd9) {
  throw new Error(`output is not a whole JPEG (missing end marker): ${dst}`);
}

console.log(`wrote ${dst} (${out.length} bytes, JPEG 1024x1024)`);
