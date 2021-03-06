# -*- coding: utf-8 -*-
import subprocess
import json
"""
Create a dict keyed by unicode characters of the mean brightness of those
characters. Useful for creating ascii or unicode gradients for ascii art.
"""
font = "Noto-Sans-Mono-Regular"
#Grab a good sample of Unicode characters - Change the ranges to include 
#whatever unicode characters you're interested in.
unicodestring = "".join([chr(s) for s in range(32,127)]) + \
                "".join([chr(s) for s in range(162,191)])

#Create a png for each character using imagemagick
for i,character in enumerate(unicodestring):
    subprocess.run(["convert", "-background","black", "-fill","white", \
                    "-font", font, "-pointsize","72",\
                    "label:"+character, f"{i}.png"])

#Measure the mean brightness of each character in the png and save as a dict.
#Brightness is measured with imagemagick.
meanbrightness = {}
for i, character in enumerate(unicodestring):
    cmd = ["identify", "-format", "\"%[fx:mean]\"", f"{i}.png"]
    meanbrightness[character]=subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

brightjson = json.dumps(meanbrightness)
with open("meanbrightness.json","w") as f:
    f.write(brightjson)
