// ============================================================
// WAR ROOM AUCTION SIMULATOR ENGINE (PHASE 6)
// ============================================================
import { ICONS } from './icons.js';

export function parsePriceToCr(priceStr) {
  if (!priceStr) return 0.0;
  const s = priceStr.toLowerCase();

  // "₹1.10 Cr" or "1.50 Cr"
  const crMatch = s.match(/₹?\s*(\d+(?:\.\d+)?)\s*cr/);
  if (crMatch) {
    return parseFloat(crMatch[1]);
  }

  // "₹20 Lakh" or "50 Lakh"
  const lakhMatch = s.match(/₹?\s*(\d+(?:\.\d+)?)\s*lakh/);
  if (lakhMatch) {
    return parseFloat(lakhMatch[1]) / 100.0;
  }

  return 0.0;
}

export class WarRoomSimulator {
  constructor(containerEl, { eligiblePlayers, creditsData, metaData }) {
    this.container = containerEl;
    this.eligiblePlayers = eligiblePlayers || [];
    this.creditsData = creditsData || {};
    this.metaData = metaData || {};

    // Editable Model Assumptions (as of 16 Nov 2026)
    this.startingPurse = 45.0; // ₹ Cr (Not Rs 102 Cr!)
    this.initialSquad = 18;    // Max 25
    this.initialOverseas = 4; // Max 8

    // Stated Franchise Needs (4 Jharokha Arches)
    this.slots = [
      {
        id: 'slot-death-pacer',
        roman: 'I',
        need: 'Death-Overs Pacer',
        icon: ICONS.zap,
        tacticalGap: 'High-leverage overs 17–20 specialist to complement Jofra Archer. Target sub-7.5 economy & high dot ball frequency.',
        recommended: ['Jamie Overton', 'Gerald Coetzee', 'Matheesha Pathirana', 'Blessing Muzarabani'],
        assigned: null
      },
      {
        id: 'slot-finisher',
        roman: 'II',
        need: 'Middle-Order Finisher',
        icon: ICONS.flame,
        tacticalGap: 'Explosive boundary hitter for death overs (15–20). Target crisis strike rate (>170) and par-deficit acceleration.',
        recommended: ['Tim David', 'David Miller', 'Ashutosh Sharma', 'Glenn Maxwell'],
        assigned: null
      },
      {
        id: 'slot-spinner',
        roman: 'III',
        need: 'Wicket-Taking Spinner',
        icon: ICONS.compass,
        tacticalGap: 'Middle-overs controller (overs 7–15) with strike capability. Target elevated dismissal rate and collapse induction.',
        recommended: ['Mohammad Rishad Hossain'],
        assigned: null
      },
      {
        id: 'slot-indian-pace',
        roman: 'IV',
        need: 'Indian Pace Depth',
        icon: ICONS.shield,
        tacticalGap: 'Domestic Indian pace backup under pressure to preserve overseas quota slots and absorb powerplay/death overs.',
        recommended: ['Anshul Kamboj'],
        assigned: null
      }
    ];

    this.render();
  }

  setStartingPurse(val) {
    this.startingPurse = Math.max(0, parseFloat(val) || 0);
    const hl = document.getElementById('sim-headline-purse');
    if (hl) {
      hl.textContent = `Allocating an assumed purse of ₹${this.startingPurse.toFixed(1)} Cr (editable, unverified, as of 16 Nov 2026)`;
    }
    this.updateGauges();
  }

  setInitialSquad(val) {
    this.initialSquad = Math.max(0, parseInt(val, 10) || 0);
    this.updateGauges();
  }

  setInitialOverseas(val) {
    this.initialOverseas = Math.max(0, parseInt(val, 10) || 0);
    this.updateGauges();
  }

