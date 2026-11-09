
from pathlib import Path
from PIL import Image
import hashlib

ASSET_DIR = Path("Lab7")
LOGO = ASSET_DIR / "compay_logo.png"
PROFILE = ASSET_DIR / "profile.png"
PYTHON_IMG = ASSET_DIR / "python.png"
OUTPUT_DIR = Path("Lab7_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

for path in [LOGO, PROFILE, PYTHON_IMG]:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Check where you extracted Lab7.zip")
    with Image.open(path) as image:
        print(path.name, image.size, image.mode, path.stat().st_size, "bytes")

print()
print()

def sha256_file(path):
    """Calculate the SHA-256 digest of a file's exact bytes."""
    with open(path, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()

# Save baseline hashes now; we will use these values again in Part 5.
original_logo_hash = sha256_file(LOGO)
original_profile_hash = sha256_file(PROFILE)

print("Original logo SHA-256:   ", original_logo_hash)
print("Original profile SHA-256:", original_profile_hash)

print()
print()

def set_LSB(value, bit):
    """Return an integer with its least significant bit set to 0 or 1."""
    if bit not in ("0", "1"):
        raise ValueError("bit must be '0' or '1'")
    return (value & 254) if bit == "0" else (value | 1)

def get_LSB(value):
    return str(value & 1)

value = 150
for bit in ("0", "1"):
    changed = set_LSB(value, bit)
    print(value, format(value, "08b"), "→", changed, format(changed, "08b"), "LSB", get_LSB(changed))

assert set_LSB(150, "1") == 151
assert get_LSB(151) == "1"

print()
print()

value = 201
print("Original:", value, format(value, "08b"))

for bit in ("0", "1"):
    changed = set_LSB(value, bit)
    print(value, format(value, "08b"), "→", changed, format(changed, "08b"), "LSB", get_LSB(changed))

print()
print()

sample = "HI"
raw = sample.encode("utf-8")
print("Characters:", list(sample))
print("Byte values:", list(raw))
print("Bits:", " ".join(format(b, "08b") for b in raw))
print("Terminator:", format(0, "08b"))

print()
print("PART2")
print()
def max_message_bytes(width, height, channels=4, terminator_bytes=1):
    capacity_bytes = (width * height * channels) // 8
    return max(0, capacity_bytes - terminator_bytes)

print("100×100 RGBA:", max_message_bytes(100, 100, 4), "message bytes")
print("100×100 RGB:", max_message_bytes(100, 100, 3), "message bytes")

payload = "TARGET:192.168.1.50"
required_bytes = len(payload.encode("utf-8")) + 1
print("Payload + terminator:", required_bytes, "bytes")
print("Pixels needed (supplied RGBA method):", required_bytes * 2)
assert required_bytes == 20

print()
print("PART3")
print()
import sys
sys.path.insert(0, str(ASSET_DIR.resolve()))
from steganography_LSB import hide_message, extract_message

TEST_STEGO = OUTPUT_DIR / "python_test_stego.png"
hide_message(str(PYTHON_IMG), "HI", str(TEST_STEGO))
recovered = extract_message(str(TEST_STEGO))
print("Recovered:", recovered)
assert recovered == "HI"

print()
print("PART 3 B")
print()

def encode_checked(source_path, message, output_path):
    """Validate a short ASCII message, then call the supplied encoder."""
    source_path = Path(source_path)
    output_path = Path(output_path)
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    if not message:
        raise ValueError("Message must not be empty")
    if "\x00" in message:
        raise ValueError("Zero byte is reserved as a terminator")
    with Image.open(source_path) as image:
        available_pixels = image.width * image.height
    needed_pixels = 2 * (len(message.encode("utf-8")) + 1)
    if needed_pixels > available_pixels:
        raise ValueError("Message exceeds image capacity")
        raise NotImplementedError("Complete TODOs before running")
    hide_message(str(source_path), message, str(output_path))
    return output_path

LOGO_STEGO = encode_checked(LOGO, "TARGET:192.168.1.50", OUTPUT_DIR / "company_logo_stego.png")
print(LOGO_STEGO)

print()
print("PART 3 C")
print()

def decode_manual(path):
    with Image.open(path) as image:
        pixels = list(image.convert("RGBA").getdata())
    decoded_bytes = bytearray()
    for index in range(0, len(pixels) - 1, 2):
        first, second = pixels[index], pixels[index + 1]

        first_bits = "".join(str(channel & 1) for channel in first)
        second_bits = "".join(str(channel & 1) for channel in second)
        
        bits = first_bits + second_bits
        value = int(bits, 2)
        if value == 0:
            break
        decoded_bytes.append(value)
        
    return decoded_bytes.decode("utf-8")

manual_message = decode_manual(LOGO_STEGO)

reference_message = extract_message(str(LOGO_STEGO))

print("Manual message:", manual_message)
print("Reference message:", reference_message)


assert decode_manual(LOGO_STEGO) == "TARGET:192.168.1.50"
assert extract_message(str(LOGO_STEGO)) == "TARGET:192.168.1.50"

print()
print("PART4")
print()

ports = [80, 443, 3478, 5060]
port_text = ",".join(str(port) for port in ports)
port_bytes = port_text.encode("utf-8")
print("Message:", port_text)
print("Bytes:", port_bytes)
assert port_text == "80,443,3478,5060"

print()
print("PART 4 A")
print()
import stepic
with Image.open(PROFILE) as source:
     rgb_image = source.convert("RGB")
     stego_img = stepic.encode(rgb_image, port_bytes)
     profile_stego = OUTPUT_DIR / "profile_secret.png"
     stego_img.save(profile_stego, "PNG")

print("Output created:", profile_stego)

print()
print("PART 4 B")
print()
with Image.open(profile_stego) as img:
    recovered_port = stepic.decode(img)

if isinstance(recovered_port, bytes):
    recovered_port_text = recovered_port.decode("utf-8")
else:
    recovered_port_text = recovered_port

print("Recovered ports:", recovered_port_text)

assert recovered_port_text == port_text

print("Message successfully recovered")


print()
print("PART5")
print()

def compare_images(original_path, stego_path):
    with Image.open(original_path) as original, Image.open(stego_path) as stego:
        a = list(original.convert("RGBA").getdata())
        b = list(stego.convert("RGBA").getdata())
        if original.size != stego.size:
            raise ValueError("Image dimensions differ")
    changed_pixels = sum(p != q for p, q in zip(a, b))
    changed_channels = sum(x != y for p, q in zip(a, b) for x, y in zip(p, q))
    return {
        "original_bytes": Path(original_path).stat().st_size,
        "stego_bytes": Path(stego_path).stat().st_size,
        "original_sha256": sha256_file(original_path),
        "stego_sha256": sha256_file(stego_path),
        "same_file_bytes": sha256_file(original_path) == sha256_file(stego_path),
        "changed_pixels": changed_pixels,
        "changed_channels": changed_channels,
        "total_pixels": len(a),
    }

print("Reference test:", compare_images(PYTHON_IMG, TEST_STEGO))

print()
print("PART 5 A")
print()
logo_stats = compare_images(LOGO, LOGO_STEGO)
profile_stego = OUTPUT_DIR / "profile_secret.png"
profile_stats = compare_images(PROFILE, profile_stego)

print("Original logo baseline matches current original:",
     original_logo_hash == sha256_file(LOGO))
print("Original logo vs. stego identical:",
      original_logo_hash == sha256_file(LOGO_STEGO))
print("Original profile vs. stego identical:",
       original_profile_hash == sha256_file(profile_stego))

print("Logo pixel comparison:", logo_stats)
print("Logo changed pixels: %.4f%%" % (100 * logo_stats["changed_pixels"] / logo_stats["total_pixels"]) )
print("Profile pixel comparison:", profile_stats)
print("Profile changed pixels: %.4f%%" % (100 * profile_stats["changed_pixels"] / profile_stats["total_pixels"]) )

print()
print("PART 5 B")
print()

before_extract = sha256_file(LOGO_STEGO)
recovered = decode_manual(LOGO_STEGO)
after_extract = sha256_file(LOGO_STEGO)

print("Recovered message:", recovered)
print("Before extraction:", before_extract)
print("After extraction: ", after_extract)
assert before_extract == after_extract, "Extraction unexpectedly changed the file!"
assert recovered == "TARGET:192.168.1.50"

print()

before_extract = sha256_file(profile_stego)

with Image.open(profile_stego) as image:
    recovered_ports = stepic.decode(image)

if isinstance(recovered_ports, bytes):
    recovered_ports = recovered_ports.decode("utf-8")

after_extract = sha256_file(profile_stego)

print("Stepic recovered port list:", recovered_ports)
print("Stepic hash before extraction:", before_extract)
print("Stepic hash after extraction:", after_extract)

assert before_extract == after_extract

print()
print("PART 5 C")
print()

from IPython.display import display

def show_pair(original_path, stego_path):
    with Image.open(original_path) as original, Image.open(stego_path) as stego:
        print("Original:")
        display(original.copy().resize((300, 300)))
        print("Stego:")
        display(stego.copy().resize((300, 300)))

show_pair(LOGO, LOGO_STEGO)
show_pair(PROFILE, OUTPUT_DIR / "profile_secret.png")