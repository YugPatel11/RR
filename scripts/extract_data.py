import os
import re
import json

def extract_data():
    html_path = os.path.join(os.path.dirname(__file__), "..", "old", "index_1.html")
    out_path = os.path.join(os.path.dirname(__file__), "..", "public", "data", "players.json")

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the const DATA = { ... }; block
    match = re.search(r"const\s+DATA\s*=\s*(\{.*?\});\s*(?:\n|\r|\/\/)", content, re.DOTALL)
    if not match:
        raise ValueError("Could not find const DATA in old/index_1.html")

    data_str = match.group(1)
    data = json.loads(data_str)

    # Normalize Batters
    for b in data.get("top_batters", []):
        is_rr = bool(b.get("is_rr", False) or "Rajasthan Royals" in b.get("team", "") or "RR" in b.get("status", ""))
        is_pak = (b.get("nationality", "").lower() == "pakistan")
        is_ret = ("retired" in b.get("status", "").lower())
        
        b["is_rr"] = is_rr
        if is_pak:
            b["is_available"] = False
            b["locked_reason"] = "Pakistani player ineligible for IPL"
        elif is_ret:
            b["is_available"] = False
            b["locked_reason"] = "Retired"
        elif is_rr:
            b["is_available"] = False
            b["locked_reason"] = "Already at RR"
        else:
            b["is_available"] = True
            b["locked_reason"] = None

    # Normalize Bowlers
    for bw in data.get("top_bowlers", []):
        is_rr = bool(bw.get("is_rr", False) or "Rajasthan Royals" in bw.get("team", "") or "RR" in bw.get("status", ""))
        is_pak = bool(bw.get("is_pakistan", False) or bw.get("nationality", "").lower() == "pakistan")
        is_ret = ("retired" in bw.get("status", "").lower())

        bw["is_rr"] = is_rr
        if is_pak:
            bw["is_available"] = False
            bw["locked_reason"] = "Pakistani player ineligible for IPL"
        elif is_ret:
            bw["is_available"] = False
            bw["locked_reason"] = "Retired"
        elif is_rr:
            bw["is_available"] = False
            bw["locked_reason"] = "Already at RR"
        else:
            bw["is_available"] = True
            bw["locked_reason"] = None

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully extracted DATA and saved to {out_path}")
    print(f"Top Batters: {len(data.get('top_batters', []))}")
    print(f"Top Bowlers: {len(data.get('top_bowlers', []))}")

if __name__ == "__main__":
    extract_data()

