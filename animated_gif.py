"""
To stitch `png`s into an animated gif (assumes pngs should be ordered by name):
"""
import imageio
from pathlib import Path

png_dir = Path('your png directory')
images = [imageio.imread(png_dir / file_name) for file_name in sorted(png_dir.iterdir()) if file_name.suffix == '.png']
imageio.mimsave(png_dir / 'title.gif', images, duration = .1)
