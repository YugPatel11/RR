"""
Post-processing: Fix nationality, add RR squad context, regenerate results.json
"""
import pandas as pd
import numpy as np
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', '..', 'Data Pack', 'Data Pack')
OUT  = os.path.join(BASE, '..')

ctpm = pd.read_csv(os.path.join(DATA, 'competition_team_player_mapping.csv'))
comp = pd.read_csv(os.path.join(DATA, 'competitions.csv'))

# Build proper nationality
IPL_COMP_IDS = [1358, 1715, 2193, 2725, 3298]
T20I_comps = comp[comp['match_format'] == 'T20I']['comp_id'].tolist()

# T20I players → international team = their country
t20i_players = ctpm[ctpm['comp_id'].isin(T20I_comps)]
# Get primary country (most common team name in T20I)
player_country = t20i_players.groupby('player_id')['team_name'].agg(lambda x: x.value_counts().index[0]).to_dict()

# IPL-only players → Indian
ipl_players = set(ctpm[ctpm['comp_id'].isin(IPL_COMP_IDS)]['player_id'].unique())
t20i_player_set = set(t20i_players['player_id'].unique())
ipl_only = ipl_players - t20i_player_set

# India A / Emerging teams
india_assoc = ctpm[ctpm['team_name'].str.contains('India', case=False, na=False)]['player_id'].unique()

for pid in ipl_only:
    player_country[pid] = 'India'
for pid in india_assoc:
    if pid not in player_country:
        player_country[pid] = 'India'

# Load results
with open(os.path.join(OUT, 'results.json')) as f:
    data = json.load(f)

# Get player name → id mapping
name_to_id = ctpm[['player_id', 'player_name']].drop_duplicates('player_name').set_index('player_name')['player_id'].to_dict()

# Load batter/bowler ratings for player IDs
bat_ratings = pd.read_csv(os.path.join(OUT, 'analysis', 'batter_ratings.csv'))
bowl_ratings = pd.read_csv(os.path.join(OUT, 'analysis', 'bowler_ratings.csv'))

# Map IDs
bat_id_map = bat_ratings.set_index('player_name')['striker_id'].to_dict()
bowl_id_map = bowl_ratings.set_index('player_name')['bowler_id'].to_dict()

# RR current squad (IPL 2026) player IDs
rr_players_2026 = ctpm[(ctpm['comp_id'] == 3298) & (ctpm['team_name'] == 'Rajasthan Royals')]['player_id'].unique()
rr_player_names = ctpm[(ctpm['comp_id'] == 3298) & (ctpm['team_name'] == 'Rajasthan Royals')]['player_name'].unique()

# RR squad gaps based on research
RR_GAPS = {
    'death_bowling': 'Needs a reliable death-overs specialist to support Jofra Archer',
    'finisher': 'Needs explosive lower-middle-order finisher to complement top-order firepower',
    'spin_control': 'Needs economical wicket-taking spinner for middle-overs control',
    'pace_backup': 'Needs Indian pace backup for death overs (Tushar Deshpande inconsistent)',
    'top_order_backup': 'Could use a backup opener/top-order option'
}

