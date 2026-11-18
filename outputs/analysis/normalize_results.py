"""
Normalize results.json with verified metadata from players_meta.json.
Ensures unified player structure across both top_batters and top_bowlers.
"""

import json

with open('outputs/players_meta.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

with open('outputs/results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

p_dict = meta['players']

# Normalized fields to ensure on both batters and bowlers
for b in results['top_batters']:
    name = b['name']
    p_info = p_dict.get(name, {})
    b['player_id'] = p_info.get('player_id')
    b['age'] = p_info.get('age')
    b['dob'] = p_info.get('dob')
    b['role'] = p_info.get('primary_role')
    b['batting_style'] = p_info.get('batting_style')
    b['bowling_style'] = p_info.get('bowling_style')
    b['ipl_eligibility'] = p_info.get('ipl_eligibility')
    b['is_eligible'] = "Eligible" in p_info.get('ipl_eligibility', '')
    b['is_pakistan'] = "Pakistan" in p_info.get('nationality', '')
    b['is_retired'] = "Retired" in p_info.get('ipl_eligibility', '')
    b['is_rr'] = "Rajasthan Royals" in p_info.get('ipl_franchise_2026', '')
    b['is_available'] = b['is_eligible'] and not b['is_rr']
    b['last_verified_price'] = p_info.get('last_verified_price')
    b['base_price_slab'] = p_info.get('current_base_price_slab')
    b['verified_source_url'] = p_info.get('source_url')
    b['verified_source_name'] = p_info.get('source_name')
    b['verified_as_of'] = p_info.get('verified_as_of')

for b in results['top_bowlers']:
    name = b['name']
    p_info = p_dict.get(name, {})
    b['player_id'] = p_info.get('player_id')
    b['age'] = p_info.get('age')
    b['dob'] = p_info.get('dob')
    b['role'] = p_info.get('primary_role')
    b['batting_style'] = p_info.get('batting_style')
    b['bowling_style'] = p_info.get('bowling_style')
    b['ipl_eligibility'] = p_info.get('ipl_eligibility')
    b['is_eligible'] = "Eligible" in p_info.get('ipl_eligibility', '')
    b['is_pakistan'] = "Pakistan" in p_info.get('nationality', '')
    b['is_retired'] = "Retired" in p_info.get('ipl_eligibility', '')
    b['is_rr'] = "Rajasthan Royals" in p_info.get('ipl_franchise_2026', '')
    b['is_available'] = b['is_eligible'] and not b['is_rr']
    b['last_verified_price'] = p_info.get('last_verified_price')
    b['base_price_slab'] = p_info.get('current_base_price_slab')
    b['verified_source_url'] = p_info.get('source_url')
    b['verified_source_name'] = p_info.get('source_name')
    b['verified_as_of'] = p_info.get('verified_as_of')

# Save updated results.json
with open('outputs/results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Normalized results.json with unified player structure across batters and bowlers.")

