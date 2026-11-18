import os
import re
import json
import requests
from io import BytesIO
from PIL import Image

HEADERS = {'User-Agent': 'RajasthanRoyalsResearch/1.0 (cricket-analytics@royals.com)'}

PLAYERS = [
    # Top 10 Batters
    {
        "name": "Vaibhav Sooryavanshi",
        "slug": "vaibhav-sooryavanshi",
        "initials": "VS",
        "role": "Opening Batter",
        "team": "Rajasthan Royals",
        "commons_file": None, # Only GODL-India group photo exists; strictly rejected per license whitelist
        "fallback_reason": "No CC0/CC-BY/CC-BY-SA portrait on Commons (only non-whitelisted GODL group photo)"
    },
    {
        "name": "Ashutosh Sharma",
        "slug": "ashutosh-sharma",
        "initials": "AS",
        "role": "Finisher / Batter",
        "team": "Delhi Capitals",
        "commons_file": None,
        "fallback_reason": "No cricketer portrait on Commons (only namesake professor/government secretary)"
    },
    {
        "name": "Reeza Hendricks",
        "slug": "reeza-hendricks",
        "initials": "RH",
        "role": "Opening Batter",
        "team": "South Africa",
        "commons_file": "File:REEZA HENDRICKS (15519916117).jpg",
        "fallback_reason": None
    },
    {
        "name": "Glenn Maxwell",
        "slug": "glenn-maxwell",
        "initials": "GM",
        "role": "All-Rounder",
        "team": "Australia",
        "commons_file": "File:2018.02.03.22.38.28-Glenn Maxwell-0003 (25557926667) (cropped).jpg",
        "fallback_reason": None
    },
    {
        "name": "Shubham Dubey",
        "slug": "shubham-dubey",
        "initials": "SD",
        "role": "Middle-Order Batter",
        "team": "Rajasthan Royals",
        "commons_file": None,
        "fallback_reason": "No photo available on Wikimedia Commons"
    },
    {
        "name": "Dinesh Karthik",
        "slug": "dinesh-karthik",
        "initials": "DK",
        "role": "Wicketkeeper Finisher",
        "team": "RCB (Retired)",
        "commons_file": "File:Dinesh.Karthik.jpg",
        "fallback_reason": None
    },
    {
        "name": "Riyan Parag",
        "slug": "riyan-parag",
        "initials": "RP",
        "role": "Middle-Order Batter",
        "team": "Rajasthan Royals",
        "commons_file": None,
        "fallback_reason": "No freely licensed photo available on Wikimedia Commons"
    },
    {
        "name": "Travis Head",
        "slug": "travis-head",
        "initials": "TH",
        "role": "Opening Batter",
        "team": "Australia / SRH",
        "commons_file": "File:Travis Head bowling at Perth Stadium, First Test Australia versus West Indies, 2 December 2022 01.jpg",
        "fallback_reason": None
    },
    {
        "name": "Tim David",
        "slug": "tim-david",
        "initials": "TD",
        "role": "Finisher",
        "team": "Australia",
        "commons_file": None,
        "fallback_reason": "No freely licensed cricketer portrait on Commons"
    },
    {
        "name": "David Miller",
        "slug": "david-miller",
        "initials": "DM",
        "role": "Finisher",
        "team": "South Africa",
        "commons_file": "File:DAVID MILLER (15085495183).jpg",
        "fallback_reason": None
    },

    # Top 10 Bowlers
    {
        "name": "Sufiyan Muqeem",
        "slug": "sufiyan-muqeem",
        "initials": "SM",
        "role": "Wrist Spinner",
        "team": "Pakistan",
        "commons_file": None,
        "fallback_reason": "No photo available on Wikimedia Commons"
    },
    {
        "name": "Jamie Overton",
        "slug": "jamie-overton",
        "initials": "JO",
        "role": "Fast-Bowling All-Rounder",
        "team": "England / CSK",
        "commons_file": "File:Jamie Overton Surrey.jpg",
        "fallback_reason": None
    },
    {
        "name": "Abrar Ahmed",
        "slug": "abrar-ahmed",
        "initials": "AA",
        "role": "Leg Spinner",
        "team": "Pakistan",
        "commons_file": "File:Abrar Ahmed bowling 2023 (cropped).jpg",
        "fallback_reason": None
    },
    {
        "name": "Matheesha Pathirana",
        "slug": "matheesha-pathirana",
        "initials": "MP",
        "role": "Fast Bowler",
        "team": "Sri Lanka / CSK",
        "commons_file": None,
        "fallback_reason": "No freely licensed photo available on Wikimedia Commons"
    },
    {
        "name": "Blessing Muzarabani",
        "slug": "blessing-muzarabani",
        "initials": "BM",
        "role": "Fast Bowler",
        "team": "Zimbabwe",
        "commons_file": "File:PCC XI v Zimbabwe 2025 06.jpg",
        "fallback_reason": None
    },
    {
        "name": "Mohammad Rishad Hossain",
        "slug": "mohammad-rishad-hossain",
        "initials": "RH",
        "role": "Leg-Spin All-Rounder",
        "team": "Bangladesh",
        "commons_file": "File:Rishad Hossain, 2025-02-08 Fortune Barishal BPL 2025 Champions Trophy Presentation Dhaka (PID-0003668) (cropped).jpg",
        "fallback_reason": None
    },
    {
        "name": "Shaheen Afridi",
        "slug": "shaheen-afridi",
        "initials": "SA",
        "role": "Fast Bowler",
        "team": "Pakistan",
        "commons_file": "File:Shaheen Afridi.jpg",
        "fallback_reason": None
    },
    {
        "name": "Gerald Coetzee",
        "slug": "gerald-coetzee",
        "initials": "GC",
        "role": "Fast Bowler",
        "team": "South Africa",
        "commons_file": "File:RSA vs AUS Day 2 - Gerald Coetzee.jpg",
        "fallback_reason": None
    },
    {
        "name": "Anshul Kamboj",
        "slug": "anshul-kamboj",
        "initials": "AK",
        "role": "Medium-Fast Bowler",
        "team": "India / CSK / MI",
        "commons_file": None,
        "fallback_reason": "No photo available on Wikimedia Commons"
    },
    {
        "name": "Mohammad Nawaz",
        "slug": "mohammad-nawaz",
        "initials": "MN",
        "role": "Spin All-Rounder",
        "team": "Pakistan",
        "commons_file": None,
        "fallback_reason": "No freely licensed cricketer portrait on Commons"
    }
]