# Player context from research (age, role, auction feasibility, risks)
PLAYER_CONTEXT = {
    'Vaibhav Sooryavanshi': {
        'age': '18 (b. 2008)', 'role': 'Opening batter (LHB)', 'nationality': 'India',
        'status': 'RETAINED by RR', 'ipl_team': 'Rajasthan Royals',
        'note': 'Already retained. 776 runs in IPL 2026 at SR 184. RR cornerstone.',
        'rr_fit': 'Already at RR — the data confirms he is their most valuable batting asset under pressure.',
        'risk': 'Very young; sample = 82 HP balls. Extraordinary ceiling but sustainability unproven.'
    },
    'Ashutosh Sharma': {
        'age': '24 (b. 2002)', 'role': 'Top-order batter (RHB)', 'nationality': 'India',
        'status': 'At Delhi Capitals', 'ipl_team': 'Delhi Capitals',
        'note': 'Explosive IPL performer. 180+ SR under pressure.',
        'rr_fit': 'Could serve as top-order backup/Impact Player. Fills Indian batting depth gap.',
        'risk': 'Limited sample in T20I. Only IPL data. DC likely to retain.',
        'price_band': '₹3-6 Cr'
    },
    'Reeza Hendricks': {
        'age': '35 (b. 1989)', 'role': 'Opening batter (RHB)', 'nationality': 'South Africa',
        'status': 'Overseas, no IPL contract', 'ipl_team': 'None (uncapped in IPL)',
        'note': '278 HP balls, huge SR uplift under pressure (178 vs 130). T20I specialist.',
        'rr_fit': 'Top-order overseas option. Would use overseas slot. RR already have Jaiswal at top.',
        'risk': 'Age 35. T20I-only data, no IPL experience. Weak-opposition inflation possible.',
        'price_band': '₹1-2 Cr (base price)'
    },
    'Glenn Maxwell': {
        'age': '38 (b. 1988)', 'role': 'All-rounder (RHB, off-spin)', 'nationality': 'Australia',
        'status': 'Overseas', 'ipl_team': 'Previously RCB',
        'note': 'Elite match-winner under pressure. 180+ SR in HP situations.',
        'rr_fit': 'Could fill finisher + part-time spin role. Uses overseas slot.',
        'risk': 'Age 38. Injury history. Uses overseas slot. Recent form declining.',
        'price_band': '₹4-8 Cr'
    },
    'Shubham Dubey': {
        'age': '24 (b. 2002)', 'role': 'Middle-order batter (RHB)', 'nationality': 'India',
        'status': 'RETAINED by RR', 'ipl_team': 'Rajasthan Royals',
        'note': 'Already retained. SR jumps from 105 (LP) to 181 (HP) — massive pressure performer.',
        'rr_fit': 'Already at RR. Data validates his role as a pressure finisher.',
        'risk': 'Small sample (91 HP balls). Big SR delta may mean volatile performances.'
    },
    'Dinesh Karthik': {
        'age': '41 (b. 1985)', 'role': 'Wicketkeeper-finisher (RHB)', 'nationality': 'India',
        'status': 'RETIRED', 'ipl_team': 'Retired (was at RCB)',
        'note': 'Retired from cricket. Data from 2022-2024 era. Not available for auction.',
        'rr_fit': 'NOT AVAILABLE — retired.',
        'risk': 'Retired. Cannot be targeted at auction.'
    },
    'Riyan Parag': {
        'age': '23 (b. 2002)', 'role': 'Top/Middle-order batter + off-spin (RHB)', 'nationality': 'India',
        'status': 'RETAINED by RR', 'ipl_team': 'Rajasthan Royals',
        'note': 'Already retained. Solid under pressure (SR 163) with good consistency.',
        'rr_fit': 'Already at RR. Captain material. Data confirms reliability.',
        'risk': 'Lower bootstrap stability (7.2%) — rankings can shift with more data.'
    },
    'Travis Head': {
        'age': '33 (b. 1993)', 'role': 'Top-order batter (LHB)', 'nationality': 'Australia',
        'status': 'Overseas', 'ipl_team': 'Previously SRH',
        'note': 'Aggressive LHB. 170 SR under pressure. 151 HP balls.',
        'rr_fit': 'LHB provides batting balance alongside RR RHB-heavy lineup. Impact player potential.',
        'risk': 'Age 33. Dot% of 44% under HP is high. Uses overseas slot.',
        'price_band': '₹8-12 Cr'
    },
    'Tim David': {
        'age': '29 (b. 1996)', 'role': 'Finisher (RHB)', 'nationality': 'Australia/Singapore',
        'status': 'Overseas', 'ipl_team': 'RCB (2025-26)',
        'note': 'Elite finisher. 187 SR under HP with 367 balls — large sample. 91.6% bootstrap stability.',
        'rr_fit': 'IDEAL finisher target. Fills RR middle-order power gap. Death-overs specialist.',
        'risk': 'Uses overseas slot. High auction demand expected.',
        'price_band': '₹10-14 Cr'
    },
    'David Miller': {
        'age': '37 (b. 1989)', 'role': 'Finisher (LHB)', 'nationality': 'South Africa',
        'status': 'Overseas', 'ipl_team': 'Delhi Capitals (2025-26)',
        'note': 'Veteran finisher. 164 SR under HP. Huge sample (573 HP balls). Low bootstrap (5.6%).',
        'rr_fit': 'LHB finisher option. Provides experience and stability. Uses overseas slot.',
        'risk': 'Age 37. Low bootstrap stability. Uses overseas slot.',
        'price_band': '₹4-7 Cr'
    },
    'Sufiyan Muqeem': {
        'age': '23 (b. 2003)', 'role': 'Left-arm wrist spinner', 'nationality': 'Pakistan',
        'status': 'Overseas (Pakistan)', 'ipl_team': 'None (Pakistan player)',
        'note': 'Economy of 5.0 under HP — extraordinary. 56% dot ball rate. 218 HP balls.',
        'rr_fit': 'ELITE spin option for middle-overs control. BUT Pakistani players not available in IPL.',
        'risk': 'Pakistani players CANNOT play IPL. Not available for auction.',
        'price_band': 'N/A (ineligible)'
    },
    'Jamie Overton': {
        'age': '30 (b. 1994)', 'role': 'Fast-bowling all-rounder (RHB)', 'nationality': 'England',
        'status': 'Overseas', 'ipl_team': 'CSK (2024-25)',
        'note': 'All-rounder with 6.5 econ under HP + batting utility. High wicket rate (12.93%).',
        'rr_fit': 'Death bowling + lower-order hitting. Exactly what RR needs.',
        'risk': 'Injury-prone. Uses overseas slot. 116 HP balls (small sample).',
        'price_band': '₹4-8 Cr'
    },
    'Abrar Ahmed': {
        'age': '25 (b. 2001)', 'role': 'Leg-spin / mystery spinner', 'nationality': 'Pakistan',
        'status': 'Overseas (Pakistan)', 'ipl_team': 'None (Pakistan player)',
        'note': 'Economy 5.3 under HP, 98.6% bootstrap stability. Elite pressure bowler.',
        'rr_fit': 'NOT AVAILABLE — Pakistani player cannot play IPL.',
        'risk': 'Pakistani players ineligible for IPL.',
        'price_band': 'N/A (ineligible)'
    },
    'Matheesha Pathirana': {
        'age': '22 (b. 2004)', 'role': 'Fast bowler (slingy action)', 'nationality': 'Sri Lanka',
        'status': 'Overseas', 'ipl_team': 'CSK (retained)',
        'note': 'Elite death bowler. 6.9 econ under HP with 403 HP balls. 9.68% wicket rate.',
        'rr_fit': 'PERFECT death bowling solution for RR. Young, proven in IPL.',
        'risk': 'CSK likely to retain. Very high demand if available. Uses overseas slot.',
        'price_band': '₹12-18 Cr if released'
    },
    'Blessing Muzarabani': {
        'age': '28 (b. 1998)', 'role': 'Fast bowler', 'nationality': 'Zimbabwe',
        'status': 'Overseas', 'ipl_team': 'None currently',
        'note': 'High wicket rate (14.68%) under HP. 109 HP balls (small sample).',
        'rr_fit': 'Death bowling option. Affordable overseas pace. Limited IPL experience.',
        'risk': 'Small sample. Weak-opposition T20I inflation possible. Uses overseas slot.',
        'price_band': '₹2-4 Cr'
    },
    'Mohammad Rishad Hossain': {
        'age': '22 (b. 2004)', 'role': 'Fast bowler', 'nationality': 'Bangladesh',
        'status': 'Overseas', 'ipl_team': 'KKR (2024-25)',
        'note': 'Young pacer. 6.9 econ under HP with 13.68% wicket rate.',
        'rr_fit': 'Young pace investment. Death bowling potential.',
        'risk': 'Uses overseas slot. Limited IPL track record.',
        'price_band': '₹2-5 Cr'
    },
    'Shaheen Afridi': {
        'age': '26 (b. 2000)', 'role': 'Left-arm fast bowler', 'nationality': 'Pakistan',
        'status': 'Overseas (Pakistan)', 'ipl_team': 'None (Pakistan player)',
        'note': 'World-class pacer. 6.5 econ under HP. 64.8% bootstrap stability.',
        'rr_fit': 'NOT AVAILABLE — Pakistani player cannot play IPL.',
        'risk': 'Pakistani players ineligible for IPL.',
        'price_band': 'N/A (ineligible)'
    },
    'Gerald Coetzee': {
        'age': '24 (b. 2002)', 'role': 'Fast bowler', 'nationality': 'South Africa',
        'status': 'Overseas', 'ipl_team': 'MI (2024), RR previously',
        'note': 'Young express pacer. 7.4 econ under HP. 11.11% wicket rate.',
        'rr_fit': 'Previously at RR (2024). Knows the franchise. Death bowling support.',
        'risk': 'Injury concerns. 126 HP balls (small sample). Uses overseas slot.',
        'price_band': '₹4-8 Cr'
    },
    'Anshul Kamboj': {
        'age': '24 (b. 2002)', 'role': 'Medium-fast bowler', 'nationality': 'India',
        'status': 'Indian domestic', 'ipl_team': 'Chennai Super Kings',
        'note': 'Indian pacer. 7.3 econ under HP. 14.29% wicket rate. 98 HP balls.',
        'rr_fit': 'Indian pace backup for death overs. Does not use overseas slot!',
        'risk': 'Small sample (98 HP balls). CSK may retain. Limited T20 experience.',
        'price_band': '₹2-4 Cr'
    },
    'Mohammad Nawaz': {
        'age': '32 (b. 1994)', 'role': 'Left-arm spin all-rounder', 'nationality': 'Pakistan',
        'status': 'Overseas (Pakistan)', 'ipl_team': 'None (Pakistan player)',
        'note': 'Left-arm spinner with batting. 6.3 econ under HP. 70.8% bootstrap stability.',
        'rr_fit': 'NOT AVAILABLE — Pakistani player cannot play IPL.',
        'risk': 'Pakistani players ineligible for IPL.',
        'price_band': 'N/A (ineligible)'
    },
}

