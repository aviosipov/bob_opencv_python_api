

import subprocess
t = subprocess.check_output(["C:\\Program Files (x86)\\ZBar\\bin\\zbarimg","-q",     "images/qr.png"])
print t



try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract



tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'


img = Image.open('E:\\python_projects\\opencv_python_api\\images\\text_tris.jpg')
img.load()

#print(pytesseract.image_to_string(img))  # 'eng' for english

tt= pytesseract.image_to_string(img,lang='eng', config=tessdata_dir_config)
print tt