  assignPlayerToSlot(slotIndex, player, customPrice = null) {
    if (slotIndex < 0 || slotIndex >= this.slots.length) return;

    // Check if player is already assigned in another slot
    this.slots.forEach((s, idx) => {
      if (s.assigned && s.assigned.player.name === player.name) {
        this.slots[idx].assigned = null;
      }
    });

    const isVerified = !!(player.verified_meta && player.verified_meta.verified && player.is_price_verified);
    const parsedPrice = parsePriceToCr(player.display_price);

    let priceCr = parsedPrice;
    let isEstimate = false;

    if (customPrice !== null) {
      priceCr = parseFloat(customPrice) || 0.0;
      isEstimate = true;
    } else if (!isVerified || priceCr === 0) {
      // Default estimate if unverified
      priceCr = player.price_band ? parsePriceToCr(player.price_band) || 2.0 : 2.0;
      isEstimate = true;
    }

    this.slots[slotIndex].assigned = {
      player,
      priceCr,
      isEstimate
    };

    this.render();
  }

  removePlayerFromSlot(slotIndex) {
    if (slotIndex < 0 || slotIndex >= this.slots.length) return;
    this.slots[slotIndex].assigned = null;
    this.render();
  }

  updateAssignedPrice(slotIndex, newPrice) {
    if (!this.slots[slotIndex] || !this.slots[slotIndex].assigned) return;
    const p = parseFloat(newPrice) || 0.0;
    this.slots[slotIndex].assigned.priceCr = p;
    this.slots[slotIndex].assigned.isEstimate = true;
    this.updateGauges();
    this.updateSlotPriceTag(slotIndex);
  }

  calculateMetrics() {
    let totalSpent = 0.0;
    let addedOverseas = 0;
    let addedSquad = 0;

    const roleBreakdown = {
      batters: 0,
      finishers: 0,
      pacers: 0,
      spinners: 0,
      allrounders: 0
    };

    this.slots.forEach((slot) => {
      if (slot.assigned) {
        const p = slot.assigned.player;
        totalSpent += slot.assigned.priceCr;
        addedSquad += 1;

        const isOverseas = (p.display_nationality || p.slot || '').toLowerCase() !== 'india' &&
                           !(p.slot || '').toLowerCase().includes('indian');
        if (isOverseas) {
          addedOverseas += 1;
        }

        const roleStr = (p.display_role || p.role || '').toLowerCase();
        if (roleStr.includes('opening') || roleStr.includes('top-order')) roleBreakdown.batters++;
        if (roleStr.includes('finisher')) roleBreakdown.finishers++;
        if (roleStr.includes('fast') || roleStr.includes('pace') || roleStr.includes('medium')) roleBreakdown.pacers++;
        if (roleStr.includes('spin') || roleStr.includes('wrist') || roleStr.includes('orthodox')) roleBreakdown.spinners++;
        if (roleStr.includes('all-rounder') || roleStr.includes('allrounder')) roleBreakdown.allrounders++;
      }
    });

    const remainingPurse = this.startingPurse - totalSpent;
    const finalSquad = this.initialSquad + addedSquad;
    const finalOverseas = this.initialOverseas + addedOverseas;

    const isPurseBreached = remainingPurse < 0;
    const isSquadBreached = finalSquad > 25;
    const isOverseasBreached = finalOverseas > 8;

    return {
      totalSpent,
      remainingPurse,
      finalSquad,
      finalOverseas,
      isPurseBreached,
      isSquadBreached,
      isOverseasBreached,
      roleBreakdown
    };
  }

