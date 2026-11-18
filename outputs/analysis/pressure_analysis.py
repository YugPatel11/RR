"""
SupeRR Selector Season 2 — Round 1
Pressure Performance Analysis for IPL 2027 Auction (Rajasthan Royals)

Complete, reproducible pipeline:
  python pressure_analysis.py

Reads from: ../../Data Pack/Data Pack/*.csv
Writes to:  ../  (JSON results, CSVs, intermediate files)

Author: RR War Room Analytics
Seed: 42 (all randomness is seeded)
"""

import pandas as pd
import numpy as np
import json
import os
import warnings
from collections import defaultdict

warnings.filterwarnings('ignore')
np.random.seed(42)

# ─── PATHS ───────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', '..', 'Data Pack', 'Data Pack')
OUT  = os.path.join(BASE, '..')

def load_data():
    """Load and return all CSV files."""
    print("Loading data...")
    bbb    = pd.read_csv(os.path.join(DATA, 'ball_by_ball.csv'))
    matches= pd.read_csv(os.path.join(DATA, 'matches.csv'))
    comp   = pd.read_csv(os.path.join(DATA, 'competitions.csv'))
    teams  = pd.read_csv(os.path.join(DATA, 'teams.csv'))
    ctpm   = pd.read_csv(os.path.join(DATA, 'competition_team_player_mapping.csv'))
    pe     = pd.read_csv(os.path.join(DATA, 'playing_eleven.csv'))
    return bbb, matches, comp, teams, ctpm, pe

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 0: DATA PREPARATION
# ═══════════════════════════════════════════════════════════════════════════════

def prepare_data(bbb, matches, comp, teams, ctpm):
    """
    Clean data, derive cumulative scores, targets, legal balls, etc.
    Returns enriched ball-by-ball DataFrame (innings 1 & 2 only).
    """
    print("Phase 0: Preparing data...")

    # IPL comp_ids
    IPL_COMP_IDS = [1358, 1715, 2193, 2725, 3298]

    # Add competition info to matches
    matches = matches.merge(comp[['comp_id', 'match_format', 'season']], on='comp_id', how='left')
    matches['is_ipl'] = matches['comp_id'].isin(IPL_COMP_IDS)

    # Filter to innings 1 & 2 only (exclude Super Overs)
    df = bbb[bbb['innings'].isin([1, 2])].copy()
    print(f"  Balls after removing Super Overs: {len(df)}")

    # Remove matches with no result / abandoned
    valid_matches = matches[matches['result'].notna() & ~matches['result'].str.contains('No Result|Abandoned|No result', case=False, na=False)]
    df = df[df['match_id'].isin(valid_matches['match_id'])]
    print(f"  Balls after removing no-result matches: {len(df)}")

    # Merge match info
    df = df.merge(matches[['match_id', 'comp_id', 'match_format', 'season', 'is_ipl',
                           'stage', 'knock_out', 'win_team_id', 'result',
                           'first_inn_revised_overs', 'second_inn_revised_overs',
                           'revised_target']], on='match_id', how='left')

    # ─── Derive total runs per ball ───
    df['extras1_runs'] = df['extras1_runs'].fillna(0).astype(int)
    df['extras_2_runs'] = df['extras_2_runs'].fillna(0).astype(int)
    df['total_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']

    # ─── Legal ball flag ───
    # Legal ball = not a wide and not a no-ball (Overstep)
    df['is_legal'] = ~df['extras_type'].isin(['wide', 'Overstep'])

    # ─── Bowler-chargeable runs ───
    # Don't charge byes or leg-byes to the bowler
    df['bowler_runs'] = df['runs'].copy()  # bat runs always charged
    # Add wides and no-balls (extras1_runs for wide/Overstep)
    wide_or_nb = df['extras_type'].isin(['wide', 'Overstep'])
    df.loc[wide_or_nb, 'bowler_runs'] = df.loc[wide_or_nb, 'bowler_runs'] + df.loc[wide_or_nb, 'extras1_runs']
    # extras_2_runs on wide/Overstep are also bowler's fault (runs scored off them)
    df.loc[wide_or_nb, 'bowler_runs'] = df.loc[wide_or_nb, 'bowler_runs'] + df.loc[wide_or_nb, 'extras_2_runs']
    # byes/legbyes: extras1_runs NOT charged to bowler

    # ─── Bowler wicket flag ───
    # Don't credit run-outs, retired-out, obstructing-the-field to bowler
    NON_BOWLER_DISMISSALS = ['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field']
    df['bowler_wicket'] = (df['is_wicket'] == True) & (~df['dismissal_type'].isin(NON_BOWLER_DISMISSALS))

    # ─── Sort by match, innings, ball sequence ───
    df = df.sort_values(['match_id', 'innings', 'innings_ball_num']).reset_index(drop=True)

    # ─── Cumulative runs and wickets per innings ───
    # Group by match_id + innings
    grp = df.groupby(['match_id', 'innings'])

    df['cum_total_runs'] = grp['total_runs'].cumsum()
    df['cum_wickets'] = grp['is_wicket'].cumsum()

    # Runs/wickets BEFORE this ball (state entering the ball)
    df['runs_before'] = df['cum_total_runs'] - df['total_runs']
    df['wkts_before'] = df['cum_wickets'] - df['is_wicket'].astype(int)
    # Fix: wicket happens on the ball, so wkts_before should not count current ball
    # Actually, cum_wickets includes current ball, so:
    df['wkts_before'] = df['cum_wickets'].shift(1, fill_value=0)
    # Reset at innings boundaries
    mask = df.groupby(['match_id', 'innings']).cumcount() == 0
    df.loc[mask, 'wkts_before'] = 0

    # ─── Legal balls count ───
    df['legal_ball_count'] = grp['is_legal'].cumsum()
    df['legal_balls_before'] = df['legal_ball_count'] - df['is_legal'].astype(int)
    df.loc[mask, 'legal_balls_before'] = 0

    # ─── Over number (1-indexed) ───
    # overid is already 1-indexed

    # ─── Phase classification ───
    df['phase'] = 'middle'
    df.loc[df['overid'] <= 6, 'phase'] = 'powerplay'
    df.loc[df['overid'] >= 17, 'phase'] = 'death'

    # ─── First innings totals (for target calculation) ───
    first_inn_totals = df[df['innings'] == 1].groupby('match_id').agg(
        first_inn_total=('total_runs', 'sum'),
        first_inn_legal_balls=('is_legal', 'sum')
    ).reset_index()

    df = df.merge(first_inn_totals, on='match_id', how='left')

    # ─── Target for 2nd innings ───
    # Use revised_target if present, else first_inn_total + 1
    df['target'] = np.where(
        (df['innings'] == 2) & df['revised_target'].notna(),
        df['revised_target'],
        np.where(df['innings'] == 2, df['first_inn_total'] + 1, np.nan)
    )

    # ─── Max overs for 2nd innings ───
    df['max_overs_2nd'] = np.where(
        df['second_inn_revised_overs'].notna(),
        df['second_inn_revised_overs'],
        20.0
    )
    df['max_balls_2nd'] = df['max_overs_2nd'] * 6

    # ─── Balls remaining (2nd innings) ───
    df['balls_remaining'] = np.where(
        df['innings'] == 2,
        df['max_balls_2nd'] - df['legal_balls_before'],
        np.nan
    )

    # ─── Runs needed (2nd innings) ───
    df['runs_needed'] = np.where(
        df['innings'] == 2,
        df['target'] - df['runs_before'],
        np.nan
    )

    # ─── Required run rate (2nd innings) ───
    df['rrr'] = np.where(
        (df['innings'] == 2) & (df['balls_remaining'] > 0),
        df['runs_needed'] / df['balls_remaining'] * 6,  # per over
        np.nan
    )

    # ─── Current run rate ───
    df['crr'] = np.where(
        df['legal_balls_before'] > 0,
        df['runs_before'] / df['legal_balls_before'] * 6,
        0
    )

    # ─── Wickets in hand (2nd innings) ───
    df['wkts_in_hand'] = 10 - df['wkts_before']

    # ─── Knockout / high-stakes match flag ───
    df['is_knockout'] = df['stage'].isin(['Final', 'Qualifier', 'Eliminator', 'Semi Final']).astype(int)

    # ─── Build team strength ratings (from win records) ───
    team_strength = _build_team_strength(matches)
    df = df.merge(team_strength.rename('opp_strength'), left_on='bowling_team_id', right_index=True, how='left')
    df['opp_strength'] = df['opp_strength'].fillna(0.5)
    # For bowlers, opposition is the batting team
    df = df.merge(team_strength.rename('bat_opp_strength'), left_on='batting_team_id', right_index=True, how='left')
    df['bat_opp_strength'] = df['bat_opp_strength'].fillna(0.5)

    print(f"  Final prepared dataset: {len(df)} balls, {df['match_id'].nunique()} matches")
    return df, matches, team_strength


