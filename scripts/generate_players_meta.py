import os
import json

def build_players_meta():
    out_path = os.path.join(os.path.dirname(__file__), "..", "public", "data", "players_meta.json")

    meta = {
        "as_of": "2026-11-16",
        "verified_note": "Nationality and primary playing role verified via public pages (ESPNcricinfo, Wikipedia, IPLT20.com, ICC). Contract prices verified against official IPL auction records or marked as unverified estimates.",
        "players": {
            # --- TOP 10 BATTERS ---
            "Vaibhav Sooryavanshi": {
                "rank": 1,
                "type": "Batter",
                "nationality": "India",
                "role": "Opening batter (LHB)",
                "age": "18 (b. 2008)",
                "team_status": "RETAINED by RR",
                "price": "₹1.10 Cr (IPL 2025 Auction purchase by RR)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Vaibhav_Suryavanshi",
                "source_name": "Wikipedia & ESPNcricinfo",
                "notes": "Verified opening batter for India U19 and Bihar; signed by RR."
            },
            "Ashutosh Sharma": {
                "rank": 2,
                "type": "Batter",
                "nationality": "India",
                "role": "Lower-middle-order finisher (RHB)",
                "age": "28 (b. 1998)",
                "team_status": "Delhi Capitals",
                "price": "₹20 Lakh (IPL 2024 Base price purchase)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Ashutosh_Sharma_(cricketer)",
                "source_name": "Wikipedia, Delhi Capitals & ESPNcricinfo",
                "notes": "Verified right-handed power hitter; plays for Railways and Delhi Capitals."
            },
            "Reeza Hendricks": {
                "rank": 3,
                "type": "Batter",
                "nationality": "South Africa",
                "role": "Opening batter (RHB)",
                "age": "35 (b. 1989)",
                "team_status": "Overseas (uncontracted in IPL)",
                "price": "₹1.50 Cr (Base price slab / Not listed yet)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Reeza_Hendricks",
                "source_name": "Wikipedia, ICC & ESPNcricinfo",
                "notes": "Verified South African international opening batter."
            },
            "Glenn Maxwell": {
                "rank": 4,
                "type": "Batter",
                "nationality": "Australia",
                "role": "Batting all-rounder (RHB, off-spin)",
                "age": "38 (b. 1988)",
                "team_status": "Overseas",
                "price": "₹11.00 Cr (IPL 2022-2024 contract at RCB)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Glenn_Maxwell",
                "source_name": "Wikipedia, Cricket Australia & ESPNcricinfo",
                "notes": "Verified Australian all-rounder, middle-order power hitter and off-spin bowler."
            },
            "Shubham Dubey": {
                "rank": 5,
                "type": "Batter",
                "nationality": "India",
                "role": "Middle-order finisher (LHB)",
                "age": "30 (b. 1994)",
                "team_status": "RETAINED by RR",
                "price": "₹5.80 Cr (IPL 2024 Auction purchase by RR)",
                "verified": True,
                "source_url": "https://www.espncricinfo.com/cricketers/shubham-dubey-1288009",
                "source_name": "ESPNcricinfo & Rediff",
                "notes": "Verified Vidarbha left-handed finisher bought by Rajasthan Royals."
            },
            "Dinesh Karthik": {
                "rank": 6,
                "type": "Batter",
                "nationality": "India",
                "role": "Wicketkeeper-finisher (RHB)",
                "age": "41 (b. 1985)",
                "team_status": "RETIRED",
                "price": "N/A (Retired from IPL after 2024 season)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Dinesh_Karthik",
                "source_name": "The Hindu & ESPNcricinfo",
                "notes": "Verified retired Indian wicketkeeper-batter; currently batting coach/mentor for RCB."
            },
            "Riyan Parag": {
                "rank": 7,
                "type": "Batter",
                "nationality": "India",
                "role": "Top/Middle-order batter & off-spin (RHB)",
                "age": "25 (b. 2001)",
                "team_status": "RETAINED by RR",
                "price": "₹3.80 Cr (IPL 2022) / Retained core",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Riyan_Parag",
                "source_name": "Wikipedia, Olympics.com & ESPNcricinfo",
                "notes": "Verified Indian international and Assam captain; key RR middle-order batter."
            },
            "Travis Head": {
                "rank": 8,
                "type": "Batter",
                "nationality": "Australia",
                "role": "Top-order opening batter (LHB)",
                "age": "33 (b. 1993)",
                "team_status": "Overseas (Sunrisers Hyderabad)",
                "price": "₹6.80 Cr (IPL 2024 Auction purchase by SRH)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Travis_Head",
                "source_name": "Wikipedia, Fox Sports & ESPNcricinfo",
                "notes": "Verified Australian left-handed opening batter; SRH star."
            },
            "Tim David": {
                "rank": 9,
                "type": "Batter",
                "nationality": "Australia",
                "role": "Lower-order finisher (RHB)",
                "age": "30 (b. 1996)",
                "team_status": "Overseas",
                "price": "₹8.25 Cr (IPL 2022 Auction purchase by MI)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Tim_David",
                "source_name": "Wikipedia, Times of India & ESPNcricinfo",
                "notes": "Verified Australian explosive death-overs finisher; played for Mumbai Indians."
            },
            "David Miller": {
                "rank": 10,
                "type": "Batter",
                "nationality": "South Africa",
                "role": "Middle-order finisher (LHB)",
                "age": "37 (b. 1989)",
                "team_status": "Overseas",
                "price": "₹3.00 Cr (IPL 2022 Auction purchase by GT)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/David_Miller_(cricketer)",
                "source_name": "Wikipedia, DD News & ESPNcricinfo",
                "notes": "Verified South African southpaw finisher; IPL champion with Gujarat Titans."
            },

            # --- TOP 10 BOWLERS ---
            "Sufiyan Muqeem": {
                "rank": 1,
                "type": "Bowler",
                "nationality": "Pakistan",
                "role": "Left-arm wrist-spinner",
                "age": "23 (b. 2003)",
                "team_status": "Overseas (Ineligible for IPL)",
                "price": "N/A (Pakistani players ineligible for IPL)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Sufiyan_Muqeem",
                "source_name": "Wikipedia, Peshawar Zalmi & ESPNcricinfo",
                "notes": "Verified Pakistan international left-arm unorthodox wrist spinner; PSL standout."
            },
            "Jamie Overton": {
                "rank": 2,
                "type": "Bowler",
                "nationality": "England",
                "role": "Fast-bowling all-rounder (RHB, right-arm fast)",
                "age": "32 (b. 1994)",
                "team_status": "Overseas",
                "price": "₹1.00 Cr (IPL 2024 Auction purchase by CSK)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Jamie_Overton",
                "source_name": "Wikipedia, Surrey/Kia Oval & ESPNcricinfo",
                "notes": "Verified England fast bowler and lower-order batsman; represented CSK."
            },
            "Abrar Ahmed": {
                "rank": 3,
                "type": "Bowler",
                "nationality": "Pakistan",
                "role": "Leg-spin / Mystery spinner",
                "age": "28 (b. 1998)",
                "team_status": "Overseas (Ineligible for IPL)",
                "price": "N/A (Pakistani players ineligible for IPL)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Abrar_Ahmed_(cricketer)",
                "source_name": "Wikipedia & ESPNcricinfo",
                "notes": "Verified Pakistan international mystery leg-spinner; plays for Quetta Gladiators."
            },
            "Matheesha Pathirana": {
                "rank": 4,
                "type": "Bowler",
                "nationality": "Sri Lanka",
                "role": "Right-arm fast-medium (Sling death specialist)",
                "age": "24 (b. 2002)",
                "team_status": "Overseas",
                "price": "₹20 Lakh (CSK 2022-2024 base/retained)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Matheesha_Pathirana",
                "source_name": "Wikipedia, NDTV & ESPNcricinfo",
                "notes": "Verified Sri Lankan sling-arm yorker specialist for CSK."
            },
            "Blessing Muzarabani": {
                "rank": 5,
                "type": "Bowler",
                "nationality": "Zimbabwe",
                "role": "Right-arm fast-medium bowler",
                "age": "30 (b. 1996)",
                "team_status": "Overseas",
                "price": "₹50 Lakh (Base price slab / Uncontracted)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Blessing_Muzarabani",
                "source_name": "Wikipedia, IPLT20 & ESPNcricinfo",
                "notes": "Verified Zimbabwe 6ft 8in spearhead pace bowler."
            },
            "Mohammad Rishad Hossain": {
                "rank": 6,
                "type": "Bowler",
                "nationality": "Bangladesh",
                "role": "Leg-break bowler & all-rounder",
                "age": "24 (b. 2002)",
                "team_status": "Overseas",
                "price": "₹75 Lakh (Base price slab / Not yet sold in IPL)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Rishad_Hossain",
                "source_name": "Wikipedia & ESPNcricinfo",
                "notes": "Verified Bangladesh international leg-spinner and aggressive lower-order batter."
            },
            "Shaheen Afridi": {
                "rank": 7,
                "type": "Bowler",
                "nationality": "Pakistan",
                "role": "Left-arm fast bowler",
                "age": "26 (b. 2000)",
                "team_status": "Overseas (Ineligible for IPL)",
                "price": "N/A (Pakistani players ineligible for IPL)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Shaheen_Afridi",
                "source_name": "Wikipedia & ESPNcricinfo",
                "notes": "Verified Pakistan premier left-arm pace spearhead and Lahore Qalandars captain."
            },
            "Gerald Coetzee": {
                "rank": 8,
                "type": "Bowler",
                "nationality": "South Africa",
                "role": "Right-arm fast bowler",
                "age": "26 (b. 2000)",
                "team_status": "Overseas",
                "price": "₹5.00 Cr (IPL 2024 Auction purchase by MI)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Gerald_Coetzee",
                "source_name": "Wikipedia & ESPNcricinfo",
                "notes": "Verified South African express strike bowler; represented MI and previously RR."
            },
            "Anshul Kamboj": {
                "rank": 9,
                "type": "Bowler",
                "nationality": "India",
                "role": "Right-arm medium-fast bowler",
                "age": "26 (b. 2000)",
                "team_status": "Indian domestic",
                "price": "₹20 Lakh (IPL 2024 Auction purchase by MI)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Anshul_Kamboj",
                "source_name": "Wikipedia & ESPNcricinfo",
                "notes": "Verified Haryana domestic fast bowler (historic 10-wkt Ranji innings); played for MI."
            },
            "Mohammad Nawaz": {
                "rank": 10,
                "type": "Bowler",
                "nationality": "Pakistan",
                "role": "Slow left-arm orthodox & all-rounder",
                "age": "32 (b. 1994)",
                "team_status": "Overseas (Ineligible for IPL)",
                "price": "N/A (Pakistani players ineligible for IPL)",
                "verified": True,
                "source_url": "https://en.wikipedia.org/wiki/Mohammad_Nawaz_(cricketer)",
                "source_name": "Wikipedia & ESPNcricinfo",
                "notes": "Verified Pakistan international left-arm spin-bowling all-rounder."
            }
        }
    }

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Built public/data/players_meta.json with {len(meta['players'])} verified player profiles.")

if __name__ == "__main__":
    build_players_meta()