  render() {
    if (!this.container) return;
    this.container.innerHTML = '';

    const metrics = this.calculateMetrics();

    // 1. War Room Assumptions Bar (Editorial Header & Inputs)
    const assumptionsCard = document.createElement('div');
    assumptionsCard.className = 'simulator-assumptions-card';
    assumptionsCard.innerHTML = `
      <div class="assumptions-header">
        <div class="ah-left">
          <div class="editorial-meta-tag">
            <span class="em-fig">FIG. 05</span>
            <span class="em-sep">/</span>
            <span class="em-category">TACTICAL LINEUP SIMULATOR</span>
            <span class="em-sep">/</span>
            <span class="em-date">16 NOV 2026</span>
          </div>
          <h2 class="editorial-display-heading" id="sim-headline-purse">Allocating an assumed purse of ₹${this.startingPurse.toFixed(1)} Cr (editable, unverified, as of 16 Nov 2026)</h2>
          <p class="editorial-lead-text">
            Total salary cap ceiling is ₹157.00 Cr (auction purse + incremental performance pay + match fees ceiling; unverified assumption). Purse, squad size, and overseas limit below are fully editable inputs to stress-test Rajasthan Royals auction allocation scenarios.
          </p>
        </div>
      </div>

      <div class="assumptions-input-grid">
        <div class="assump-field">
          <label for="sim-input-purse" class="assump-label">ASSUMED AUCTION PURSE</label>
          <div class="assump-input-box">
            <span class="curr-prefix">₹</span>
            <input type="number" id="sim-input-purse" class="assump-number-input" value="${this.startingPurse.toFixed(1)}" step="0.5" min="0" max="157" />
            <span class="curr-suffix">Cr</span>
          </div>
          <span class="field-hint">Editable assumption (Ceiling ₹157 Cr)</span>
        </div>

        <div class="assump-field">
          <label for="sim-input-squad" class="assump-label">INITIAL SQUAD SIZE</label>
          <div class="assump-input-box">
            <input type="number" id="sim-input-squad" class="assump-number-input" value="${this.initialSquad}" min="0" max="25" />
            <span class="curr-suffix">/ 25</span>
          </div>
          <span class="field-hint">Max BCCI roster limit: 25</span>
        </div>

        <div class="assump-field">
          <label for="sim-input-overseas" class="assump-label">RETAINED OVERSEAS</label>
          <div class="assump-input-box">
            <input type="number" id="sim-input-overseas" class="assump-number-input" value="${this.initialOverseas}" min="0" max="8" />
            <span class="curr-suffix">/ 8</span>
          </div>
          <span class="field-hint">Max BCCI overseas quota: 8</span>
        </div>

        <div class="assump-field">
          <label class="assump-label">FRANCHISE ROSTER STATUS</label>
          <div class="status-pending-pill">Unverified Assumption</div>
          <span class="field-hint">As of 16 Nov 2026</span>
        </div>
      </div>
    `;
    this.container.appendChild(assumptionsCard);

    // 2. Live Metrics & Rule Breaches Gauges Bar
    const gaugesCard = document.createElement('div');
    gaugesCard.className = 'simulator-gauges-card';
    gaugesCard.id = 'sim-gauges-card';
    this.container.appendChild(gaugesCard);

    // 3. Four Editorial Tactical Slots Grid
    const archesContainer = document.createElement('div');
    archesContainer.className = 'tactical-slots-grid';
    archesContainer.id = 'jharokha-arches-grid';
    this.container.appendChild(archesContainer);

    this.renderGauges(metrics);
    this.renderArches();
    this.bindInputs();
  }