# Update results.json
for b in data['top_batters']:
    name = b['name']
    # Fix nationality
    pid = bat_id_map.get(name)
    if pid:
        country = player_country.get(pid, 'Unknown')
        if country in ['India', 'India A', 'India B']:
            b['slot'] = 'Indian'
        else:
            b['slot'] = 'Overseas'
        b['nationality'] = country
    ctx = PLAYER_CONTEXT.get(name, {})
    b['age'] = ctx.get('age', 'Unknown')
    b['role'] = ctx.get('role', 'Unknown')
    b['status'] = ctx.get('status', 'Unknown')
    b['rr_fit'] = ctx.get('rr_fit', 'TBD')
    b['risk'] = ctx.get('risk', 'TBD')
    b['price_band'] = ctx.get('price_band', 'TBD')
    b['is_rr'] = pid in rr_players_2026 if pid else False
    b['is_available'] = ctx.get('status', '') not in ['RETIRED', 'RETAINED by RR']

for b in data['top_bowlers']:
    name = b['name']
    pid = bowl_id_map.get(name)
    if pid:
        country = player_country.get(pid, 'Unknown')
        if country in ['India', 'India A', 'India B']:
            b['slot'] = 'Indian'
        else:
            b['slot'] = 'Overseas'
        b['nationality'] = country
    ctx = PLAYER_CONTEXT.get(name, {})
    b['age'] = ctx.get('age', 'Unknown')
    b['role'] = ctx.get('role', 'Unknown')
    b['status'] = ctx.get('status', 'Unknown')
    b['rr_fit'] = ctx.get('rr_fit', 'TBD')
    b['risk'] = ctx.get('risk', 'TBD')
    b['price_band'] = ctx.get('price_band', 'TBD')
    b['is_pakistan'] = 'Pakistan' in ctx.get('nationality', '')

