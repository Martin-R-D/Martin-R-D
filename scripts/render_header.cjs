// Requires sharp (npm install sharp). Render SVG motion into PNG frames.
const fs = require('fs');
const path = require('path');
const sharp = require(require.resolve('sharp', {paths: [process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES || process.cwd()]}));
const root = path.resolve(__dirname, '..');
const svg = fs.readFileSync(path.join(root, 'assets/header.svg'), 'utf8').replace(/<style>[\s\S]*?<\/style>/, '');
const dir = path.join(root, 'frames');
fs.mkdirSync(dir, {recursive: true});
(async () => {
 for (let i=0; i<84; i++) {
  const frame = svg.replace('class="satellite"', `transform="rotate(${i*360/84})"`).replace('class="orbit-ring"', `transform="rotate(${-i*360/84})"`);
  await sharp(Buffer.from(frame)).png().toFile(path.join(dir, `${String(i).padStart(3,'0')}.png`));
 }
})();
