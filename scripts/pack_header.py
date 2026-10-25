# After: npm install sharp && node scripts/render_header.cjs
# Requires Pillow: python3 -m pip install Pillow
from pathlib import Path
from PIL import Image
root = Path(__file__).resolve().parents[1]
frames = [Image.open(p).convert('RGB') for p in sorted((root / 'frames').glob('*.png'))]
if not frames:
    raise RuntimeError('Run node scripts/render_header.cjs first')
palette = frames[0].quantize(colors=128)
frames = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
frames[0].save(root / 'assets/header.gif', save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=False)
