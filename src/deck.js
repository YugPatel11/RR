/**
 * PRESENT MODE & METHODOLOGY SLIDE DECK
 * 16:9 Presentation Overlay for Rajasthan Royals SupeRR Selector War Room
 */

export class PresentDeck {
  constructor(options = {}) {
    this.container = document.getElementById('present-deck-modal');
    this.slideEl = document.getElementById('deck-slide-content');
    this.counterEl = document.getElementById('deck-counter');
    this.btnPrev = document.getElementById('deck-btn-prev');
    this.btnNext = document.getElementById('deck-btn-next');
    this.btnClose = document.getElementById('deck-btn-close');
    this.btnFullscreen = document.getElementById('deck-btn-fullscreen');
    this.btnPrint = document.getElementById('deck-btn-print');
    this.pillsContainer = document.getElementById('deck-pills');

    this.currentSlide = 0;
    this.totalSlides = 5;
    this.isOpen = false;

    this.slidesData = [
      {
        id: 'slide-1',
        tag: 'METHODOLOGY REPORT · SLIDE 1 OF 5',
        title: 'Pressure Definition & Dynamic Leverage Architecture',
        subtitle: 'Quantifying match leverage across 199,208 decisive deliveries into 4 distinct pressure bands',
        content: `
          <div class="deck-slide-grid">
            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">THE COMPOSITE LEVERAGE FORMULA</div>
                <h4 class="deck-card-title">Continuous Pressure Index <em>P</em> &in; [0, 1]</h4>
                <p class="deck-card-text">
                  Match pressure is dynamic, contextual, and score-dependent. Every legal delivery is evaluated across five real-time match state deficits:
                </p>
                <div class="deck-formula-box">
                  <span class="df-math">P = 0.30&middot;&Delta;RRR + 0.20&middot;RPB + 0.25&middot;ParDef + 0.15&middot;Collapse + 0.10&middot;Death</span>
                </div>
                <ul class="deck-bullet-list">
                  <li><strong>&Delta;RRR (30%):</strong> Current Required Run Rate surge above standard chase par (6.0 rpo).</li>
                  <li><strong>RPB (20%):</strong> Runs needed per legal ball remaining in chase phases.</li>
                  <li><strong>ParDef (25%):</strong> 1st innings deficit vs historical wicket-over par curve.</li>
                  <li><strong>Collapse (15%):</strong> Top-order shock (&ge;3 wickets down inside Powerplay).</li>
                  <li><strong>Death (10%):</strong> Leverage escalation in overs 16–20 with match in balance.</li>
                </ul>
              </div>
            </div>

            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">EMPIRICAL DATA STRATIFICATION</div>
                <h4 class="deck-card-title">The 4 Verified Pressure Bands</h4>
                <p class="deck-card-text">
                  The dataset stratifies into 4 hierarchical operational pressure bands (not equal quartiles):
                </p>
                <div class="deck-band-table">
                  <div class="dbt-row dbt-head">
                    <span>BAND</span><span>LEVERAGE</span><span>BALLS</span><span>STRIKE RATE</span><span>WKT %</span>
                  </div>
                  <div class="dbt-row">
                    <span class="dbt-band b1">Band 1: Low</span><span>P &lt; 0.25</span><span>156,905 (78.8%)</span><span>139.1</span><span>5.12%</span>
                  </div>
                  <div class="dbt-row">
                    <span class="dbt-band b2">Band 2: Medium</span><span>0.25 &ndash; 0.55</span><span>30,281 (15.2%)</span><span>134.8</span><span>5.89%</span>
                  </div>
                  <div class="dbt-row">
                    <span class="dbt-band b3">Band 3: High</span><span>0.55 &ndash; 0.80</span><span>8,083 (4.1%)</span><span>128.4</span><span>7.21%</span>
                  </div>
                  <div class="dbt-row highlight-row">
                    <span class="dbt-band b4">Band 4: Crisis</span><span>P &ge; 0.80</span><span>3,939 (2.0%)</span><span>118.8</span><span>10.69%</span>
                  </div>
                </div>
                <div class="deck-callout">
                  <strong>Key Finding:</strong> In Band 4 crisis moments, league-wide strike rate collapses by <strong>-20.3 rpo</strong> while wicket probability more than doubles (<strong>+108.8%</strong>).
                </div>
              </div>
            </div>
          </div>
        `
      },
      {
        id: 'slide-2',
        tag: 'METHODOLOGY REPORT · SLIDE 2 OF 5',
        title: 'Performance Measurement & Baseline Shrinkage',
        subtitle: 'Dual-layer Ghost Baseline modeling and Bayesian stabilization against sample variance',
        content: `
          <div class="deck-slide-grid">
            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">DUAL-LAYER GHOST BASELINE ARCHITECTURE</div>
                <h4 class="deck-card-title">Separating Baseline Class from Clutch Lift</h4>
                <p class="deck-card-text">
                  Traditional cricket scouting conflates overall talent with pressure fortitude. Our model isolates two independent vectors for each player:
                </p>
                <div class="deck-layer-comparison">
                  <div class="dl-item solid">
                    <span class="dl-badge solid-b">SOLID VECTOR (CRISIS)</span>
                    <p>Performance restricted exclusively to High Pressure deliveries (Bands 3 &amp; 4, <em>P</em> &ge; 0.55).</p>
                  </div>
                  <div class="dl-item ghost">
                    <span class="dl-badge ghost-b">DASHED GHOST VECTOR (BASELINE)</span>
                    <p>Standard delivery performance under normal conditions (Bands 1 &amp; 2, <em>P</em> &lt; 0.55).</p>
                  </div>
                </div>
                <p class="deck-card-text">
                  <strong>Clutch Differential (&Delta;):</strong> True reliability is measured as &Delta; = Metric<sub>HP</sub> &minus; Metric<sub>Baseline</sub>. Positive differential indicates a clutch multiplier.
                </p>
              </div>
            </div>

            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">BAYESIAN REGULARIZATION</div>
                <h4 class="deck-card-title">Empirical Bayes Shrinkage</h4>
                <p class="deck-card-text">
                  To protect Rajasthan Royals from bidding on small-sample anomalies, ratings are regularized toward league prior distributions:
                </p>
                <div class="deck-formula-box">
                  <span class="df-math">R<sub>shrunk</sub> = [N<sub>HP</sub> / (N<sub>HP</sub> + k)] &middot; R<sub>observed</sub> + [k / (N<sub>HP</sub> + k)] &middot; &mu;<sub>league</sub></span>
                </div>
                <ul class="deck-bullet-list">
                  <li><strong>Shrinkage Constant (<em>k</em> = 35 balls):</strong> Pulls volatile low-ball samples toward the league average.</li>
                  <li><strong>Inverted Bowler Normalization:</strong> Lower economy yields higher rating points (12.0 &minus; Econ).</li>
                  <li><strong>Dot Ball & Boundary Weighting:</strong> Batters credited for boundary creation + dot minimization; bowlers rewarded for dot accumulation.</li>
                </ul>
              </div>
            </div>
          </div>
        `
      },
      {
        id: 'slide-3',
        tag: 'METHODOLOGY REPORT · SLIDE 3 OF 5',
        title: 'Fair Comparisons: Sample Sizes, Eligibility & League Context',
        subtitle: 'Qualification thresholds, international tier conversion, and auction availability constraints',
        content: `
          <div class="deck-slide-grid">
            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">SAMPLE SIZE QUALIFICATION</div>
                <h4 class="deck-card-title">Strict Qualification Filters</h4>
                <p class="deck-card-text">
                  To ensure statistical credibility, players must meet rigorous qualification hurdles across the 2022–2026 data window:
                </p>
                <ul class="deck-bullet-list">
                  <li><strong>Batters:</strong> Minimum <strong>50 legal deliveries faced</strong> in high-pressure match situations across at least 8 fixtures.</li>
                  <li><strong>Bowlers:</strong> Minimum <strong>60 legal deliveries bowled</strong> in high-pressure situations across at least 8 fixtures.</li>
                  <li><strong>Outlier Capping:</strong> Single-over anomalous spikes (e.g. 30-run overs) are winsorized at 3 standard deviations to prevent leverage distortion.</li>
                </ul>
                <div class="deck-callout">
                  <strong>Conversion Coefficients:</strong> IPL deliveries are weighted at 1.00; Full-Member T20I at 0.95; Associate T20I at 0.75 with opponent quality indexing.
                </div>
              </div>
            </div>

            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">AUCTION ACTIONABILITY CRITERIA</div>
                <h4 class="deck-card-title">Eligibility & Franchise Reality</h4>
                <p class="deck-card-text">
                  The model ranks true global talent, but highlights practical auction constraints for the RR War Room:
                </p>
                <div class="deck-eligibility-list">
                  <div class="del-item locked">
                    <span class="del-icon">🔒</span>
                    <div>
                      <strong>Pakistani Internationals:</strong>
                      <span>Muqeem, Nawaz, Abrar, Shaheen are analytically elite but ineligible for IPL participation due to BCCI policy.</span>
                    </div>
                  </div>
                  <div class="del-item locked">
                    <span class="del-icon">🔒</span>
                    <div>
                      <strong>Internationally Retired:</strong>
                      <span>Dinesh Karthik (Rank 6 batter) is officially retired from competitive IPL cricket.</span>
                    </div>
                  </div>
                  <div class="del-item target">
                    <span class="del-icon">🎯</span>
                    <div>
                      <strong>Auction-Actionable Targets:</strong>
                      <span>Ashutosh Sharma, Blessing Muzarabani, Anshul Kamboj, Mohammad Rishad Hossain, Jamie Overton.</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `
      },
      {
        id: 'slide-4',
        tag: 'METHODOLOGY REPORT · SLIDE 4 OF 5',
        title: 'Evidence for the Top 10: Batters & Bowlers',
        subtitle: 'Empirical rankings, performance differentials, and priority acquisition recommendations for RR',
        content: `
          <div class="deck-slide-grid">
            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">TOP 10 RELIABLE BATTERS</div>
                <div class="deck-top10-table">
                  <div class="dtt-row dtt-head"><span>RK</span><span>PLAYER</span><span>NAT</span><span>RATING</span><span>HP SR</span><span>BASE SR</span><span>STATUS</span></div>
                  <div class="dtt-row"><span>1</span><strong>V. Sooryavanshi</strong><span>IND</span><span class="gold-t">0.896</span><span>256.1</span><span>219.4</span><span class="rr-t">Retained</span></div>
                  <div class="dtt-row highlight-row"><span>2</span><strong>Ashutosh Sharma</strong><span>IND</span><span class="gold-t">0.884</span><span>208.7</span><span>166.6</span><span class="act-t">🎯 TARGET</span></div>
                  <div class="dtt-row"><span>3</span><strong>Reeza Hendricks</strong><span>SA</span><span class="gold-t">0.862</span><span>184.2</span><span>142.1</span><span>Overseas</span></div>
                  <div class="dtt-row"><span>4</span><strong>Glenn Maxwell</strong><span>AUS</span><span>0.849</span><span>195.4</span><span>154.3</span><span>Overseas</span></div>
                  <div class="dtt-row"><span>5</span><strong>Shubham Dubey</strong><span>IND</span><span>0.825</span><span>179.3</span><span>141.2</span><span class="rr-t">Retained</span></div>
                  <div class="dtt-row locked-row"><span>6</span><strong>Dinesh Karthik</strong><span>IND</span><span>0.812</span><span>198.5</span><span>161.4</span><span class="lock-t">🔒 Retired</span></div>
                  <div class="dtt-row"><span>7</span><strong>Heinrich Klaasen</strong><span>SA</span><span>0.798</span><span>191.0</span><span>168.2</span><span>Retained</span></div>
                  <div class="dtt-row"><span>8</span><strong>Tilak Varma</strong><span>IND</span><span>0.781</span><span>168.4</span><span>144.5</span><span>Retained</span></div>
                  <div class="dtt-row"><span>9</span><strong>Shimron Hetmyer</strong><span>WI</span><span>0.765</span><span>182.1</span><span>155.8</span><span class="rr-t">Retained</span></div>
                  <div class="dtt-row"><span>10</span><strong>Nicholas Pooran</strong><span>WI</span><span>0.748</span><span>176.5</span><span>159.2</span><span>Retained</span></div>
                </div>
              </div>
            </div>

            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">TOP 10 RELIABLE BOWLERS</div>
                <div class="deck-top10-table">
                  <div class="dtt-row dtt-head"><span>RK</span><span>PLAYER</span><span>NAT</span><span>RATING</span><span>HP ECON</span><span>BASE ECON</span><span>STATUS</span></div>
                  <div class="dtt-row locked-row"><span>1</span><strong>Sufiyan Muqeem</strong><span>PAK</span><span class="gold-t">0.912</span><span>6.12</span><span>7.45</span><span class="lock-t">🔒 Ineligible</span></div>
                  <div class="dtt-row highlight-row"><span>2</span><strong>B. Muzarabani</strong><span>ZIM</span><span class="gold-t">0.891</span><span>6.45</span><span>7.80</span><span class="act-t">🎯 TARGET</span></div>
                  <div class="dtt-row locked-row"><span>3</span><strong>Mohammad Nawaz</strong><span>PAK</span><span class="gold-t">0.874</span><span>6.72</span><span>7.95</span><span class="lock-t">🔒 Ineligible</span></div>
                  <div class="dtt-row highlight-row"><span>4</span><strong>Anshul Kamboj</strong><span>IND</span><span class="gold-t">0.856</span><span>6.88</span><span>8.15</span><span class="act-t">🎯 TARGET</span></div>
                  <div class="dtt-row highlight-row"><span>5</span><strong>Rishad Hossain</strong><span>BAN</span><span>0.839</span><span>6.95</span><span>8.22</span><span class="act-t">🎯 TARGET</span></div>
                  <div class="dtt-row"><span>6</span><strong>Jasprit Bumrah</strong><span>IND</span><span>0.821</span><span>6.18</span><span>6.85</span><span>Retained</span></div>
                  <div class="dtt-row locked-row"><span>7</span><strong>Abrar Ahmed</strong><span>PAK</span><span>0.803</span><span>7.10</span><span>8.30</span><span class="lock-t">🔒 Ineligible</span></div>
                  <div class="dtt-row"><span>8</span><strong>Arshdeep Singh</strong><span>IND</span><span>0.789</span><span>7.62</span><span>8.85</span><span>Retained</span></div>
                  <div class="dtt-row locked-row"><span>9</span><strong>Shaheen Afridi</strong><span>PAK</span><span>0.772</span><span>7.45</span><span>8.20</span><span class="lock-t">🔒 Ineligible</span></div>
                  <div class="dtt-row highlight-row"><span>10</span><strong>Jamie Overton</strong><span>ENG</span><span>0.758</span><span>7.84</span><span>9.10</span><span class="act-t">🎯 TARGET</span></div>
                </div>
              </div>
            </div>
          </div>
        `
      },
      {
        id: 'slide-5',
        tag: 'METHODOLOGY REPORT · SLIDE 5 OF 5',
        title: 'Reliability & Limitations: Bootstrap CIs & War Room Guidance',
        subtitle: 'Statistical uncertainty, sample caveats, and auction purse financial framework',
        content: `
          <div class="deck-slide-grid">
            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">STATISTICAL ROBUSTNESS</div>
                <h4 class="deck-card-title">Bootstrap Empirical Confidence Intervals</h4>
                <p class="deck-card-text">
                  To quantify uncertainty, 10,000 bootstrap iterations were computed for every qualified candidate:
                </p>
                <ul class="deck-bullet-list">
                  <li><strong>Top-Tier Stability:</strong> Vaibhav Sooryavanshi (99.4%), Ashutosh Sharma (98.2%), and Jasprit Bumrah (97.8%) demonstrate exceptional rank stability across resamples.</li>
                  <li><strong>Halo Width Variance:</strong> Visualized in 3D as halo rings: narrow halos denote narrow 90% CIs (high certainty); wide halos denote broader variance.</li>
                  <li><strong>Small-Sample Hazard:</strong> Sooryavanshi's 82 HP balls produce a wide 90% CI [225.0 - 294.0 SR], indicating unmatched ceiling but higher variance.</li>
                </ul>
              </div>
            </div>

            <div class="deck-col">
              <div class="deck-card">
                <div class="deck-card-label">STRATEGIC AUCTION LIMITATIONS</div>
                <h4 class="deck-card-title">War Room Financial Constraints</h4>
                <p class="deck-card-text">
                  Rajasthan Royals must balance statistical impact against auction mechanics:
                </p>
                <div class="deck-warning-box">
                  <div class="dw-title">⚠️ MANDATORY FINANCIAL DISCLOSURE</div>
                  <p>
                    <strong>₹157.00 Crore</strong> is the 2027 total player salary cap (including performance bonuses and match fees), <strong>NOT</strong> the auction purse. Starting auction purse is an editable assumption (assumed at ₹45.0 Cr pending 17 Nov 2026 retention declarations).
                  </p>
                </div>
                <ul class="deck-bullet-list">
                  <li><strong>Weak-Opposition Deflation:</strong> Associate matches for Muzarabani and Rishad Hossain require tactical ground-truthing against elite 145+ km/h pace.</li>
                  <li><strong>Actionable Blueprint:</strong> Target Jamie Overton (Death Pacer), Ashutosh Sharma (Finisher), Rishad Hossain (Spinner), and Anshul Kamboj (Indian Pace Depth).</li>
                </ul>
              </div>
            </div>
          </div>
        `
      }
    ];

    this.init();
  }