def _build_team_strength(matches):
    """
    Simple team strength: win% across all matches, shrunk toward 0.5.
    """
    records = []
    for _, row in matches.iterrows():
        if pd.isna(row['win_team_id']):
            continue
        # home team
        records.append({'team_id': row['home_team_id'], 'win': 1 if row['win_team_id'] == row['home_team_id'] else 0})
        records.append({'team_id': row['away_team_id'], 'win': 1 if row['win_team_id'] == row['away_team_id'] else 0})

    tdf = pd.DataFrame(records)
    ts = tdf.groupby('team_id').agg(wins=('win', 'sum'), total=('win', 'count'))
    # Empirical Bayes shrinkage toward 0.5
    prior_n = 10  # prior equivalent of 10 matches at 50%
    ts['strength'] = (ts['wins'] + prior_n * 0.5) / (ts['total'] + prior_n)
    return ts['strength']


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: PRESSURE INDEX
# ═══════════════════════════════════════════════════════════════════════════════

def build_par_curves(df):
    """
    Build par score curves: expected cumulative runs at each (over, wickets_lost) state.
    Uses 1st innings data across all matches.
    """
    print("  Building par score curves from 1st innings data...")
    inn1 = df[df['innings'] == 1].copy()

    # Bin: (overid, wkts_before) → mean runs_before at start of that ball
    par = inn1.groupby(['overid', 'wkts_before'])['runs_before'].mean().reset_index()
    par.columns = ['overid', 'wkts_before', 'par_score']

    # Create a lookup dict
    par_dict = {}
    for _, row in par.iterrows():
        par_dict[(int(row['overid']), int(row['wkts_before']))] = row['par_score']

    return par_dict


def compute_pressure_index(df, par_dict):
    """
    Ball-level Pressure Index (0-1) combining multiple signals.

    2nd innings signals:
      - Required run rate pressure: (RRR - 6) / 12, clipped to [0,1]
      - Resource depletion: (balls_used / max_balls) * (wickets_lost / 10)
      - Crisis: RRR > 10 AND wkts_in_hand <= 4 → bonus
      - Runs per ball needed: runs_needed / balls_remaining, clipped

    1st innings signals:
      - Score deficit vs par: (par_score - actual_score) / par_score, clipped
      - Collapse detection: 2+ wickets in last 18 balls (3 overs)
      - New batter under deficit

    Universal signals:
      - Death-over leverage: overs 17-20 get a boost
      - Knockout match bonus
      - Close-finish bonus (derived from result margin)

    All components combined with weights, then min-max scaled to [0,1].
    """
    print("Phase 2: Computing Pressure Index...")

    n = len(df)
    pressure = np.zeros(n)

    # ─── Pre-compute signals ───
    overid = df['overid'].values
    innings = df['innings'].values
    wkts_before = df['wkts_before'].values
    runs_before = df['runs_before'].values
    rrr = df['rrr'].values
    balls_remaining = df['balls_remaining'].values
    runs_needed = df['runs_needed'].values
    wkts_in_hand = df['wkts_in_hand'].values
    is_knockout = df['is_knockout'].values
    legal_balls_before = df['legal_balls_before'].values
    max_balls_2nd = df['max_balls_2nd'].values

    # ─── Close finish detection ───
    # Parse result field for margin
    close_finish = _compute_close_finish(df)

    # ─── Collapse detection ───
    collapse = _compute_collapse(df)

    # ─── Par score deficit (1st innings) ───
    par_deficit = np.zeros(n)
    for i in range(n):
        if innings[i] == 1:
            key = (int(overid[i]), min(int(wkts_before[i]), 9))
            par = par_dict.get(key, runs_before[i])
            if par > 0:
                deficit = (par - runs_before[i]) / max(par, 1)
                par_deficit[i] = np.clip(deficit, 0, 1)

    # ─── Combine signals ───
    for i in range(n):
        p = 0.0

        if innings[i] == 2:
            # Required run rate pressure
            if not np.isnan(rrr[i]):
                rrr_p = np.clip((rrr[i] - 6.0) / 12.0, 0, 1)
                p += 0.30 * rrr_p

            # Runs per ball needed
            if not np.isnan(runs_needed[i]) and not np.isnan(balls_remaining[i]) and balls_remaining[i] > 0:
                rpb = runs_needed[i] / balls_remaining[i]
                rpb_p = np.clip((rpb - 1.0) / 2.0, 0, 1)
                p += 0.20 * rpb_p

            # Resource depletion
            if not np.isnan(balls_remaining[i]):
                max_b = max_balls_2nd[i] if not np.isnan(max_balls_2nd[i]) else 120
                balls_used_frac = legal_balls_before[i] / max(max_b, 1)
                wkt_frac = (10 - wkts_in_hand[i]) / 10.0
                resource_p = balls_used_frac * wkt_frac
                p += 0.10 * np.clip(resource_p, 0, 1)

            # Crisis: RRR > 10 AND <= 4 wickets
            if not np.isnan(rrr[i]) and rrr[i] > 10 and wkts_in_hand[i] <= 4:
                p += 0.10

        elif innings[i] == 1:
            # Par deficit
            p += 0.25 * par_deficit[i]

            # Collapse
            p += 0.15 * collapse[i]

        # ─── Universal signals ───
        # Death-over leverage
        if overid[i] >= 17:
            death_boost = (overid[i] - 16) / 4.0  # 0.25 for over 17, up to 1.0 for over 20
            p += 0.10 * death_boost

        # Knockout match
        p += 0.05 * is_knockout[i]

        # Close finish
        p += 0.10 * close_finish[i]

        pressure[i] = p

    # ─── Normalize to [0, 1] ───
    p_min, p_max = np.nanmin(pressure), np.nanmax(pressure)
    if p_max > p_min:
        pressure = (pressure - p_min) / (p_max - p_min)

    df = df.copy()
    df['pressure_index'] = pressure

    # ─── Classify pressure levels ───
    df['is_high_pressure'] = df['pressure_index'] >= df['pressure_index'].quantile(0.75)
    df['pressure_bin'] = pd.cut(df['pressure_index'], bins=[0, 0.25, 0.5, 0.75, 1.0],
                                labels=['low', 'medium', 'high', 'very_high'], include_lowest=True)

    print(f"  Pressure Index computed. Mean={pressure.mean():.3f}, Std={pressure.std():.3f}")
    print(f"  High-pressure balls (top 25%): {df['is_high_pressure'].sum()} ({df['is_high_pressure'].mean()*100:.1f}%)")

    return df


