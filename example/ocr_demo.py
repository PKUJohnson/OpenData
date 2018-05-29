# encoding: utf-8

import tesserocr
from tesserocr import PyTessBaseAPI

from PIL import Image

img1 = Image.open('report.jpg')
code = tesserocr.image_to_text(img1, lang="chi_sim")
print(code.replace(" ", ""))
