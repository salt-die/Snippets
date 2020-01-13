# -*- coding: utf-8 -*-
"""
Often I generate a large number of numbered pngs, e.g., 000.png, 001.png...,
that I want to stitch together into an animated gif.  This code does that.
"""
import os
import imageio

png_dir = 'your png directory'
images = [imageio.imread(os.path.join(png_dir, file_name))
          for file_name in sorted(os.listdir(png_dir))
          if file_name.endswith('.png')]
imageio.mimsave(png_dir + 'title.gif', images, duration = .1)