BACKGROUNDS = [
    {
        "slug": "sawai-mansingh-stadium",
        "title": "Sawai Mansingh Stadium, Jaipur",
        "commons_file": "File:Sawai-Mansingh-Stadium-Jaipur.jpg",
        "max_width": 1920
    },
    {
        "slug": "chand-baori-stepwell",
        "title": "Chand Baori Stepwell, Rajasthan",
        "commons_file": "File:Chand Baori, Abhaneri 13 stories.jpg",
        "max_width": 1920
    },
    {
        "slug": "hawa-mahal-jaipur",
        "title": "Hawa Mahal, Jaipur",
        "commons_file": "File:East facade Hawa Mahal Jaipur from ground level (July 2022) - img 01.jpg",
        "max_width": 1920
    }
]

def clean_html(raw_html):
    if not raw_html:
        return "Unknown"
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def get_commons_info(file_title):
    params = {
        'action': 'query',
        'format': 'json',
        'titles': file_title,
        'prop': 'imageinfo',
        'iiprop': 'url|size|extmetadata'
    }
    r = requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=HEADERS, timeout=15)
    data = r.json()
    pages = data.get('query', {}).get('pages', {})
    for pid, p in pages.items():
        if 'imageinfo' in p and len(p['imageinfo']) > 0:
            ii = p['imageinfo'][0]
            meta = ii.get('extmetadata', {})
            author = clean_html(meta.get('Artist', {}).get('value', 'Unknown'))
            lic = meta.get('LicenseShortName', {}).get('value', 'Unknown')
            url = ii.get('url')
            desc_url = ii.get('descriptionurl', f"https://commons.wikimedia.org/wiki/{file_title}")
            return {
                "url": url,
                "author": author,
                "license": lic,
                "source_url": desc_url
            }
    return None

def download_and_resize(img_url, out_path, max_width=800):
    res = requests.get(img_url, headers=HEADERS, timeout=25)
    img = Image.open(BytesIO(res.content))
    if img.width > max_width:
        ratio = max_width / float(img.width)
        new_h = int(img.height * ratio)
        img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "JPEG", quality=88)
    print(f"Downloaded & resized to {out_path} ({img.size[0]}x{img.size[1]})")

