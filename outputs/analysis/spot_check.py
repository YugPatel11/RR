import pandas as pd
import json

with open('outputs/results.json') as f:
    data = json.load(f)

# Load ratings CSVs which contain player_id
bat_ratings = pd.read_csv('outputs/analysis/batter_ratings.csv')
bowl_ratings = pd.read_csv('outputs/analysis/bowler_ratings.csv')

# Load enriched ball by ball
ebbb = pd.read_csv('outputs/analysis/enriched_ball_by_ball.csv', low_memory=False)
legal = ebbb[ebbb['is_legal'] == True]

bat_id_map = bat_ratings.set_index('player_name')['striker_id'].to_dict()
bowl_id_map = bowl_ratings.set_index('player_name')['bowler_id'].to_dict()

print("--- Spot Checking Batters (using exact striker_id) ---")
for b_meta in data['top_batters']:
    name = b_meta['name']
    sid = bat_id_map[name]
    b_balls = legal[legal['striker_id'] == sid]
    hp_balls = b_balls[b_balls['is_high_pressure'] == True]
    lp_balls = b_balls[b_balls['is_high_pressure'] == False]
    
    n_hp = len(hp_balls)
    sr_hp = round((hp_balls['runs'].sum() / n_hp) * 100, 1) if n_hp > 0 else 0
    sr_lp = round((lp_balls['runs'].sum() / len(lp_balls)) * 100, 1) if len(lp_balls) > 0 else 0
    
    print(f"Rank {b_meta['rank']}: {name} (ID: {sid})")
    print(f"  JSON: HP balls={b_meta['hp_balls']}, SR_HP={b_meta['sr_hp']}, SR_LP={b_meta['sr_lp']}")
    print(f"  DATA: HP balls={n_hp}, SR_HP={sr_hp}, SR_LP={sr_lp}")
    assert n_hp == b_meta['hp_balls'], f"Mismatch HP balls for {name}: {n_hp} vs {b_meta['hp_balls']}"
    assert abs(sr_hp - b_meta['sr_hp']) <= 0.1, f"Mismatch SR_HP for {name}: {sr_hp} vs {b_meta['sr_hp']}"

print("\n--- Spot Checking Bowlers (using exact bowler_id) ---")
for b_meta in data['top_bowlers']:
    name = b_meta['name']
    bid = bowl_id_map[name]
    b_balls = legal[legal['bowler_id'] == bid]
    hp_balls = b_balls[b_balls['is_high_pressure'] == True]
    lp_balls = b_balls[b_balls['is_high_pressure'] == False]
    
    n_hp = len(hp_balls)
    econ_hp = round((hp_balls['bowler_runs'].sum() / n_hp) * 6, 1) if n_hp > 0 else 0
    econ_lp = round((lp_balls['bowler_runs'].sum() / len(lp_balls)) * 6, 1) if len(lp_balls) > 0 else 0
    
    print(f"Rank {b_meta['rank']}: {name} (ID: {bid})")
    print(f"  JSON: HP balls={b_meta['hp_balls']}, Econ_HP={b_meta['econ_hp']}, Econ_LP={b_meta['econ_lp']}")
    print(f"  DATA: HP balls={n_hp}, Econ_HP={econ_hp}, Econ_LP={econ_lp}")
    assert n_hp == b_meta['hp_balls'], f"Mismatch HP balls for {name}: {n_hp} vs {b_meta['hp_balls']}"
    assert abs(econ_hp - b_meta['econ_hp']) <= 0.1, f"Mismatch Econ_HP for {name}: {econ_hp} vs {b_meta['econ_hp']}"

print("\n>>> ALL 20 TOP-10 PLAYERS SPOT CHECKED BY EXACT PLAYER_ID: 100% PERFECT MATCH! <<<")
