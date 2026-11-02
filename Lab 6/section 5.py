from pathlib import Path
from PIL import Image, ExifTags

image_dir = Path("Images")
print("Images found:", len(list(image_dir.glob("*.png"))))

# Activation.png

print()
print("Activation.png")

image_path = image_dir / "Activation.png" 
with Image.open(image_path) as img:
    exif = img.getexif()
    print("EXIF tags:", len(exif))
    for tag_id, value in exif.items():
        print(ExifTags.TAGS.get(tag_id, tag_id), ":", value)
    xmp = img.info.get("XML:com.adobe.xmp") or img.info.get("xmp")
    if isinstance(xmp, bytes):
        xmp = xmp.decode("utf-8", errors="replace")
    print(xmp if xmp else "No XMP found")

    exif_details = exif.get_ifd(34665)
    raw_comment = exif_details.get(37510)
    print( repr(raw_comment))
    if isinstance(raw_comment, bytes):
            message = raw_comment[8:].decode(
                "utf-8",
                errors="replace"
            )
            print(message)

print()
print()
print("Brain-Chemicals.png")

# Brain-Chemicals.png

image_path = image_dir / "Brain-Channel.png"
with Image.open(image_path) as img:
    exif = img.getexif()
    print("EXIF tags:", len(exif))
    for tag_id, value in exif.items():
        print(ExifTags.TAGS.get(tag_id, tag_id), ":", value)
    print(ExifTags.TAGS.get(tag_id, tag_id), ":", value)
    if  ExifTags.TAGS.get(tag_id, tag_id) == "ImageDescription":
                    print("Field:", ExifTags.TAGS.get(tag_id, tag_id))
                    print("Partial secret:", value)
    xmp = img.info.get("XML:com.adobe.xmp") or img.info.get("xmp")
    if isinstance(xmp, bytes):
        xmp = xmp.decode("utf-8", errors="replace")
    print(xmp if xmp else "No XMP found")

print()
print()
print("Brain.png")

# Brain.png

image_path = image_dir / "Brain.png" # or Chemicals.png
with Image.open(image_path) as img:
    for key, value in img.info.items():
        if isinstance(value, str):
            print(key, ":", value)

print()
print()
print("Chemicals.png")

# Chemicals.png

image_path = image_dir / "Chemicals.png"
with Image.open(image_path) as img:
    for key, value in img.info.items():
        if isinstance(value, str):
            print(key, ":", value)

print()
print()
print("Dopamine.png")

# Dopamine.png

image_path = image_dir / "Dopamine.png"
with Image.open(image_path) as img:
    xmp = img.info.get("XML:com.adobe.xmp") or img.info.get("xmp")
    if isinstance(xmp, bytes):
        xmp = xmp.decode("utf-8", errors="replace")
    print(xmp if xmp else "No XMP found")

print()
print()
print("Music.png")

# Music.png

import base64

image_path = image_dir / "Music.png"
with Image.open(image_path) as img:
    exif = img.getexif()
    for tag_id, value in exif.items():
        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
        if ExifTags.TAGS.get(tag_id, tag_id) == "Copyright":
            print("Encoded value:", value)
            
            decoded = base64.b64decode(value).decode("utf-8")
            print("Partial secret:", decoded)

print()