  init() {
    if (!this.container) return;

    if (this.btnPrev) this.btnPrev.addEventListener('click', () => this.prev());
    if (this.btnNext) this.btnNext.addEventListener('click', () => this.next());
    if (this.btnClose) this.btnClose.addEventListener('click', () => this.close());
    if (this.btnFullscreen) this.btnFullscreen.addEventListener('click', () => this.toggleFullscreen());
    if (this.btnPrint) this.btnPrint.addEventListener('click', () => this.printDeck());

    // Keyboard Navigation
    window.addEventListener('keydown', (e) => {
      if (!this.isOpen) return;

      if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        this.next();
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp') {
        e.preventDefault();
        this.prev();
      } else if (e.key === 'Escape') {
        this.close();
      } else if (e.key === 'f' || e.key === 'F') {
        this.toggleFullscreen();
      }
    });

    // Render Pills
    this.renderPills();
  }

  renderPills() {
    if (!this.pillsContainer) return;
    this.pillsContainer.innerHTML = '';
    this.slidesData.forEach((s, idx) => {
      const btn = document.createElement('button');
      btn.className = `deck-pill-btn ${idx === this.currentSlide ? 'active' : ''}`;
      btn.setAttribute('title', `Jump to Slide ${idx + 1}: ${s.title}`);
      btn.textContent = `${idx + 1}`;
      btn.addEventListener('click', () => this.goTo(idx));
      this.pillsContainer.appendChild(btn);
    });
  }

  open(startSlideIndex = 0) {
    if (!this.container) return;
    this.isOpen = true;
    this.currentSlide = Math.max(0, Math.min(startSlideIndex, this.totalSlides - 1));
    this.container.classList.add('active');
    document.body.classList.add('deck-open');
    this.renderSlide();
  }

  close() {
    if (!this.container) return;
    this.isOpen = false;
    this.container.classList.remove('active');
    document.body.classList.remove('deck-open');
    if (document.fullscreenElement) {
      document.exitFullscreen().catch(() => {});
    }
  }

  next() {
    if (this.currentSlide < this.totalSlides - 1) {
      this.currentSlide++;
      this.renderSlide();
    }
  }

  prev() {
    if (this.currentSlide > 0) {
      this.currentSlide--;
      this.renderSlide();
    }
  }

  goTo(idx) {
    if (idx >= 0 && idx < this.totalSlides) {
      this.currentSlide = idx;
      this.renderSlide();
    }
  }

  toggleFullscreen() {
    if (!document.fullscreenElement) {
      this.container.requestFullscreen().catch((err) => {
        console.warn('Fullscreen request failed:', err);
      });
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }

  printDeck() {
    // Print triggers the custom print stylesheet formatting all 5 slides
    window.print();
  }

  renderSlide() {
    if (!this.slideEl) return;
    const slide = this.slidesData[this.currentSlide];

    if (this.counterEl) {
      this.counterEl.textContent = `Slide ${this.currentSlide + 1} of ${this.totalSlides}`;
    }

    if (this.btnPrev) this.btnPrev.disabled = this.currentSlide === 0;
    if (this.btnNext) this.btnNext.disabled = this.currentSlide === this.totalSlides - 1;

    // Update Pills
    if (this.pillsContainer) {
      const pills = this.pillsContainer.querySelectorAll('.deck-pill-btn');
      pills.forEach((p, i) => {
        if (i === this.currentSlide) p.classList.add('active');
        else p.classList.remove('active');
      });
    }

    this.slideEl.innerHTML = `
      <div class="deck-slide-inner animate-slide-in">
        <div class="deck-slide-header">
          <div class="deck-slide-tag">
            <span class="pulse-dot"></span>
            <span>${slide.tag}</span>
            <span class="devanagari-inline">हल्ला बोल</span>
          </div>
          <h2 class="deck-slide-title">${slide.title}</h2>
          <p class="deck-slide-subtitle">${slide.subtitle}</p>
        </div>
        <div class="deck-slide-body">
          ${slide.content}
        </div>
      </div>
    `;
  }
}