def _compute_close_finish(df):
    """Detect close finishes from result text. Returns array of 0/1 per ball."""
    close = np.zeros(len(df))
    result_map = {}
    for _, row in df[['match_id', 'result']].drop_duplicates().iterrows():
        res = str(row['result'])
        is_close = 0
        # "Won by X runs" - close if X <= 15
        if 'run' in res.lower():
            try:
                margin = int(''.join(filter(str.isdigit, res.split('by')[-1].split('run')[0].strip())))
                if margin <= 15:
                    is_close = 1
            except:
                pass
        # "Won by X wickets" - close if X <= 3
        elif 'wicket' in res.lower():
            try:
                margin = int(''.join(filter(str.isdigit, res.split('by')[-1].split('wicket')[0].strip())))
                if margin <= 3:
                    is_close = 1
            except:
                pass
        # Super Over
        elif 'super over' in res.lower() or 'tie' in res.lower():
            is_close = 1
        result_map[row['match_id']] = is_close

    close = df['match_id'].map(result_map).fillna(0).values
    return close


def _compute_collapse(df):
    """Detect collapse situations: 2+ wickets in last 18 legal balls. Returns 0-1 per ball.
    Vectorized with searchsorted for speed."""
    collapse = np.zeros(len(df))
    for (mid, inn), grp in df.groupby(['match_id', 'innings']):
        idx = grp.index.values
        wkt_cum = grp['is_wicket'].astype(int).cumsum().values
        legal_cum = grp['is_legal'].astype(int).cumsum().values
        n = len(idx)
        for j in range(n):
            target_legal = legal_cum[j] - 18
            if target_legal <= 0:
                wkts_in_window = wkt_cum[j]
            else:
                start_j = np.searchsorted(legal_cum[:j+1], target_legal, side='right')
                wkts_in_window = wkt_cum[j] - (wkt_cum[start_j - 1] if start_j > 0 else 0)
            if wkts_in_window >= 2:
                collapse[idx[j]] = min(wkts_in_window / 4.0, 1.0)
    return collapse


def validate_pressure_index(df):
    """
    Phase 2 validation: show that high-pressure situations differ measurably
    from low-pressure ones.
    """
    print("\n  Validating Pressure Index...")

    results = {}

    # Compare high vs low pressure bins
    for label, grp in df.groupby('pressure_bin', observed=True):
        legal = grp[grp['is_legal']]
        sr = legal['runs'].mean() * 100 if len(legal) > 0 else 0
        dot_pct = (legal['runs'] == 0).mean() * 100 if len(legal) > 0 else 0
        wkt_rate = grp['is_wicket'].mean() * 100
        boundary_pct = ((grp['is_four'] == True) | (grp['is_six'] == True)).mean() * 100
        results[label] = {
            'balls': len(grp),
            'strike_rate': round(sr, 1),
            'dot_pct': round(dot_pct, 1),
            'wicket_rate': round(wkt_rate, 2),
            'boundary_pct': round(boundary_pct, 1)
        }

    print("\n  Pressure validation (high vs low pressure):")
    print(f"  {'Bin':<12} {'Balls':>8} {'SR':>8} {'Dot%':>8} {'Wkt%':>8} {'Bnd%':>8}")
    for label in ['low', 'medium', 'high', 'very_high']:
        if label in results:
            r = results[label]
            print(f"  {label:<12} {r['balls']:>8} {r['strike_rate']:>8.1f} {r['dot_pct']:>8.1f} {r['wicket_rate']:>8.2f} {r['boundary_pct']:>8.1f}")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: PERFORMANCE MEASUREMENT
# ═══════════════════════════════════════════════════════════════════════════════

