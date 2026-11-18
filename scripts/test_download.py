import os
import requests
from io import BytesIO
from PIL import Image

headers = {'User-Agent': 'RajasthanRoyalsResearch/1.0 (cricket@royals.com)'}

url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/2018.02.03.22.38.28-Glenn_Maxwell-0003_%2825557926667%29_%28cropped%29.jpg"
res = requests.get(url, headers=headers, timeout=15)
img = Image.open(BytesIO(res.content))
print(f"Original size: {img.size}, mode: {img.mode}")

# Resize to max 800px wide
if img.width > 800:
    ratio = 800.0 / img.width
    new_h = int(img.height * ratio)
    img = img.resize((800, new_h), Image.Resampling.LANCZOS)
    print(f"Resized size: {img.size}")

if img.mode != 'RGB':
    img = img.convert('RGB')

out_path = os.path.join("public", "img", "players", "glenn-maxwell.jpg")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
img.save(out_path, "JPEG", quality=85)
print(f"Saved to {out_path} (size: {os.path.getsize(out_path)} bytes)")

