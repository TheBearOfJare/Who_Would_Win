from PIL import Image
import glob, os

for infile in glob.glob("uploads/photos/champions/*.jpeg"):
    file, ext = os.path.splitext(infile)
    print(file)
    im = Image.open(infile).convert("RGB")
    im.save(file + ".webp", "webp")