def build_expected_models(df):
    """
    Build context-adjusted expectations:
    - Expected runs per legal ball given (over, wickets_lost, innings, phase, pace_or_spin)
    - Expected wicket probability per ball given same context
    """
    print("\nPhase 3: Building expected performance models...")

    legal = df[df['is_legal']].copy()

    # Expected batting runs per ball
    bat_exp = legal.groupby(['overid', 'wkts_before', 'innings', 'pace_or_spin']).agg(
        exp_runs=('runs', 'mean'),
        exp_wkt=('is_wicket', 'mean'),
        n_balls=('runs', 'count')
    ).reset_index()

    # Shrink toward global mean where small samples
    global_runs = legal['runs'].mean()
    global_wkt = legal['is_wicket'].mean()
    prior_n = 50

    bat_exp['exp_runs_shrunk'] = (bat_exp['exp_runs'] * bat_exp['n_balls'] + global_runs * prior_n) / (bat_exp['n_balls'] + prior_n)
    bat_exp['exp_wkt_shrunk'] = (bat_exp['exp_wkt'] * bat_exp['n_balls'] + global_wkt * prior_n) / (bat_exp['n_balls'] + prior_n)

    # Build lookup
    exp_dict = {}
    for _, row in bat_exp.iterrows():
        key = (int(row['overid']), int(row['wkts_before']), int(row['innings']),
               row['pace_or_spin'] if pd.notna(row['pace_or_spin']) else 'Pace')
        exp_dict[key] = (row['exp_runs_shrunk'], row['exp_wkt_shrunk'])

    # Bowling expected: runs conceded per ball
    bowl_exp = legal.groupby(['overid', 'wkts_before', 'innings']).agg(
        exp_bowl_runs=('bowler_runs', 'mean'),
        exp_bowl_wkt=('bowler_wicket', 'mean'),
        n_balls=('bowler_runs', 'count')
    ).reset_index()

    global_bowl_runs = legal['bowler_runs'].mean()
    global_bowl_wkt = legal['bowler_wicket'].mean()
    bowl_exp['exp_bowl_runs_shrunk'] = (bowl_exp['exp_bowl_runs'] * bowl_exp['n_balls'] + global_bowl_runs * prior_n) / (bowl_exp['n_balls'] + prior_n)
    bowl_exp['exp_bowl_wkt_shrunk'] = (bowl_exp['exp_bowl_wkt'] * bowl_exp['n_balls'] + global_bowl_wkt * prior_n) / (bowl_exp['n_balls'] + prior_n)

    bowl_dict = {}
    for _, row in bowl_exp.iterrows():
        key = (int(row['overid']), int(row['wkts_before']), int(row['innings']))
        bowl_dict[key] = (row['exp_bowl_runs_shrunk'], row['exp_bowl_wkt_shrunk'])

    return exp_dict, bowl_dict, global_runs, global_wkt, global_bowl_runs, global_bowl_wkt


def compute_batter_metrics(df, exp_dict, global_runs, global_wkt):
    """
    Compute per-batter metrics under pressure vs baseline.
    """
    print("  Computing batter metrics...")

    legal = df[df['is_legal']].copy()

    # Vectorized lookup of expected runs for each ball
    overids = legal['overid'].astype(int).values
    wkts = np.minimum(legal['wkts_before'].astype(int).values, 9)
    inngs = legal['innings'].astype(int).values
    ps = legal['pace_or_spin'].fillna('Pace').values

    exp_r = np.zeros(len(legal))
    exp_w = np.zeros(len(legal))
    for i in range(len(legal)):
        key = (overids[i], wkts[i], inngs[i], ps[i])
        e = exp_dict.get(key, (global_runs, global_wkt))
        exp_r[i] = e[0]
        exp_w[i] = e[1]

    legal['exp_runs'] = exp_r
    legal['exp_wkt'] = exp_w
    legal['runs_above_exp'] = legal['runs'] - legal['exp_runs']

    # Aggregate per batter
    batters = {}
    for hp_label in [True, False]:
        grp = legal[legal['is_high_pressure'] == hp_label]
        agg = grp.groupby('striker_id').agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
            runs_above_exp=('runs_above_exp', 'sum'),
            fours=('is_four', 'sum'),
            sixes=('is_six', 'sum'),
            dots=('runs', lambda x: (x == 0).sum()),
            wickets=('is_wicket', 'sum'),
            matches=('match_id', 'nunique'),
            exp_runs_total=('exp_runs', 'sum'),
        ).reset_index()

        agg['strike_rate'] = agg['runs'] / agg['balls'] * 100
        agg['boundary_pct'] = (agg['fours'] + agg['sixes']) / agg['balls'] * 100
        agg['dot_pct'] = agg['dots'] / agg['balls'] * 100
        agg['balls_per_dismissal'] = agg['balls'] / agg['wickets'].replace(0, np.nan)
        agg['runs_above_exp_per_ball'] = agg['runs_above_exp'] / agg['balls']

        suffix = '_hp' if hp_label else '_lp'
        agg = agg.rename(columns={c: c + suffix for c in agg.columns if c != 'striker_id'})
        if hp_label:
            batters['hp'] = agg
        else:
            batters['lp'] = agg

    # Merge
    bat = batters['hp'].merge(batters['lp'], on='striker_id', how='outer')

    return bat, legal


def compute_bowler_metrics(df, bowl_dict, global_bowl_runs, global_bowl_wkt):
    """
    Compute per-bowler metrics under pressure vs baseline.
    """
    print("  Computing bowler metrics...")

    legal = df[df['is_legal']].copy()

    # Vectorized lookup
    overids = legal['overid'].astype(int).values
    wkts = np.minimum(legal['wkts_before'].astype(int).values, 9)
    inngs = legal['innings'].astype(int).values

    exp_br = np.zeros(len(legal))
    exp_bw = np.zeros(len(legal))
    for i in range(len(legal)):
        key = (overids[i], wkts[i], inngs[i])
        e = bowl_dict.get(key, (global_bowl_runs, global_bowl_wkt))
        exp_br[i] = e[0]
        exp_bw[i] = e[1]

    legal['exp_bowl_runs'] = exp_br
    legal['exp_bowl_wkt'] = exp_bw
    legal['runs_below_exp'] = legal['exp_bowl_runs'] - legal['bowler_runs']  # positive = good for bowler
    legal['wkt_above_exp'] = legal['bowler_wicket'].astype(int) - legal['exp_bowl_wkt']

    bowlers = {}
    for hp_label in [True, False]:
        grp = legal[legal['is_high_pressure'] == hp_label]
        agg = grp.groupby('bowler_id').agg(
            balls=('bowler_runs', 'count'),
            runs_conceded=('bowler_runs', 'sum'),
            runs_below_exp=('runs_below_exp', 'sum'),
            wkt_above_exp=('wkt_above_exp', 'sum'),
            wickets=('bowler_wicket', 'sum'),
            dots=('bowler_runs', lambda x: (x == 0).sum()),
            fours_conceded=('is_four', 'sum'),
            sixes_conceded=('is_six', 'sum'),
            matches=('match_id', 'nunique'),
            exp_runs_total=('exp_bowl_runs', 'sum'),
        ).reset_index()

        agg['economy'] = agg['runs_conceded'] / agg['balls'] * 6
        agg['dot_pct'] = agg['dots'] / agg['balls'] * 100
        agg['boundary_conceded_pct'] = (agg['fours_conceded'] + agg['sixes_conceded']) / agg['balls'] * 100
        agg['wicket_rate'] = agg['wickets'] / agg['balls'] * 100
        agg['runs_below_exp_per_ball'] = agg['runs_below_exp'] / agg['balls']

        suffix = '_hp' if hp_label else '_lp'
        agg = agg.rename(columns={c: c + suffix for c in agg.columns if c != 'bowler_id'})
        if hp_label:
            bowlers['hp'] = agg
        else:
            bowlers['lp'] = agg

    bowl = bowlers['hp'].merge(bowlers['lp'], on='bowler_id', how='outer')

    return bowl, legal


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3b: PRESSURE RELIABILITY RATING
# ═══════════════════════════════════════════════════════════════════════════════

