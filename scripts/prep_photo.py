from pathlib import Path
import sys
from PIL import Image,ImageOps,ImageEnhance
src=Path(sys.argv[1]) if len(sys.argv)>1 else Path("source-photo.png")
out=Path("data/source-prepped.png")
img=ImageOps.exif_transpose(Image.open(src).convert("RGB"))
gray=ImageEnhance.Sharpness(ImageEnhance.Contrast(ImageOps.grayscale(img)).enhance(2.2)).enhance(1.4)
out.parent.mkdir(exist_ok=True); gray.save(out)
