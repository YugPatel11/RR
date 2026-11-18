"""
SupeRR Selector Season 2 — Master Reproducible Pipeline
Rajasthan Royals IPL 2027 Auction Analytics War Room

Runs the full end-to-end analytics workflow with one command:
  python run_all.py

Steps:
  1. pressure_analysis.py: Data cleaning, Pressure Index calculation,
     Expected models, Bayesian shrinkage, Bootstrap CIs, Rankings & CSV output.
  2. generate_players_meta.py: Sourced and verified external metadata with 'as of' dates.
  3. normalize_results.py: Synchronizes unified player attributes across batters & bowlers.
  4. generate_report_charts.py: High-DPI visualizations for PDF report.
  5. build_interactive_dashboard.py: Compiles offline-ready, responsive index.html.
  6. build_pdf_report.py: Generates publication-quality Methodology_Report.pdf.
  7. spot_check.py: Reconciles all top-10 player statistics against raw ball deliveries.

Seed: 42 (fixed across all stochastic operations)
"""

import subprocess
import sys
import os

ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.abspath(os.path.join(ANALYSIS_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(OUTPUTS_DIR, ".."))

SCRIPTS = [
    (os.path.join(ANALYSIS_DIR, "pressure_analysis.py"), "Phase 0-6: Statistical Pressure Analysis & Bootstrap"),
    (os.path.join(ANALYSIS_DIR, "generate_players_meta.py"), "Metadata Compilation: Verified Auction Data & Sourcing"),
    (os.path.join(ANALYSIS_DIR, "normalize_results.py"), "Normalization: Unifying Batting & Bowling Schema"),
    (os.path.join(OUTPUTS_DIR, "generate_report_charts.py"), "Chart Generation: High-DPI Report Graphics"),
    (os.path.join(ANALYSIS_DIR, "build_interactive_dashboard.py"), "Dashboard Compilation: Interactive index.html"),
    (os.path.join(OUTPUTS_DIR, "build_pdf_report.py"), "Document Generation: Compiling Methodology_Report.pdf"),
    (os.path.join(ANALYSIS_DIR, "spot_check.py"), "Quality Audit: Spot-Checking Players by Exact ID"),
]

def main():
    print("=" * 75)
    print("SupeRR Selector Season 2: Master Pipeline Runner")
    print("Rajasthan Royals Analytics War Room — IPL 2027 Roster Planning")
    print("=" * 75)

    for script_path, desc in SCRIPTS:
        print(f"\n>> Executing: {desc}")
        print(f"   Script: {os.path.basename(script_path)}")
        res = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(script_path))
        if res.returncode != 0:
            print(f"ERROR: Execution failed for {script_path}")
            sys.exit(res.returncode)

    print("\n" + "=" * 75)
    print("SUCCESS: Full pipeline completed successfully!")
    print(f"Deliverables verified in: {OUTPUTS_DIR}")
    print("  - analysis/ : Reproducible scripts, CSVs, and figures")
    print("  - Methodology_Report.pdf : 7-page technical methodology paper")
    print("  - index.html + style.css : Interactive visual dashboard with 3D & presentation mode")
    print("  - top10_lists.csv : Final validated batting & bowling rankings")
    print("  - players_meta.json : Verified external contracts and sourcing dossier")
    print("=" * 75)

if __name__ == '__main__':
    main()
