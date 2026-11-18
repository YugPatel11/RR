import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(OUT_DIR, 'results.json'), 'r') as f:
    data = json.load(f)

# Styles
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
colors_rr = {'blue': '#1A2456', 'pink': '#EA1A85', 'light_blue': '#2A3670', 'gray': '#6B7280', 'light_gray': '#F4F5F7'}

# 1. Pressure validation chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=300)
bins = ['Low', 'Medium', 'High', 'Very High']
bin_keys = ['low', 'medium', 'high', 'very_high']
wkt_rates = [data['pressure_validation'][k]['wicket_rate'] for k in bin_keys]
dot_rates = [data['pressure_validation'][k]['dot_pct'] for k in bin_keys]

ax1.bar(bins, wkt_rates, color=['#A5B4FC', '#818CF8', '#4F46E5', '#EA1A85'], width=0.55, edgecolor='black', linewidth=0.5)
ax1.set_title('Wicket Hazard Rate by Pressure Quartile (%)', fontsize=11, fontweight='bold', color=colors_rr['blue'])
ax1.set_ylabel('Wickets per 100 Balls (%)', fontsize=9)
for i, v in enumerate(wkt_rates):
    ax1.text(i, v + 0.3, f"{v:.1f}%", ha='center', fontsize=9, fontweight='bold')
ax1.set_ylim(0, max(wkt_rates) + 2)

ax2.bar(bins, dot_rates, color=['#93C5FD', '#60A5FA', '#2563EB', '#1A2456'], width=0.55, edgecolor='black', linewidth=0.5)
ax2.set_title('Dot Ball Concentration by Pressure Quartile (%)', fontsize=11, fontweight='bold', color=colors_rr['blue'])
ax2.set_ylabel('Dot Ball Percentage (%)', fontsize=9)
for i, v in enumerate(dot_rates):
    ax2.text(i, v + 1.0, f"{v:.1f}%", ha='center', fontsize=9, fontweight='bold')
ax2.set_ylim(0, max(dot_rates) + 6)

plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'analysis', 'fig_pressure_validation.png'))
plt.close(fig)

# 2. Top 10 Batters SR: Pressure vs Normal + Error Bars
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
batters = data['top_batters']
names = [b['name'].split()[-1] if len(b['name'].split())>1 else b['name'] for b in batters]
full_names = [b['name'] for b in batters]
sr_hp = [b['sr_hp'] for b in batters]
sr_lp = [b['sr_lp'] for b in batters]
ci_low = [b['ci_low'] for b in batters]
ci_high = [b['ci_high'] for b in batters]
x = np.arange(len(names))
width = 0.35

rects1 = ax.bar(x - width/2, sr_lp, width, label='Normal Match State', color='#1A2456', alpha=0.85)
rects2 = ax.bar(x + width/2, sr_hp, width, label='High Pressure', color='#EA1A85', alpha=0.95)

# Add error bars for pressure SR
err_low = np.maximum(0, np.array(sr_hp) - np.array(ci_low))
err_high = np.maximum(0, np.array(ci_high) - np.array(sr_hp))
ax.errorbar(x + width/2, sr_hp, yerr=[err_low, err_high], fmt='none', ecolor='black', capsize=3, elinewidth=1.2)

ax.set_title('Top 10 Batters: Strike Rate (Normal vs High Pressure) with 90% Empirical CI', fontsize=11, fontweight='bold', color=colors_rr['blue'])
ax.set_ylabel('Strike Rate (Runs / 100 Balls)', fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels([f"#{b['rank']} {n}" for b, n in zip(batters, names)], rotation=25, ha='right', fontsize=8.5)
ax.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'analysis', 'fig_bat_perf.png'))
plt.close(fig)

# 3. Top 10 Bowlers Economy: Normal vs High Pressure + Error Bars
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
bowlers = data['top_bowlers']
b_names = [b['name'].split()[-1] if len(b['name'].split())>1 else b['name'] for b in bowlers]
econ_hp = [b['econ_hp'] for b in bowlers]
econ_lp = [b['econ_lp'] for b in bowlers]
b_ci_low = [b['ci_low'] for b in bowlers]
b_ci_high = [b['ci_high'] for b in bowlers]
x = np.arange(len(b_names))

rects1 = ax.bar(x - width/2, econ_lp, width, label='Normal Match State', color='#1A2456', alpha=0.85)
rects2 = ax.bar(x + width/2, econ_hp, width, label='High Pressure (Lower = Better)', color='#EA1A85', alpha=0.95)

# Add error bars
b_err_low = np.maximum(0, np.array(econ_hp) - np.array(b_ci_low))
b_err_high = np.maximum(0, np.array(b_ci_high) - np.array(econ_hp))
ax.errorbar(x + width/2, econ_hp, yerr=[b_err_low, b_err_high], fmt='none', ecolor='black', capsize=3, elinewidth=1.2)

ax.set_title('Top 10 Bowlers: Economy Rate (Normal vs High Pressure) with 90% Empirical CI', fontsize=11, fontweight='bold', color=colors_rr['blue'])
ax.set_ylabel('Economy Rate (Runs / Over)', fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels([f"#{b['rank']} {n}" for b, n in zip(bowlers, b_names)], rotation=25, ha='right', fontsize=8.5)
ax.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'analysis', 'fig_bowl_perf.png'))
plt.close(fig)

# 4. Bootstrap Retention Stability Comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=300)
bat_stab = [b['top10_pct'] for b in batters]
bowl_stab = [b['top10_pct'] for b in bowlers]

ax1.barh([f"#{b['rank']} {n}" for b, n in zip(batters, names)][::-1], bat_stab[::-1], color='#EA1A85', alpha=0.85, height=0.6)
ax1.set_title('Batters: Top-10 Bootstrap Stability (%)', fontsize=10, fontweight='bold', color=colors_rr['blue'])
ax1.set_xlabel('% of 500 Resamples Retained in Top 10', fontsize=8.5)
ax1.set_xlim(0, 105)

ax2.barh([f"#{b['rank']} {n}" for b, n in zip(bowlers, b_names)][::-1], bowl_stab[::-1], color='#1A2456', alpha=0.85, height=0.6)
ax2.set_title('Bowlers: Top-10 Bootstrap Stability (%)', fontsize=10, fontweight='bold', color=colors_rr['blue'])
ax2.set_xlabel('% of 500 Resamples Retained in Top 10', fontsize=8.5)
ax2.set_xlim(0, 105)

plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'analysis', 'fig_bootstrap_stability.png'))
plt.close(fig)

print("Generated all 4 report chart figures successfully.")