def generate_svg_monogram(slug, initials, full_name, role, out_path):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" height="800">
  <defs>
    <!-- Dark Navy to RR Pink Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B1E" />
      <stop offset="50%" stop-color="#0B133A" />
      <stop offset="100%" stop-color="#280826" />
    </linearGradient>
    
    <!-- Gold Metallic Gradient -->
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE27A" />
      <stop offset="35%" stop-color="#D4AF37" />
      <stop offset="70%" stop-color="#997A1E" />
      <stop offset="100%" stop-color="#D4AF37" />
    </linearGradient>

    <!-- RR Pink Radial Glow -->
    <radialGradient id="pinkGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#EA1A85" stop-opacity="0.35" />
      <stop offset="70%" stop-color="#EA1A85" stop-opacity="0.05" />
      <stop offset="100%" stop-color="#EA1A85" stop-opacity="0" />
    </radialGradient>
    
    <!-- Text Gold Gradient -->
    <linearGradient id="textGold" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="60%" stop-color="#FFDE82" />
      <stop offset="100%" stop-color="#D4AF37" />
    </linearGradient>
  </defs>

  <!-- Deep Canvas -->
  <rect width="800" height="800" fill="url(#bgGrad)" />

  <!-- Radial Pink Ambience -->
  <circle cx="400" cy="380" r="320" fill="url(#pinkGlow)" />

  <!-- Concentric Stepwell Line Patterns -->
  <g opacity="0.12" stroke="#D4AF37" stroke-width="1.5" fill="none">
    <rect x="40" y="40" width="720" height="720" />
    <rect x="70" y="70" width="660" height="660" />
    <rect x="100" y="100" width="600" height="600" />
    <line x1="40" y1="40" x2="100" y2="100" />
    <line x1="760" y1="40" x2="700" y2="100" />
    <line x1="40" y1="760" x2="100" y2="700" />
    <line x1="760" y1="760" x2="700" y2="700" />
  </g>

  <!-- Outer Fine Gold Frame -->
  <rect x="30" y="30" width="740" height="740" fill="none" stroke="url(#goldGrad)" stroke-width="2" rx="4" />
  <rect x="38" y="38" width="724" height="724" fill="none" stroke="#EA1A85" stroke-width="1" opacity="0.6" rx="2" />

  <!-- Corner Rajasthani Diamond Accents -->
  <g fill="url(#goldGrad)">
    <polygon points="30,30 45,30 30,45" />
    <polygon points="770,30 755,30 770,45" />
    <polygon points="30,770 45,770 30,755" />
    <polygon points="770,770 755,770 770,755" />
    <circle cx="400" cy="55" r="4" />
    <circle cx="400" cy="745" r="4" />
  </g>

  <!-- Central Crest Rings -->
  <circle cx="400" cy="360" r="185" fill="#0B133A" stroke="#EA1A85" stroke-width="2" opacity="0.8" />
  <circle cx="400" cy="360" r="175" fill="none" stroke="url(#goldGrad)" stroke-width="2.5" stroke-dasharray="6,4" />
  <circle cx="400" cy="360" r="155" fill="#070B1E" stroke="#EA1A85" stroke-width="1.5" />

  <!-- Monogram Initials -->
  <text x="400" y="415" 
        font-family="'Fraunces', 'Times New Roman', serif" 
        font-size="140" 
        font-weight="700" 
        letter-spacing="6" 
        fill="url(#textGold)" 
        text-anchor="middle"
        filter="drop-shadow(0px 8px 16px rgba(0,0,0,0.8))">{initials}</text>

  <!-- Royal Star Ornament -->
  <text x="400" y="240" font-family="sans-serif" font-size="20" fill="url(#goldGrad)" text-anchor="middle">★ ★ ★</text>

  <!-- Player Name Banner -->
  <text x="400" y="585" 
        font-family="'Barlow Condensed', 'Arial Black', sans-serif" 
        font-size="34" 
        font-weight="700" 
        letter-spacing="4" 
        fill="#FFFFFF" 
        text-anchor="middle">{full_name.upper()}</text>

  <!-- Role / Subtitle -->
  <text x="400" y="625" 
        font-family="'Barlow Condensed', sans-serif" 
        font-size="20" 
        font-weight="600" 
        letter-spacing="3" 
        fill="#D4AF37" 
        text-anchor="middle">{role.upper()}</text>

  <text x="400" y="655" 
        font-family="'JetBrains Mono', monospace" 
        font-size="13" 
        letter-spacing="2" 
        fill="#EA1A85" 
        text-anchor="middle">RAJASTHAN ROYALS · WAR ROOM SHORTLIST</text>
