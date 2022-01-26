#!/usr/bin/env python3
from PIL import Image

im = Image.open('images/png_test')
im = im.convert('RGB')
im.resize((128, 128)).rotate((90)).save('images_main/test_result.jpg')