  renderGauges(metrics) {
    const gaugesCard = document.getElementById('sim-gauges-card');
    if (!gaugesCard) return;

    const pursePct = Math.min(100, Math.max(0, (metrics.totalSpent / (this.startingPurse || 1)) * 100));

    // Rule Warning Banner
    let warningsHtml = '';
    if (metrics.isPurseBreached) {
      warningsHtml += `<div class="rule-warning-pill purse-breach">${ICONS.alertTriangle} PURSE DEFICIT: Allocated bids exceed available purse by ₹${Math.abs(metrics.remainingPurse).toFixed(2)} Cr!</div>`;
    }
    if (metrics.isSquadBreached) {
      warningsHtml += `<div class="rule-warning-pill squad-breach">${ICONS.alertTriangle} SQUAD LIMIT BREACH: Total roster exceeds maximum 25 players (${metrics.finalSquad} / 25)!</div>`;
    }
    if (metrics.isOverseasBreached) {
      warningsHtml += `<div class="rule-warning-pill overseas-breach">${ICONS.alertTriangle} OVERSEAS BREACH: Squad exceeds maximum 8 overseas quota (${metrics.finalOverseas} / 8)!</div>`;
    }
    if (!warningsHtml) {
      warningsHtml = `<div class="rule-compliant-pill">${ICONS.checkCircle} SQUAD &amp; PURSE RULES COMPLIANT · Valid Auction Strategy</div>`;
    }

    // 8 Overseas Visual Dots
    let overseasDotsHtml = '';
    for (let i = 1; i <= 8; i++) {
      if (i <= this.initialOverseas) {
        overseasDotsHtml += `<span class="ov-dot initial" title="Retained Overseas #${i}"></span>`;
      } else if (i <= metrics.finalOverseas) {
        overseasDotsHtml += `<span class="ov-dot simulated ${metrics.isOverseasBreached ? 'breach' : ''}" title="Auction Addition Overseas #${i}"></span>`;
      } else {
        overseasDotsHtml += `<span class="ov-dot empty" title="Available Overseas Slot #${i}"></span>`;
      }
    }
    if (metrics.finalOverseas > 8) {
      for (let i = 9; i <= metrics.finalOverseas; i++) {
        overseasDotsHtml += `<span class="ov-dot excess breach" title="Excess Overseas #${i}">!</span>`;
      }
    }

    gaugesCard.innerHTML = `
      <div class="gauges-status-banner">
        ${warningsHtml}
      </div>

      <div class="gauges-strip-grid">
        <!-- Gauge 1: Purse Utilization -->
        <div class="gauge-box purse-gauge-box">
          <div class="g-header">
            <span class="g-lbl">REMAINING ASSUMED PURSE</span>
            <span class="g-val ${metrics.isPurseBreached ? 'negative' : 'pink'}">₹${metrics.remainingPurse.toFixed(2)} Cr</span>
          </div>
          <div class="gauge-track">
            <div class="gauge-bar spent-bar" style="width: ${pursePct.toFixed(1)}%;"></div>
          </div>
          <div class="g-sub">
            <span>Spent: ₹${metrics.totalSpent.toFixed(2)} Cr</span>
            <span>Purse: ₹${this.startingPurse.toFixed(2)} Cr</span>
          </div>
        </div>

        <!-- Gauge 2: Squad Slots -->
        <div class="gauge-box squad-gauge-box">
          <div class="g-header">
            <span class="g-lbl">SQUAD ROSTER SLOTS</span>
            <span class="g-val ${metrics.isSquadBreached ? 'negative' : 'white'}">${metrics.finalSquad} <span class="max-sub">/ 25</span></span>
          </div>
          <div class="gauge-track">
            <div class="gauge-bar squad-bar" style="width: ${Math.min(100, (metrics.finalSquad / 25) * 100).toFixed(1)}%;"></div>
          </div>
          <div class="g-sub">
            <span>${25 - metrics.finalSquad} slots available</span>
            <span>${this.slots.filter(s => s.assigned).length} drafted in sim</span>
          </div>
        </div>

        <!-- Gauge 3: Overseas Quota (8 Dots) -->
        <div class="gauge-box overseas-gauge-box">
          <div class="g-header">
            <span class="g-lbl">OVERSEAS QUOTA (8 MAX)</span>
            <span class="g-val ${metrics.isOverseasBreached ? 'negative' : 'pink'}">${metrics.finalOverseas} <span class="max-sub">/ 8</span></span>
          </div>
          <div class="overseas-dots-bar">
            ${overseasDotsHtml}
          </div>
          <div class="g-sub">
            <span>Pink = Retained, White = Simulated Draft</span>
            <span>${Math.max(0, 8 - metrics.finalOverseas)} free</span>
          </div>
        </div>
      </div>
    `;
  }

