// news-image-20261122: the entry image is entry.png in this repository, and the
// program writes it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when
// run outside the grader's container). No network and no randomness: every run
// writes exactly the same bytes, so the two grader runs agree byte for byte.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), readFileSync(join(here, 'entry.png')));
