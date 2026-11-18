import json

with open('outputs/results.json') as f:
    data = json.load(f)

print("BATTERS:")
for b in data['top_batters']:
    print(f"#{b['rank']}: {b['name']} | Nat: {b.get('nationality')} | Role: {b.get('role')} | Status: {b.get('status')} | Price: {b.get('price_band')}")

print("\nBOWLERS:")
for b in data['top_bowlers']:
    print(f"#{b['rank']}: {b['name']} | Nat: {b.get('nationality')} | Role: {b.get('role')} | Status: {b.get('status')} | Price: {b.get('price_band')}")