# Add RR context
data['rr_context'] = {
    'squad_2026': list(rr_player_names),
    'gaps': RR_GAPS,
    'purse': '₹157 Cr total cap',
    'auction_date': 'December 16, 2026',
    'overseas_limit': '8 per squad, 4 per XI',
    'core_retained': ['Yashasvi Jaiswal', 'Riyan Parag', 'Dhruv Jurel', 'Vaibhav Sooryavanshi', 'Jofra Archer', 'Sam Curran', 'Ravindra Jadeja'],
    'expected_releases': ['Shimron Hetmyer (high price vs output)', 'Kwena Maphaka', 'Yudhvir Singh'],
}

# Save updated results
with open(os.path.join(OUT, 'results.json'), 'w') as f:
    json.dump(data, f, indent=2, default=str)

print("Updated results.json with nationality fixes and RR context.")
print("\nAuction-actionable players (NOT retired, NOT already at RR, NOT Pakistan):")
for b in data['top_batters']:
    available = b.get('is_available', True) and b.get('status', '') not in ['RETIRED']
    not_rr = not b.get('is_rr', False)
    name = b['name']
    ctx = PLAYER_CONTEXT.get(name, {})
    nat = ctx.get('nationality', '')
    if available and not_rr and 'Pakistan' not in nat:
        print(f"  BAT #{b['rank']}: {name} ({b['slot']}) — {ctx.get('rr_fit', 'TBD')}")

for b in data['top_bowlers']:
    nat = PLAYER_CONTEXT.get(b['name'], {}).get('nationality', '')
    if 'Pakistan' not in nat and b.get('status', '') not in ['RETIRED']:
        print(f"  BOWL #{b['rank']}: {b['name']} ({b['slot']}) — {PLAYER_CONTEXT.get(b['name'], {}).get('rr_fit', 'TBD')}")

