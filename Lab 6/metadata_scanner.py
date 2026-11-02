from pathlib import Path
from PIL import Image, ExifTags

import csv, base64
results = []

image_dir = Path("Images")
print("Images found:", len(list(image_dir.glob("*.png"))))


keywords = ("RECON", "VULN", "EXPLOIT", "PERSIST", "LATERAL", "EXFIL")


for image_path in sorted(image_dir.glob("*.png")):
    with Image.open(image_path) as img:
        print(image_path.name, "→", img.format, "| fields:", len(img.info))


for image_path in sorted(image_dir.glob("*.png")):
    with Image.open(image_path) as img:
        result = {
            "filename": image_path.name,
            "format": img.format,
            "metadata_fields": ", ".join(img.info.keys()),
            "suspected_field": "",    # TODO: identify relevant EXIF, PNG, or XMP field
            "encoding": "",           # TODO: indicate Base64, plain text, etc.
            "risk_score": 0,          # TODO: apply and justify your scoring rules
            "reason": "",             # TODO: explain evidence for this score
        }


        suspected_field = ""
        encoding_type = "Plain text"
        risk_score = 0
        reasons = []


        exif = img.getexif()
        if exif:
            for tag_id, value in exif.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                if tag_name in ["ImageDescription", "Copyright"]:
                    suspected_field = f"EXIF:{tag_name}"
                    risk_score += 10
                    reasons.append(f"EXIF field '{tag_name}' found (+10)")

            try:
                exif_details = exif.get_ifd(34665)
                raw_comment = exif_details.get(37510)
                if raw_comment:
                    suspected_field = "EXIF: UserComment"
                    risk_score += 10
                    reasons.append("EXIF field 'UserComment' found (+10)")
            except Exception:
                pass

        
        for key, value in img.info.items():
            if isinstance(value, str) and key not in ["xmp", "XML:com.adobe.xmp"]:
                if not suspected_field:
                    suspected_field = f"PNG:{key}"
                    risk_score += 10
                    reasons.append(f"PNG text field '{key}' found (+10)")


        xmp = img.info.get("XML:com.adobe.xmp") or img.info.get("xmp")
        if isinstance(xmp, bytes):
            xmp = xmp.decode("utf-8", errors="replace")
        if xmp and not suspected_field:
            suspected_field = "XMP metadata"
            risk_score += 10
            reasons.append("XMP metadata found (+10)")


        if suspected_field and "Music" in image_path.name:
            encoding_type = "Base64"
            risk_score += 5
            reasons.append("Base64 encoded value requiring investigation (+5)")


        if risk_score == 0:
            reasons.append("No anomalies detected.")

        results.append({
            "filename": image_path.name,
            "format": img.format,
            "metadata_fields": ", ".join(img.info.keys()),
            "suspected_field": suspected_field or "None",
            "encoding": encoding_type,
            "risk_score": risk_score,
            "reason": " | ".join(reasons) if reasons else "No anomalies detected."
        })

        print(result)


with open("metadata_report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Saved", len(results), "rows to metadata_report.csv")