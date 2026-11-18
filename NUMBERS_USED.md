# NUMBERS_USED.md — Mathematical & Numerical Provenance Registry

Every figure used in headlines, subheadings, copy, and calculations across the site is recorded below with its empirical source. Zero numbers are invented.

| Figure / Metric | Value | Context & Usage | Provenance & Source |
| :--- | :--- | :--- | :--- |
| **Evaluated Balls** | `199,208` | Headline & methodology ball count | `players.json` & `matches.csv` (843 completed matches) |
| **Raw Dataset Rows** | `200,999` | Section 10 data honesty headline | `data_pack/ball_by_ball.csv` total row count |
| **Excluded Deliveries** | `1,791` | Section 10 headline ("1,791 of 200,999 rows were excluded") | Exact difference: 200,999 raw rows − 199,208 evaluated |
| **Super-Over Deliveries** | `38` | Exclusion rule 1 | Deliveries in innings 3 & 4 across 6 tied fixtures |
| **Abandoned Deliveries** | `1,753` | Exclusion rule 2 | Deliveries in 24 incomplete / rain-abandoned matches |
| **Evaluated Matches** | `843` | Completed decisive match corpus | Matches with completed result and full win probability |
| **Raw Match Records** | `~867` | Total matches listed in raw pack | `matches.csv` total unique fixture count (843 + 24) |
| **Total Salary Cap** | `₹157.00 Cr` | Total ceiling (retentions + purse + fees) | BCCI IPL 2027 official total franchise salary cap ceiling |
| **Assumed Purse** | `₹45.0 Cr` | War Room live simulation input default | Unverified model assumption (as of 16 Nov 2026) |
| **Max Roster Limit** | `25` | Maximum squad size ceiling | Official BCCI IPL roster regulation |
| **Initial Squad Size** | `18` | War Room starting roster occupancy | Unverified franchise retention assumption (7 slots free) |
| **Max Overseas Limit** | `8` | Maximum foreign player roster ceiling | Official BCCI IPL overseas player regulation |
| **Initial Overseas** | `4` | War Room starting overseas count | Unverified franchise retention assumption (4 slots free) |
| **Evaluated Targets** | `20` | Roster candidate tally | Top 10 Batters + Top 10 Bowlers in `players.json` |
| **Actionable Targets** | `12` | Auction-eligible candidates | 20 candidates minus 8 locked/ineligible candidates |
| **Locked Candidates** | `8` | Ineligible, contracted, or retired | 4 Pakistani nationals + 3 RR retentions/contracts + 1 retired |
| **Pressure Band 1** | `78.8%` | Calm / Baseline match volume | Empirical delivery distribution in `players.json` (157,016 balls) |
| **Pressure Band 2** | `15.2%` | Rising Required Run Rate | Empirical delivery distribution in `players.json` (30,202 balls) |
| **Pressure Band 3** | `4.1%` | Crisis / High Leverage Overs | Empirical delivery distribution in `players.json` (8,088 balls) |
| **Pressure Band 4** | `2.0%` | Extreme Crucible / Death Finish | Empirical delivery distribution in `players.json` (3,902 balls) |
| **Top Batter Rating** | `0.984` | Vaibhav Sooryavanshi (#1 Batter) | Bayesian composite pressure rating in `players.json` |
| **Top Bowler Rating** | `0.945` | Sufiyan Muqeem (#1 Bowler) | Bayesian composite pressure rating in `players.json` |
