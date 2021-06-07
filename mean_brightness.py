"""
Create a dict keyed by unicode characters of the mean brightness of those
characters. Useful for creating ascii or unicode gradients for ascii art.
"""
from itertools import chain
import json
import subprocess

FONT = "Noto-Sans-Mono-Regular"
# Grab a good sample of Unicode characters - Change the ranges to include whatever unicode characters you're interested in.
unicode_string = "".join(map(chr, chain(range(32,127), range(162,191))))

# Create a png for each character using imagemagick
for i, character in enumerate(unicode_string):
    subprocess.run([
        "convert", "-background", "black", "-fill", "white",
        "-font", FONT, "-pointsize", "72", f"label:{character}",
        f"{i}.png",
    ])

# Measure the mean brightness of each character in the png and save as a dict.
mean_brightness = { }
for i, character in enumerate(unicode_string):
    cmd = ["identify", "-format", '"%[fx:mean]"', f"{i}.png"]
    mean_brightness[character] = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

with open("meanbrightness.json", "w") as f:
    json.dump(mean_brightness, f)