def compute_batter_rating(bat, df, ctpm, min_hp_balls=50, min_matches=10):
    """
    Composite Pressure Reliability Rating for batters.
    Components:
      1. Pressure Impact (runs above expected per ball under HP) — 40%
      2. SR uplift under pressure vs baseline — 20%
      3. Boundary% under pressure — 15%
      4. Consistency (share of HP matches with positive impact) — 25%

    Empirical Bayes shrinkage applied.
    """
    print("  Computing batter Pressure Reliability Rating...")

    # Filter eligible
    eligible = bat[
        (bat['balls_hp'].fillna(0) >= min_hp_balls) &
        (bat['matches_hp'].fillna(0) >= min_matches)
    ].copy()

    print(f"  Eligible batters (>={min_hp_balls} HP balls, >={min_matches} HP matches): {len(eligible)}")

    if len(eligible) == 0:
        print("  WARNING: No eligible batters. Lowering thresholds.")
        min_hp_balls = 30
        min_matches = 5
        eligible = bat[
            (bat['balls_hp'].fillna(0) >= min_hp_balls) &
            (bat['matches_hp'].fillna(0) >= min_matches)
        ].copy()
        print(f"  Eligible batters with relaxed thresholds: {len(eligible)}")

    # ─── 1. Pressure Impact ───
    # Runs above expected per ball under HP, shrunk
    prior_mu = eligible['runs_above_exp_per_ball_hp'].median()
    prior_n = 30
    eligible['impact_raw'] = eligible['runs_above_exp_per_ball_hp']
    eligible['impact_shrunk'] = (
        eligible['impact_raw'] * eligible['balls_hp'] + prior_mu * prior_n
    ) / (eligible['balls_hp'] + prior_n)

    # ─── 2. SR uplift ───
    eligible['sr_hp'] = eligible['strike_rate_hp'].fillna(0)
    eligible['sr_lp'] = eligible['strike_rate_lp'].fillna(eligible['sr_hp'])
    eligible['sr_uplift'] = eligible['sr_hp'] - eligible['sr_lp']

    # ─── 3. Boundary% under pressure ───
    eligible['bnd_hp'] = eligible['boundary_pct_hp'].fillna(0)

    # ─── 4. Consistency ───
    # Compute per-match impact under HP
    consistency = _compute_batter_consistency(df, eligible['striker_id'].tolist())
    eligible = eligible.merge(consistency, on='striker_id', how='left')
    eligible['consistency'] = eligible['consistency'].fillna(0.5)

    # ─── Normalize each component to [0, 1] ───
    for col in ['impact_shrunk', 'sr_uplift', 'bnd_hp', 'consistency']:
        mn, mx = eligible[col].min(), eligible[col].max()
        if mx > mn:
            eligible[col + '_norm'] = (eligible[col] - mn) / (mx - mn)
        else:
            eligible[col + '_norm'] = 0.5

    # ─── Weighted composite ───
    eligible['pressure_rating'] = (
        0.40 * eligible['impact_shrunk_norm'] +
        0.20 * eligible['sr_uplift_norm'] +
        0.15 * eligible['bnd_hp_norm'] +
        0.25 * eligible['consistency_norm']
    )

    # ─── Add player names ───
    names = ctpm[['player_id', 'player_name']].drop_duplicates('player_id')
    eligible = eligible.merge(names, left_on='striker_id', right_on='player_id', how='left')

    # Add team names (use most recent competition)
    team_names = ctpm.sort_values('comp_id', ascending=False).drop_duplicates('player_id')[['player_id', 'team_name']]
    eligible = eligible.merge(team_names, left_on='striker_id', right_on='player_id', how='left', suffixes=('', '_team'))

    eligible = eligible.sort_values('pressure_rating', ascending=False).reset_index(drop=True)

    return eligible


def _compute_batter_consistency(df, batter_ids):
    """
    Consistency: share of high-pressure matches where the batter had positive
    runs-above-expected per ball.
    """
    hp = df[(df['is_high_pressure']) & (df['is_legal']) & (df['striker_id'].isin(batter_ids))].copy()

    match_perf = hp.groupby(['striker_id', 'match_id']).agg(
        runs=('runs', 'sum'),
        balls=('runs', 'count'),
        exp_runs=('runs', 'mean'),  # placeholder, we'll recompute
    ).reset_index()

    # Positive impact = scored above average (SR > 120 in HP context is decent)
    match_perf['sr'] = match_perf['runs'] / match_perf['balls'] * 100
    match_perf['positive'] = (match_perf['sr'] > 110).astype(int)  # threshold: SR > 110 under HP

    consistency = match_perf.groupby('striker_id').agg(
        positive_matches=('positive', 'sum'),
        total_hp_matches=('positive', 'count'),
        sr_std=('sr', 'std')
    ).reset_index()

    consistency['consistency'] = consistency['positive_matches'] / consistency['total_hp_matches']
    # Also penalize high variance
    sr_std_median = consistency['sr_std'].median()
    consistency['consistency'] = consistency['consistency'] * (1 - 0.3 * np.clip(consistency['sr_std'] / (sr_std_median * 2), 0, 1))

    return consistency[['striker_id', 'consistency']]


