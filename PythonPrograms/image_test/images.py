#!/usr/bin/env python3

import os
import re
from PIL import Image
import subprocess

files = os.listdir('images')

for file in files:
	filename = ('images/' + file)
	new_file = ('images_main/' + file)
	im = Image.open(filename)
	im = im.convert('RGB')
	im.rotate((90)).resize((128, 128)).save(new_file, 'jpeg')