  updateGauges() {
    const metrics = this.calculateMetrics();
    this.renderGauges(metrics);
  }

  renderArches() {
    const archesContainer = document.getElementById('jharokha-arches-grid');
    if (!archesContainer) return;
    archesContainer.innerHTML = '';

    this.slots.forEach((slot, idx) => {
      const archCard = document.createElement('div');
      archCard.className = `jharokha-arch-card ${slot.assigned ? 'is-occupied' : 'is-empty'}`;
      archCard.id = `jharokha-${slot.id}`;

      let contentHtml = '';

      if (slot.assigned) {
        const p = slot.assigned.player;
        const credit = this.creditsData[p.name];
        const imgSrc = credit && credit.file ? `./${credit.file}` : '';
        const priceTagClass = slot.assigned.isEstimate ? 'price-estimate-tag' : 'price-verified-tag';
        const priceTagLabel = slot.assigned.isEstimate ? '✎ Your Estimate' : '✓ Verified Auction Record';

        contentHtml = `
          <div class="assigned-player-box">
            <div class="ap-header">
              <span class="ap-rank">#${p.rank}</span>
              <button class="ap-btn-remove" data-slot="${idx}" title="Release this player from slot">${ICONS.trash} RELEASE</button>
            </div>

            <div class="ap-profile">
              <img src="${imgSrc}" alt="${p.name}" class="ap-avatar" onerror="this.style.display='none'" />
              <div class="ap-names">
                <h4 class="ap-name">${p.name}</h4>
                <div class="ap-role">${p.display_role} · ${p.display_nationality || p.team}</div>
              </div>
            </div>

            <div class="ap-metrics-pill">
              <div class="apm-item">
                <span class="apm-lbl">PRESSURE RATING</span>
                <span class="apm-val gold">${(p.rating || 0).toFixed(3)}</span>
              </div>
              <div class="apm-item">
                <span class="apm-lbl">90% CI</span>
                <span class="apm-val">[${p.ci_low} – ${p.ci_high}]</span>
              </div>
              <div class="apm-item">
                <span class="apm-lbl">STABILITY</span>
                <span class="apm-val pink">${p.top10_pct}%</span>
              </div>
            </div>

            <div class="ap-bid-control">
              <div class="bid-input-row">
                <label for="bid-input-${idx}" class="bid-label">SIMULATED WINNING BID:</label>
                <div class="bid-input-wrap">
                  <span class="bid-curr">₹</span>
                  <input type="number" id="bid-input-${idx}" class="bid-number-input" data-slot="${idx}" value="${slot.assigned.priceCr.toFixed(2)}" step="0.25" min="0" max="50" />
                  <span class="bid-suffix">Cr</span>
                </div>
              </div>
              <span id="price-tag-${idx}" class="${priceTagClass}">${priceTagLabel}</span>
            </div>
          </div>
        `;
      } else {
        // Empty slot with quick assignment
        const availableOptions = this.eligiblePlayers.filter(
          (p) => !this.slots.some((s) => s.assigned && s.assigned.player.name === p.name)
        );

        let optionsHtml = '<option value="">-- Select Target to Assign --</option>';
        availableOptions.forEach((p) => {
          optionsHtml += `<option value="${p.name}">#${p.rank} · ${p.name} (${p.display_role}) - ${p.display_price}</option>`;
        });

        // Quick recommendation chips
        let recChipsHtml = '';
        slot.recommended.forEach((recName) => {
          const recPlayer = this.eligiblePlayers.find((p) => p.name === recName);
          if (recPlayer && !this.slots.some((s) => s.assigned && s.assigned.player.name === recName)) {
            const credit = this.creditsData[recName];
            const chipImg = credit && credit.file ? `./${credit.file}` : '';
            recChipsHtml += `
              <button class="rec-chip-btn" data-slot="${idx}" data-name="${recName}" title="Quick draft ${recName}">
                ${chipImg ? `<img src="${chipImg}" alt="" class="chip-avatar" onerror="this.style.display='none'"/>` : ''}
                <span class="chip-name">${recName.split(' ')[0]}</span>
                <span class="chip-price">${recPlayer.display_price}</span>
                <span class="chip-plus">+ Draft</span>
              </button>
            `;
          }
        });

        contentHtml = `
          <div class="empty-jharokha-box">
            <div class="ej-icon">${slot.icon}</div>
            <div class="ej-prompt">UNASSIGNED TARGET SLOT</div>
            <p class="ej-desc">${slot.tacticalGap}</p>

            <div class="ej-selector-group">
              <label for="slot-select-${idx}" class="ej-label">SELECT CANDIDATE:</label>
              <select id="slot-select-${idx}" class="ej-select" data-slot="${idx}">
                ${optionsHtml}
              </select>
            </div>

            ${recChipsHtml ? `
              <div class="ej-rec-row">
                <span class="rec-title">WAR ROOM RECOMMENDED TARGETS:</span>
                <div class="rec-chips">${recChipsHtml}</div>
              </div>
            ` : ''}
          </div>
        `;
      }

      archCard.innerHTML = `
        <div class="tactical-slot-frame">
          <div class="tactical-slot-banner">
            <span class="ts-num">SLOT ${slot.roman} · TACTICAL MANDATE</span>
            <h3 class="ts-need-title">${slot.need.toUpperCase()}</h3>
          </div>
        </div>

        <div class="tactical-slot-body">
          ${contentHtml}
        </div>
      `;

      // Event bindings for this arch
      if (slot.assigned) {
        const btnRemove = archCard.querySelector('.ap-btn-remove');
        if (btnRemove) {
          btnRemove.addEventListener('click', () => this.removePlayerFromSlot(idx));
        }

        const bidInput = archCard.querySelector(`#bid-input-${idx}`);
        if (bidInput) {
          bidInput.addEventListener('input', (e) => {
            this.updateAssignedPrice(idx, e.target.value);
          });
        }
      } else {
        const sel = archCard.querySelector(`#slot-select-${idx}`);
        if (sel) {
          sel.addEventListener('change', (e) => {
            const pName = e.target.value;
            if (!pName) return;
            const p = this.eligiblePlayers.find((x) => x.name === pName);
            if (p) this.assignPlayerToSlot(idx, p);
          });
        }

        const chips = archCard.querySelectorAll('.rec-chip-btn');
        chips.forEach((btn) => {
          btn.addEventListener('click', () => {
            const pName = btn.getAttribute('data-name');
            const p = this.eligiblePlayers.find((x) => x.name === pName);
            if (p) this.assignPlayerToSlot(idx, p);
          });
        });
      }

      archesContainer.appendChild(archCard);
    });
  }

  updateSlotPriceTag(slotIndex) {
    const tagEl = document.getElementById(`price-tag-${slotIndex}`);
    if (tagEl && this.slots[slotIndex] && this.slots[slotIndex].assigned) {
      tagEl.className = 'price-estimate-tag';
      tagEl.textContent = '✎ Your Estimate';
    }
  }

  bindInputs() {
    const inputPurse = document.getElementById('sim-input-purse');
    const inputSquad = document.getElementById('sim-input-squad');
    const inputOverseas = document.getElementById('sim-input-overseas');

    if (inputPurse) {
      inputPurse.addEventListener('input', (e) => this.setStartingPurse(e.target.value));
    }
    if (inputSquad) {
      inputSquad.addEventListener('input', (e) => this.setInitialSquad(e.target.value));
    }
    if (inputOverseas) {
      inputOverseas.addEventListener('input', (e) => this.setInitialOverseas(e.target.value));
    }
  }
}