def compute_bowler_rating(bowl, df, ctpm, min_hp_balls=50, min_matches=10):
    """
    Composite Pressure Reliability Rating for bowlers.
    Components:
      1. Economy below expected under HP (runs saved per ball) — 35%
      2. Wicket rate uplift under pressure — 25%
      3. Dot ball% under pressure — 15%
      4. Consistency — 25%
    """
    print("  Computing bowler Pressure Reliability Rating...")

    eligible = bowl[
        (bowl['balls_hp'].fillna(0) >= min_hp_balls) &
        (bowl['matches_hp'].fillna(0) >= min_matches)
    ].copy()

    print(f"  Eligible bowlers (>={min_hp_balls} HP balls, >={min_matches} HP matches): {len(eligible)}")

    if len(eligible) == 0:
        min_hp_balls = 30
        min_matches = 5
        eligible = bowl[
            (bowl['balls_hp'].fillna(0) >= min_hp_balls) &
            (bowl['matches_hp'].fillna(0) >= min_matches)
        ].copy()
        print(f"  Eligible bowlers with relaxed thresholds: {len(eligible)}")

    # 1. Runs saved per ball (positive = good)
    prior_mu = eligible['runs_below_exp_per_ball_hp'].median()
    prior_n = 30
    eligible['econ_impact_shrunk'] = (
        eligible['runs_below_exp_per_ball_hp'] * eligible['balls_hp'] + prior_mu * prior_n
    ) / (eligible['balls_hp'] + prior_n)

    # 2. Wicket rate under HP
    eligible['wkt_rate_hp_val'] = eligible['wicket_rate_hp'].fillna(0)

    # 3. Dot ball %
    eligible['dot_hp_val'] = eligible['dot_pct_hp'].fillna(0)

    # 4. Consistency
    consistency = _compute_bowler_consistency(df, eligible['bowler_id'].tolist())
    eligible = eligible.merge(consistency, on='bowler_id', how='left')
    eligible['consistency'] = eligible['consistency'].fillna(0.5)

    # Normalize
    for col in ['econ_impact_shrunk', 'wkt_rate_hp_val', 'dot_hp_val', 'consistency']:
        mn, mx = eligible[col].min(), eligible[col].max()
        if mx > mn:
            eligible[col + '_norm'] = (eligible[col] - mn) / (mx - mn)
        else:
            eligible[col + '_norm'] = 0.5

    eligible['pressure_rating'] = (
        0.35 * eligible['econ_impact_shrunk_norm'] +
        0.25 * eligible['wkt_rate_hp_val_norm'] +
        0.15 * eligible['dot_hp_val_norm'] +
        0.25 * eligible['consistency_norm']
    )

    # Add names
    names = ctpm[['player_id', 'player_name']].drop_duplicates('player_id')
    eligible = eligible.merge(names, left_on='bowler_id', right_on='player_id', how='left')
    team_names = ctpm.sort_values('comp_id', ascending=False).drop_duplicates('player_id')[['player_id', 'team_name']]
    eligible = eligible.merge(team_names, left_on='bowler_id', right_on='player_id', how='left', suffixes=('', '_team'))

    eligible = eligible.sort_values('pressure_rating', ascending=False).reset_index(drop=True)

    return eligible


def _compute_bowler_consistency(df, bowler_ids):
    """Consistency: share of HP matches where bowler had below-average economy."""
    hp = df[(df['is_high_pressure']) & (df['is_legal']) & (df['bowler_id'].isin(bowler_ids))].copy()

    match_perf = hp.groupby(['bowler_id', 'match_id']).agg(
        runs_conceded=('bowler_runs', 'sum'),
        balls=('bowler_runs', 'count'),
        wickets=('bowler_wicket', 'sum'),
    ).reset_index()

    match_perf['econ'] = match_perf['runs_conceded'] / match_perf['balls'] * 6
    match_perf['positive'] = (match_perf['econ'] < 9.0).astype(int)  # Below 9 RPO under HP = decent

    consistency = match_perf.groupby('bowler_id').agg(
        positive_matches=('positive', 'sum'),
        total_hp_matches=('positive', 'count'),
        econ_std=('econ', 'std')
    ).reset_index()

    consistency['consistency'] = consistency['positive_matches'] / consistency['total_hp_matches']
    econ_std_median = consistency['econ_std'].median()
    if econ_std_median > 0:
        consistency['consistency'] = consistency['consistency'] * (1 - 0.3 * np.clip(consistency['econ_std'] / (econ_std_median * 2), 0, 1))

    return consistency[['bowler_id', 'consistency']]


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4 & 5: BOOTSTRAP CONFIDENCE & RELIABILITY
# ═══════════════════════════════════════════════════════════════════════════════

def bootstrap_rankings(df, eligible_bat, eligible_bowl, ctpm, n_boot=500):
    """
    Bootstrap confidence intervals by resampling matches.
    Returns: for each player, CI on rating and P(stays in top 10).
    """
    print("\nPhase 5: Bootstrap reliability analysis...")

    bat_ids = eligible_bat['striker_id'].tolist()[:30]  # top 30 candidates
    bowl_ids = eligible_bowl['bowler_id'].tolist()[:30]

    match_ids = df['match_id'].unique()
    n_matches = len(match_ids)

    bat_ratings_boot = defaultdict(list)
    bowl_ratings_boot = defaultdict(list)

    legal = df[df['is_legal']].copy()

    for b in range(n_boot):
        if b % 100 == 0:
            print(f"    Bootstrap {b}/{n_boot}...")

        # Resample matches
        sampled = np.random.choice(match_ids, size=n_matches, replace=True)
        boot_df = legal[legal['match_id'].isin(set(sampled))]

        # Quick batter ratings
        for sid in bat_ids:
            hp = boot_df[(boot_df['striker_id'] == sid) & (boot_df['is_high_pressure'])]
            if len(hp) < 10:
                bat_ratings_boot[sid].append(np.nan)
                continue
            sr = hp['runs'].sum() / len(hp) * 100
            bat_ratings_boot[sid].append(sr)

        # Quick bowler ratings
        for bid in bowl_ids:
            hp = boot_df[(boot_df['bowler_id'] == bid) & (boot_df['is_high_pressure'])]
            if len(hp) < 10:
                bowl_ratings_boot[bid].append(np.nan)
                continue
            econ = hp['bowler_runs'].sum() / len(hp) * 6
            bowl_ratings_boot[bid].append(econ)

    # Compute CIs and top-10 stability
    bat_ci = {}
    for sid in bat_ids:
        vals = [v for v in bat_ratings_boot[sid] if not np.isnan(v)]
        if len(vals) > 10:
            bat_ci[sid] = {
                'ci_low': round(np.percentile(vals, 5), 1),
                'ci_high': round(np.percentile(vals, 95), 1),
                'median': round(np.median(vals), 1),
            }
        else:
            bat_ci[sid] = {'ci_low': 0, 'ci_high': 0, 'median': 0}

    bowl_ci = {}
    for bid in bowl_ids:
        vals = [v for v in bowl_ratings_boot[bid] if not np.isnan(v)]
        if len(vals) > 10:
            bowl_ci[bid] = {
                'ci_low': round(np.percentile(vals, 5), 1),
                'ci_high': round(np.percentile(vals, 95), 1),
                'median': round(np.median(vals), 1),
            }
        else:
            bowl_ci[bid] = {'ci_low': 0, 'ci_high': 0, 'median': 0}

    # Top-10 stability: how often each player is in top 10 across bootstraps
    bat_top10_pct = {}
    for b in range(n_boot):
        # Rank by SR (higher = better for batters)
        boot_vals = {}
        for sid in bat_ids:
            v = bat_ratings_boot[sid][b]
            if not np.isnan(v):
                boot_vals[sid] = v
        ranked = sorted(boot_vals.keys(), key=lambda x: boot_vals[x], reverse=True)[:10]
        for sid in ranked:
            bat_top10_pct[sid] = bat_top10_pct.get(sid, 0) + 1

    for sid in bat_top10_pct:
        bat_top10_pct[sid] = round(bat_top10_pct[sid] / n_boot * 100, 1)

    bowl_top10_pct = {}
    for b in range(n_boot):
        boot_vals = {}
        for bid in bowl_ids:
            v = bowl_ratings_boot[bid][b]
            if not np.isnan(v):
                boot_vals[bid] = v
        ranked = sorted(boot_vals.keys(), key=lambda x: boot_vals[x])[:10]  # lower econ = better
        for bid in ranked:
            bowl_top10_pct[bid] = bowl_top10_pct.get(bid, 0) + 1

    for bid in bowl_top10_pct:
        bowl_top10_pct[bid] = round(bowl_top10_pct[bid] / n_boot * 100, 1)

    return bat_ci, bowl_ci, bat_top10_pct, bowl_top10_pct


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 6: FINAL OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

