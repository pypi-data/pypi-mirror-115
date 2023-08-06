from generator import *
from font import *

g = Generator()

img=g.generate_from_string('Самарская',FONT_PATH='C:\projects\OCR\generator\handwritting_generator\content\werner40.ttf')
img.save('text1.png')
img=g.generate_from_string('Свердлов',FONT_PATH='C:\projects\OCR\generator\handwritting_generator\content\werner40.ttf')
img.save('text2.png')
img=g.generate_from_string('Юдин',FONT_PATH='C:\projects\OCR\generator\handwritting_generator\content\werner40.ttf')
img.save('text3.png')