</svg>'''
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated SVG monogram: {out_path}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(base_dir, "..")
    img_players_dir = os.path.join(root_dir, "public", "img", "players")
    img_bg_dir = os.path.join(root_dir, "public", "img", "backgrounds")
    credits_path = os.path.join(root_dir, "public", "data", "credits.json")

    credits_list = []

    print("\n--- PROCESSING 20 PLAYERS ---")
    for p in PLAYERS:
        slug = p["slug"]
        cfile = p.get("commons_file")
        if cfile:
            print(f"Fetching Commons image for {p['name']} ({cfile})...")
            info = get_commons_info(cfile)
            if info and info.get("url"):
                out_file = os.path.join(img_players_dir, f"{slug}.jpg")
                rel_file = f"img/players/{slug}.jpg"
                try:
                    download_and_resize(info["url"], out_file, max_width=800)
                    credits_list.append({
                        "player": p["name"],
                        "file": rel_file,
                        "author": info["author"],
                        "license": info["license"],
                        "source_url": info["source_url"],
                        "fallback": False
                    })
                    continue
                except Exception as e:
                    print(f"Download error for {p['name']}: {e}")
            else:
                print(f"Could not retrieve Commons info for {cfile}")

        # Fallback SVG Monogram
        out_svg = os.path.join(img_players_dir, f"{slug}.svg")
        rel_svg = f"img/players/{slug}.svg"
        generate_svg_monogram(slug, p["initials"], p["name"], p["role"], out_svg)
        credits_list.append({
            "player": p["name"],
            "file": rel_svg,
            "author": "RR Analytics War Room (Handcrafted Monogram)",
            "license": "CC0 / Custom Monogram",
            "source_url": "Local Asset",
            "fallback": True,
            "fallback_reason": p.get("fallback_reason", "No freely licensed Commons portrait available")
        })

    print("\n--- PROCESSING BACKGROUND ASSETS ---")
    for bg in BACKGROUNDS:
        slug = bg["slug"]
        cfile = bg["commons_file"]
        print(f"Fetching background: {bg['title']} ({cfile})...")
        info = get_commons_info(cfile)
        if info and info.get("url"):
            out_file = os.path.join(img_bg_dir, f"{slug}.jpg")
            rel_file = f"img/backgrounds/{slug}.jpg"
            try:
                download_and_resize(info["url"], out_file, max_width=bg.get("max_width", 1920))
                credits_list.append({
                    "asset": bg["title"],
                    "file": rel_file,
                    "author": info["author"],
                    "license": info["license"],
                    "source_url": info["source_url"],
                    "fallback": False
                })
            except Exception as e:
                print(f"Background download error for {bg['title']}: {e}")

    os.makedirs(os.path.dirname(credits_path), exist_ok=True)
    with open(credits_path, "w", encoding="utf-8") as f:
        json.dump({"credits": credits_list}, f, indent=2)

    print(f"\nCompleted! Written credits to {credits_path}")

    # Summary
    photos = [c for c in credits_list if not c.get("fallback", False) and "player" in c]
    fallbacks = [c for c in credits_list if c.get("fallback", False) and "player" in c]
    bgs = [c for c in credits_list if "asset" in c]

    print(f"Real Photos: {len(photos)} / 20")
    for item in photos:
        print(f"  + [PHOTO] {item['player']}: {item['license']} ({item['author'][:25]})")

    print(f"Fallbacks: {len(fallbacks)} / 20")
    for item in fallbacks:
        print(f"  - [FALLBACK SVG] {item['player']} ({item.get('fallback_reason', '')[:40]})")

    print(f"Backgrounds: {len(bgs)}")
    for item in bgs:
        print(f"  * [BG] {item['asset']}: {item['license']}")

if __name__ == "__main__":
    main()