def generate_outputs(eligible_bat, eligible_bowl, bat_ci, bowl_ci,
                     bat_top10_pct, bowl_top10_pct, pressure_validation, df, comp):
    """
    Generate final ranked lists, JSON for HTML, and CSV.
    """
    print("\nPhase 6: Generating outputs...")

    IPL_COMP_IDS = [1358, 1715, 2193, 2725, 3298]

    # Top 10 batters
    top_bat = eligible_bat.head(10).copy()
    top_bat['rank'] = range(1, 11)
    top_bat['ci_low'] = top_bat['striker_id'].map(lambda x: bat_ci.get(x, {}).get('ci_low', 0))
    top_bat['ci_high'] = top_bat['striker_id'].map(lambda x: bat_ci.get(x, {}).get('ci_high', 0))
    top_bat['top10_pct'] = top_bat['striker_id'].map(lambda x: bat_top10_pct.get(x, 0))

    # Top 10 bowlers
    top_bowl = eligible_bowl.head(10).copy()
    top_bowl['rank'] = range(1, 11)
    top_bowl['ci_low'] = top_bowl['bowler_id'].map(lambda x: bowl_ci.get(x, {}).get('ci_low', 0))
    top_bowl['ci_high'] = top_bowl['bowler_id'].map(lambda x: bowl_ci.get(x, {}).get('ci_high', 0))
    top_bowl['top10_pct'] = top_bowl['bowler_id'].map(lambda x: bowl_top10_pct.get(x, 0))

    # ─── Determine IPL / overseas status ───
    ipl_players = set()
    ipl_matches = df[df['comp_id'].isin(IPL_COMP_IDS)]
    ipl_players.update(ipl_matches['striker_id'].unique())
    ipl_players.update(ipl_matches['bowler_id'].unique())

    # Detect Indian players (played for India team_id=18)
    india_team_matches = df[df['batting_team_id'] == 18]['striker_id'].unique().tolist()
    india_team_matches += df[df['bowling_team_id'] == 18]['bowler_id'].unique().tolist()
    india_players = set(india_team_matches)

    top_bat['is_indian'] = top_bat['striker_id'].isin(india_players)
    top_bat['slot_type'] = top_bat['is_indian'].map({True: 'Indian', False: 'Overseas'})

    top_bowl['is_indian'] = top_bowl['bowler_id'].isin(india_players)
    top_bowl['slot_type'] = top_bowl['is_indian'].map({True: 'Indian', False: 'Overseas'})

    # ─── Build JSON for HTML ───
    bat_list = []
    for _, r in top_bat.iterrows():
        bat_list.append({
            'rank': int(r['rank']),
            'name': r.get('player_name', f"ID_{r['striker_id']}"),
            'team': r.get('team_name', 'Unknown'),
            'rating': round(float(r['pressure_rating']), 3),
            'sr_hp': round(float(r.get('strike_rate_hp', 0)), 1),
            'sr_lp': round(float(r.get('strike_rate_lp', 0)), 1),
            'impact': round(float(r.get('runs_above_exp_per_ball_hp', 0)), 3),
            'ci_low': float(r['ci_low']),
            'ci_high': float(r['ci_high']),
            'top10_pct': float(r['top10_pct']),
            'hp_balls': int(r.get('balls_hp', 0)),
            'hp_matches': int(r.get('matches_hp', 0)),
            'slot': r['slot_type'],
            'boundary_pct_hp': round(float(r.get('boundary_pct_hp', 0)), 1),
            'dot_pct_hp': round(float(r.get('dot_pct_hp', 0)), 1),
        })

    bowl_list = []
    for _, r in top_bowl.iterrows():
        bowl_list.append({
            'rank': int(r['rank']),
            'name': r.get('player_name', f"ID_{r['bowler_id']}"),
            'team': r.get('team_name', 'Unknown'),
            'rating': round(float(r['pressure_rating']), 3),
            'econ_hp': round(float(r.get('economy_hp', 0)), 1),
            'econ_lp': round(float(r.get('economy_lp', 0)), 1),
            'wkt_rate_hp': round(float(r.get('wicket_rate_hp', 0)), 2),
            'ci_low': float(r['ci_low']),
            'ci_high': float(r['ci_high']),
            'top10_pct': float(r['top10_pct']),
            'hp_balls': int(r.get('balls_hp', 0)),
            'hp_matches': int(r.get('matches_hp', 0)),
            'slot': r['slot_type'],
            'dot_pct_hp': round(float(r.get('dot_pct_hp', 0)), 1),
        })

    # Pressure validation for chart
    pv_chart = {}
    for label in ['low', 'medium', 'high', 'very_high']:
        if label in pressure_validation:
            pv_chart[label] = pressure_validation[label]

    output_json = {
        'top_batters': bat_list,
        'top_bowlers': bowl_list,
        'pressure_validation': pv_chart,
        'methodology': {
            'total_balls': int(len(df)),
            'total_matches': int(df['match_id'].nunique()),
            'hp_threshold': 'Top 25% of Pressure Index',
            'min_hp_balls': 50,
            'min_matches': 10,
            'bootstrap_iterations': 500,
        }
    }

    # Save JSON
    json_path = os.path.join(OUT, 'results.json')
    with open(json_path, 'w') as f:
        json.dump(output_json, f, indent=2, default=str)
    print(f"  Results JSON saved to {json_path}")

    # ─── Save CSV ───
    csv_rows = []
    for item in bat_list:
        csv_rows.append({
            'category': 'batter',
            'rank': item['rank'],
            'player_name': item['name'],
            'team': item['team'],
            'pressure_rating': item['rating'],
            'key_stat': f"SR under pressure: {item['sr_hp']}",
            'top10_stability_pct': item['top10_pct'],
        })
    for item in bowl_list:
        csv_rows.append({
            'category': 'bowler',
            'rank': item['rank'],
            'player_name': item['name'],
            'team': item['team'],
            'pressure_rating': item['rating'],
            'key_stat': f"Economy under pressure: {item['econ_hp']}",
            'top10_stability_pct': item['top10_pct'],
        })

    csv_df = pd.DataFrame(csv_rows)
    csv_path = os.path.join(OUT, 'top10_lists.csv')
    csv_df.to_csv(csv_path, index=False)
    print(f"  Top 10 CSV saved to {csv_path}")

    return output_json


