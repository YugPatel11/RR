import json

with open('outputs/results.json') as f:
    data = json.load(f)

print('=== TOP BATTERS ===')
for b in data['top_batters']:
    rank = b['rank']
    name = b['name']
    team = b['team']
    rating = b['rating']
    sr_hp = b['sr_hp']
    sr_lp = b['sr_lp']
    impact = b['impact']
    ci_low = b['ci_low']
    ci_high = b['ci_high']
    top10 = b['top10_pct']
    slot = b['slot']
    hp_balls = b['hp_balls']
    bnd = b['boundary_pct_hp']
    dot = b['dot_pct_hp']
    print(f"  {rank:2d}. {name:25s} | {team:30s} | R={rating:.3f} | SR: {sr_hp} (HP) / {sr_lp} (LP) | Imp={impact:.3f} | CI=[{ci_low},{ci_high}] | Top10={top10}% | {slot} | {hp_balls}b | Bnd%={bnd} Dot%={dot}")

print()
print('=== TOP BOWLERS ===')
for b in data['top_bowlers']:
    rank = b['rank']
    name = b['name']
    team = b['team']
    rating = b['rating']
    econ_hp = b['econ_hp']
    econ_lp = b['econ_lp']
    wkt_rate = b['wkt_rate_hp']
    ci_low = b['ci_low']
    ci_high = b['ci_high']
    top10 = b['top10_pct']
    slot = b['slot']
    hp_balls = b['hp_balls']
    dot = b['dot_pct_hp']
    print(f"  {rank:2d}. {name:25s} | {team:30s} | R={rating:.3f} | Econ: {econ_hp} (HP) / {econ_lp} (LP) | WktR={wkt_rate} | CI=[{ci_low},{ci_high}] | Top10={top10}% | {slot} | {hp_balls}b | Dot%={dot}")