# ═══════════════════════════════════════════════════════════════════════════════
# SENSITIVITY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def sensitivity_analysis(df, eligible_bat, eligible_bowl):
    """
    Test alternative pressure definitions and threshold choices.
    """
    print("\nSensitivity Analysis...")

    # Alt 1: Top 30% as high pressure (instead of 25%)
    cutoff_30 = df['pressure_index'].quantile(0.70)
    hp_30 = df['pressure_index'] >= cutoff_30

    # Alt 2: Top 20%
    cutoff_20 = df['pressure_index'].quantile(0.80)
    hp_20 = df['pressure_index'] >= cutoff_20

    # Compare how top 10 batter IDs change
    original_top10 = set(eligible_bat.head(10)['striker_id'].tolist())

    results = {'original_top10': len(original_top10)}

    for alt_name, alt_mask in [('top30%', hp_30), ('top20%', hp_20)]:
        legal = df[df['is_legal']].copy()
        legal['alt_hp'] = alt_mask[legal.index]
        hp_grp = legal[legal['alt_hp']].groupby('striker_id').agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
        ).reset_index()
        hp_grp['sr'] = hp_grp['runs'] / hp_grp['balls'] * 100
        hp_grp = hp_grp[hp_grp['balls'] >= 30].sort_values('sr', ascending=False)
        alt_top10 = set(hp_grp.head(10)['striker_id'].tolist())
        overlap = len(original_top10 & alt_top10)
        results[alt_name] = {'overlap_with_original': overlap}
        print(f"  {alt_name}: {overlap}/10 overlap with original top 10 batters")

    # Threshold sensitivity for min balls
    for min_b in [30, 50, 80]:
        filtered = eligible_bat[eligible_bat['balls_hp'] >= min_b]
        top = set(filtered.head(10)['striker_id'].tolist())
        overlap = len(original_top10 & top)
        print(f"  Min {min_b} HP balls: {overlap}/10 overlap")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("SupeRR Selector Season 2 — Pressure Performance Analysis")
    print("=" * 70)

    # Load
    bbb, matches, comp, teams, ctpm, pe = load_data()

    # Phase 0: Prepare
    df, matches, team_strength = prepare_data(bbb, matches, comp, teams, ctpm)

    # Phase 2: Pressure Index
    par_dict = build_par_curves(df)
    df = compute_pressure_index(df, par_dict)
    pv = validate_pressure_index(df)

    # Phase 3: Performance measurement
    exp_dict, bowl_dict, gr, gw, gbr, gbw = build_expected_models(df)
    bat, legal_bat = compute_batter_metrics(df, exp_dict, gr, gw)
    bowl, legal_bowl = compute_bowler_metrics(df, bowl_dict, gbr, gbw)

    # Phase 3b: Ratings
    eligible_bat = compute_batter_rating(bat, df, ctpm)
    eligible_bowl = compute_bowler_rating(bowl, df, ctpm)

    # Phase 5: Bootstrap
    bat_ci, bowl_ci, bat_top10, bowl_top10 = bootstrap_rankings(
        df, eligible_bat, eligible_bowl, ctpm, n_boot=500
    )

    # Sensitivity
    sens = sensitivity_analysis(df, eligible_bat, eligible_bowl)

    # Phase 6: Outputs
    output = generate_outputs(eligible_bat, eligible_bowl, bat_ci, bowl_ci,
                             bat_top10, bowl_top10, pv, df, comp)

    # Print final top 10
    print("\n" + "=" * 70)
    print("FINAL TOP 10 BATTERS UNDER PRESSURE")
    print("=" * 70)
    for b in output['top_batters']:
        print(f"  #{b['rank']:2d} {b['name']:<25s} ({b['team']:<20s}) Rating={b['rating']:.3f}  SR_HP={b['sr_hp']}  Top10 in {b['top10_pct']}% boots")

    print("\n" + "=" * 70)
    print("FINAL TOP 10 BOWLERS UNDER PRESSURE")
    print("=" * 70)
    for b in output['top_bowlers']:
        print(f"  #{b['rank']:2d} {b['name']:<25s} ({b['team']:<20s}) Rating={b['rating']:.3f}  Econ_HP={b['econ_hp']}  Top10 in {b['top10_pct']}% boots")

    # Save enriched DF for cross-checks
    df.to_csv(os.path.join(OUT, 'analysis', 'enriched_ball_by_ball.csv'), index=False)
    eligible_bat.to_csv(os.path.join(OUT, 'analysis', 'batter_ratings.csv'), index=False)
    eligible_bowl.to_csv(os.path.join(OUT, 'analysis', 'bowler_ratings.csv'), index=False)

    print(f"\nAll outputs saved to {OUT}")
    print("Done.")


if __name__ == '__main__':
    main()
