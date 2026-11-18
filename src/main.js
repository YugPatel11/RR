import './style.css';
import '@fontsource/plus-jakarta-sans/400.css';
import '@fontsource/plus-jakarta-sans/600.css';
import '@fontsource/plus-jakarta-sans/700.css';
import '@fontsource/fraunces/700.css';
import '@fontsource/barlow-condensed/600.css';
import '@fontsource/barlow-condensed/700.css';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/700.css';
import '@fontsource/noto-serif-devanagari/700.css';

import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { createStepwellScene } from './stepwell.js';
import { RadarDuelChart, BATTER_AXES, BOWLER_AXES } from './radar.js';
import { WarRoomSimulator } from './simulator.js';
import { PresentDeck } from './deck.js';
import { renderSourcesAndMethodology } from './sources.js';
import { ICONS } from './icons.js';

gsap.registerPlugin(ScrollTrigger);

// WebGL Capability Check
function isWebGLAvailable() {
  try {
    const canvas = document.createElement('canvas');
    return !!(
      window.WebGLRenderingContext &&
      (canvas.getContext('webgl') || canvas.getContext('experimental-webgl'))
    );
  } catch (e) {
    return false;
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  const loader = document.getElementById('loader');
  const meterFill = document.getElementById('meter-fill');
  const meterVal = document.getElementById('meter-val');
  const canvas = document.getElementById('webgl-canvas');

  // Navigation Jump Buttons
  const btnJumpChamber = document.getElementById('btn-jump-chamber');
  const btnJumpRadar = document.getElementById('btn-jump-radar');
  const btnJumpShortlist = document.getElementById('btn-jump-shortlist');
  const btnJumpWarroom = document.getElementById('btn-jump-warroom');
  const btnJumpSources = document.getElementById('btn-jump-sources');
  const btnOpenDeck = document.getElementById('btn-open-deck');
  const btnLowPower = document.getElementById('btn-low-power');

  const cqJumpRadar = document.getElementById('cq-jump-radar');
  const cqJumpShortlist = document.getElementById('cq-jump-shortlist');
  const cqJumpWarroom = document.getElementById('cq-jump-warroom');
  const cqJumpSources = document.getElementById('cq-jump-sources');
  const cqOpenDeck = document.getElementById('cq-open-deck');
  const btnShortlistToPillars = document.getElementById('btn-shortlist-to-pillars');

  // Load Data
  let playersData = null;
  let creditsData = {};
  let metaData = {};
  let reconciliationData = null;

  try {
    const pRes = await fetch('./data/players.json');
    playersData = await pRes.json();
  } catch (err) {
    console.error('Failed to load players.json:', err);
  }

  try {
    const cRes = await fetch('./data/credits.json');
    const cJson = await cRes.json();
    if (cJson && cJson.credits) {
      cJson.credits.forEach((c) => {
        if (c.player) {
          creditsData[c.player] = c;
        }
      });
    }
  } catch (err) {
    console.error('Failed to load credits.json:', err);
  }

  try {
    const mRes = await fetch('./data/players_meta.json');
    const mJson = await mRes.json();
    if (mJson && mJson.players) {
      metaData = mJson.players;
    }
  } catch (err) {
    console.error('Failed to load players_meta.json:', err);
  }

  try {
    const rRes = await fetch('./data/reconciliation.json');
    reconciliationData = await rRes.json();
  } catch (err) {
    console.error('Failed to load reconciliation.json:', err);
  }

  const topBatters = (playersData && playersData.top_batters) || [];
  const topBowlers = (playersData && playersData.top_bowlers) || [];

  // Augment with Verified Metadata
  function enrichPlayer(p) {
    const meta = metaData[p.name];
    p.verified_meta = meta || null;
    const isVerified = meta && meta.verified;
    p.is_price_verified = !!(isVerified && meta.price && !meta.price.toLowerCase().includes('not listed') && !meta.price.toLowerCase().includes('unverified'));
    
    // Price Rule: Only values with verified:true; otherwise show "Not listed yet"
    p.display_price = (isVerified && meta.price) ? meta.price : 'Not listed yet';
    p.display_role = (meta && meta.role) || p.role || p.slot;
    p.display_nationality = (meta && meta.nationality) || p.nationality || p.team;
    p.meta_notes = meta && meta.notes;
    p.source_url = meta && meta.source_url;
  }

  topBatters.forEach(enrichPlayer);
  topBowlers.forEach(enrichPlayer);

  // State
  let currentCategory = 'batters'; // 'batters' | 'bowlers'
  let onlyEligible = false;

  const use3D = isWebGLAvailable() && window.innerWidth >= 768;

  // Initialize Lenis Smooth Scroll
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true
  });

  let isTabHidden = false;
  document.addEventListener('visibilitychange', () => {
    isTabHidden = document.hidden;
  });

  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => {
    if (!isTabHidden) {
      lenis.raf(time * 1000);
    }
  });
  gsap.ticker.lagSmoothing(0);

  // Navigation Scroll Links
  function smoothScrollTo(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
      lenis.scrollTo(el, { duration: 1.3, offset: -85 });
    }
  }

  if (btnJumpChamber) btnJumpChamber.addEventListener('click', () => smoothScrollTo('section-chamber'));
  if (btnJumpRadar) btnJumpRadar.addEventListener('click', () => smoothScrollTo('section-radar-duel'));
  if (btnJumpShortlist) btnJumpShortlist.addEventListener('click', () => smoothScrollTo('section-shortlist'));
  if (btnJumpWarroom) btnJumpWarroom.addEventListener('click', () => smoothScrollTo('section-war-room'));
  if (btnJumpSources) btnJumpSources.addEventListener('click', () => smoothScrollTo('section-sources-methodology'));
  if (cqJumpRadar) cqJumpRadar.addEventListener('click', () => smoothScrollTo('section-radar-duel'));
  if (cqJumpShortlist) cqJumpShortlist.addEventListener('click', () => smoothScrollTo('section-shortlist'));
  if (cqJumpWarroom) cqJumpWarroom.addEventListener('click', () => smoothScrollTo('section-war-room'));
  if (cqJumpSources) cqJumpSources.addEventListener('click', () => smoothScrollTo('section-sources-methodology'));
  if (btnShortlistToPillars) btnShortlistToPillars.addEventListener('click', () => smoothScrollTo('section-chamber'));

  let stepwell = null;

  if (use3D && canvas) {
    try {
      stepwell = createStepwellScene(canvas, (player) => {
        openPlayerModal(player);
      }, creditsData);
      stepwell.setPillarsData(topBatters, false, creditsData);

      gsap.ticker.add(() => {
        if (!isTabHidden && stepwell) stepwell.render();
      });
    } catch (err) {
      console.warn('Stepwell 3D initialization failed, falling back to 2D:', err);
    }
  } else {
    console.log('Mobile viewport or no WebGL: Running in high-performance 2D mode.');
  }

  // Low-Power GPU Toggle
  let isLowPower = false;
  if (btnLowPower) {
    btnLowPower.addEventListener('click', () => {
      isLowPower = !isLowPower;
      btnLowPower.classList.toggle('active', isLowPower);
      document.body.classList.toggle('low-power-mode', isLowPower);
      if (stepwell) {
        stepwell.setLowPower(isLowPower);
      }
      btnLowPower.innerHTML = `<svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> ${isLowPower ? 'LOW POWER ON' : 'LOW POWER'}`;
    });
  }

  // Master Scrubbed ScrollTrigger (Camera Descent to Chamber)
  ScrollTrigger.create({
    trigger: '#section-hero',
    endTrigger: '#section-chamber',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 0.6,
    onUpdate: (self) => {
      const p = self.progress;

      if (stepwell) {
        stepwell.updateProgress(p);
      }

      if (meterFill) {
        meterFill.style.width = `${(p * 100).toFixed(1)}%`;
      }
      if (meterVal) {
        meterVal.textContent = p.toFixed(2);
      }

      // Smooth Full-Screen Chamber Transition: active in Chamber (p in [0.38, 0.99])
      const chamberSection = document.getElementById('section-chamber');
      if (chamberSection) {
        if (p >= 0.37) {
          chamberSection.style.opacity = '1';
          chamberSection.style.pointerEvents = 'none';
        } else {
          chamberSection.style.opacity = '0';
          chamberSection.style.pointerEvents = 'none';
        }
      }

      if (p >= 0.38) {
        document.body.classList.add('in-chamber');
      } else {
        document.body.classList.remove('in-chamber');
      }
    }
  });

  // Dissolve Chamber Controls as user enters War Room Suite
  ScrollTrigger.create({
    trigger: '#war-room-suite',
    start: 'top 85%',
    onEnter: () => {
      document.body.classList.remove('in-chamber');
      const chamberSection = document.getElementById('section-chamber');
      if (chamberSection) {
        chamberSection.style.opacity = '0';
        chamberSection.style.pointerEvents = 'none';
      }
    },
    onLeaveBack: () => {
      document.body.classList.add('in-chamber');
      const chamberSection = document.getElementById('section-chamber');
      if (chamberSection) {
        chamberSection.style.opacity = '1';
        chamberSection.style.pointerEvents = 'none';
      }
    }
  });

  // Animated Count-Up for Stats Panels
  const countUpElements = document.querySelectorAll('.count-up');
  countUpElements.forEach((el) => {
    const target = parseFloat(el.getAttribute('data-target') || '0');
    const isDecimal = el.hasAttribute('data-decimal');
    const decimals = parseInt(el.getAttribute('data-decimal') || '0', 10);

    ScrollTrigger.create({
      trigger: el.closest('.card-overlay') || el,
      start: 'top 85%',
      onEnter: () => {
        const obj = { val: 0 };
        gsap.to(obj, {
          val: target,
          duration: 1.6,
          ease: 'power2.out',
          onUpdate: () => {
            if (isDecimal) {
              el.textContent = obj.val.toFixed(decimals);
            } else {
              el.textContent = Math.round(obj.val).toLocaleString();
            }
          }
        });
      },
      once: true
    });
  });

  // ============================================================
  // MULTI-ATTRIBUTE FILTERS BAR
  // ============================================================
  const btnBatters = document.getElementById('btn-toggle-batters');
  const btnBowlers = document.getElementById('btn-toggle-bowlers');
  const btnRadarBatters = document.getElementById('btn-radar-batters');
  const btnRadarBowlers = document.getElementById('btn-radar-bowlers');
  const chkAuction = document.getElementById('chk-auction-eligible');

  const filterRoleEl = document.getElementById('filter-role');
  const filterNatEl = document.getElementById('filter-nationality');
  const filterPriceEl = document.getElementById('filter-price');
  const btnResetFilters = document.getElementById('btn-reset-filters');
  const filterCountEl = document.getElementById('filter-match-count');

  function matchesPriceTier(p, tier) {
    if (tier === 'all') return true;
    const str = (p.display_price || p.price_band || '').toLowerCase();

    if (tier === 'verified') {
      return p.verified_meta && p.verified_meta.verified && p.display_price !== 'Not listed yet';
    }
    if (tier === 'under2') {
      return str.includes('lakh') || str.includes('1.') || str.includes('1.10') || str.includes('1.50') || str.includes('1.00');
    }
    if (tier === '2to7') {
      return str.includes('2.') || str.includes('3.') || str.includes('4.') || str.includes('5.') || str.includes('6.') || str.includes('3-6') || str.includes('4-7') || str.includes('4-8');
    }
    if (tier === 'above7') {
      return str.includes('8.') || str.includes('9.') || str.includes('10') || str.includes('11') || str.includes('12') || str.includes('14') || str.includes('8-12') || str.includes('10-14');
    }
    return true;
  }

  function matchesRole(p, roleFilter) {
    if (roleFilter === 'all') return true;
    const r = (p.display_role || p.role || '').toLowerCase();

    if (roleFilter === 'opening') {
      return r.includes('opening') || r.includes('opener');
    }
    if (roleFilter === 'top_order') {
      return r.includes('top-order') || r.includes('top/middle') || r.includes('opener');
    }
    if (roleFilter === 'finisher') {
      return r.includes('finisher') || r.includes('lower-middle') || r.includes('middle-order');
    }
    if (roleFilter === 'allrounder') {
      return r.includes('all-rounder') || r.includes('allrounder');
    }
    if (roleFilter === 'pace') {
      return r.includes('fast') || r.includes('pace') || r.includes('medium');
    }
    if (roleFilter === 'spin') {
      return r.includes('spin') || r.includes('wrist') || r.includes('leg-break') || r.includes('orthodox');
    }
    return true;
  }

  function matchesNationality(p, natFilter) {
    if (natFilter === 'all') return true;
    const nat = (p.display_nationality || p.nationality || p.team || '').toLowerCase();
    const slot = (p.slot || '').toLowerCase();

    if (natFilter === 'indian') {
      return nat.includes('india') || slot.includes('indian');
    }
    if (natFilter === 'overseas') {
      return !nat.includes('india') || slot.includes('overseas');
    }
    return nat.includes(natFilter.toLowerCase());
  }

  function matchesActiveFilters(p) {
    const roleVal = filterRoleEl ? filterRoleEl.value : 'all';
    const natVal = filterNatEl ? filterNatEl.value : 'all';
    const priceVal = filterPriceEl ? filterPriceEl.value : 'all';

    const matchesEligible = !onlyEligible || p.is_available;
    const matchesR = matchesRole(p, roleVal);
    const matchesN = matchesNationality(p, natVal);
    const matchesP = matchesPriceTier(p, priceVal);

    return matchesEligible && matchesR && matchesN && matchesP;
  }

  function syncCohortButtons() {
    const isBatters = currentCategory === 'batters';
    if (btnBatters) btnBatters.classList.toggle('active', isBatters);
    if (btnBowlers) btnBowlers.classList.toggle('active', !isBatters);
    if (btnRadarBatters) btnRadarBatters.classList.toggle('active', isBatters);
    if (btnRadarBowlers) btnRadarBowlers.classList.toggle('active', !isBatters);
  }

  function applyFiltersAndUpdateAll() {
    const currentList = currentCategory === 'batters' ? topBatters : topBowlers;

    // 1. Live 3D Pillar Filter: Sinks non-matching pillars into pool
    if (stepwell && stepwell.applyPillarFilter) {
      stepwell.applyPillarFilter((p) => matchesActiveFilters(p));
    }

    // 2. Filtered list for 2D components
    const filteredList = currentList.filter(matchesActiveFilters);

    // 3. Counter Badge
    if (filterCountEl) {
      filterCountEl.textContent = `${filteredList.length} / ${currentList.length} Targets`;
    }

    // 4. Update UI views
    renderShortlist(filteredList);
    renderMobileLeaderboard(filteredList);
    renderAccessibleTable(filteredList);
  }

  function updateChamberView() {
    const list = currentCategory === 'batters' ? topBatters : topBowlers;
    const isBowlers = currentCategory === 'bowlers';

    if (stepwell) {
      stepwell.setPillarsData(list, isBowlers, creditsData);
    }

    applyFiltersAndUpdateAll();
    populateRadarSelectors(currentCategory);
  }

  // Toggle Events
  if (btnBatters && btnBowlers) {
    btnBatters.addEventListener('click', () => {
      currentCategory = 'batters';
      syncCohortButtons();
      updateChamberView();
    });

    btnBowlers.addEventListener('click', () => {
      currentCategory = 'bowlers';
      syncCohortButtons();
      updateChamberView();
    });
  }

  if (btnRadarBatters && btnRadarBowlers) {
    btnRadarBatters.addEventListener('click', () => {
      currentCategory = 'batters';
      syncCohortButtons();
      updateChamberView();
    });

    btnRadarBowlers.addEventListener('click', () => {
      currentCategory = 'bowlers';
      syncCohortButtons();
      updateChamberView();
    });
  }

  if (chkAuction) {
    chkAuction.addEventListener('change', (e) => {
      onlyEligible = e.target.checked;
      applyFiltersAndUpdateAll();
    });
  }

  if (filterRoleEl) filterRoleEl.addEventListener('change', applyFiltersAndUpdateAll);
  if (filterNatEl) filterNatEl.addEventListener('change', applyFiltersAndUpdateAll);
  if (filterPriceEl) filterPriceEl.addEventListener('change', applyFiltersAndUpdateAll);

  if (btnResetFilters) {
    btnResetFilters.addEventListener('click', () => {
      if (filterRoleEl) filterRoleEl.value = 'all';
      if (filterNatEl) filterNatEl.value = 'all';
      if (filterPriceEl) filterPriceEl.value = 'all';
      if (chkAuction) {
        chkAuction.checked = false;
        onlyEligible = false;
      }
      applyFiltersAndUpdateAll();
    });
  }

  // ============================================================
  // RADAR DUEL CHART INTEGRATION
  // ============================================================
  const radarChartEl = document.getElementById('radar-chart-container');
  const radarSrSummaryEl = document.getElementById('radar-sr-summary');
  let radarChart = null;

  if (radarChartEl) {
    radarChart = new RadarDuelChart(radarChartEl, radarSrSummaryEl);
  }

  const selP1 = document.getElementById('radar-sel-p1');
  const selP2 = document.getElementById('radar-sel-p2');
  const selP3 = document.getElementById('radar-sel-p3');
  const radarH2hTable = document.getElementById('radar-h2h-table');

  function populateRadarSelectors(cohort) {
    const list = cohort === 'bowlers' ? topBowlers : topBatters;

    [selP1, selP2].forEach((sel) => {
      if (!sel) return;
      const prevVal = sel.value;
      sel.innerHTML = '';
      list.forEach((p) => {
        const opt = document.createElement('option');
        opt.value = p.name;
        opt.textContent = `#${p.rank} · ${p.name} (${p.display_nationality || p.team})`;
        sel.appendChild(opt);
      });
      if (prevVal && list.some((p) => p.name === prevVal)) {
        sel.value = prevVal;
      }
    });

    if (selP3) {
      const prevVal3 = selP3.value;
      selP3.innerHTML = '<option value="none">(None - Duel 2 Players)</option>';
      list.forEach((p) => {
        const opt = document.createElement('option');
        opt.value = p.name;
        opt.textContent = `#${p.rank} · ${p.name} (${p.display_nationality || p.team})`;
        selP3.appendChild(opt);
      });
      if (prevVal3 && (prevVal3 === 'none' || list.some((p) => p.name === prevVal3))) {
        selP3.value = prevVal3;
      }
    }

    // Set sensible defaults
    if (selP1 && list[0]) selP1.value = list[0].name;
    if (selP2 && list[1]) selP2.value = list[1].name;
    if (selP3) selP3.value = 'none';

    updateRadarChartFromSelectors();
  }

  function updateRadarChartFromSelectors() {
    if (!radarChart) return;

    const list = currentCategory === 'bowlers' ? topBowlers : topBatters;
    const p1Name = selP1 ? selP1.value : '';
    const p2Name = selP2 ? selP2.value : '';
    const p3Name = selP3 ? selP3.value : 'none';

    const p1 = list.find((p) => p.name === p1Name) || list[0];
    const p2 = list.find((p) => p.name === p2Name) || list[1];
    const p3 = p3Name !== 'none' ? list.find((p) => p.name === p3Name) : null;

    const selectedPlayers = [p1, p2, p3].filter(Boolean);

    radarChart.setCategory(currentCategory);
    radarChart.updatePlayers(selectedPlayers);
    renderRadarH2hTable(selectedPlayers);
  }

  function renderRadarH2hTable(players) {
    if (!radarH2hTable || !players.length) return;
    radarH2hTable.innerHTML = '';

    const axes = currentCategory === 'bowlers' ? BOWLER_AXES : BATTER_AXES;

    // Header row
    const headRow = document.createElement('div');
    headRow.className = 'h2h-row h2h-header-row';
    headRow.innerHTML = `
      <div>METRIC</div>
      ${players.map((p, idx) => `<div class="h2h-val-cell p${idx + 1}-val">${p.name.split(' ')[0]}</div>`).join('')}
      ${players.length < 3 ? '<div>-</div>' : ''}
    `;
    radarH2hTable.appendChild(headRow);

    // Rows for each axis
    axes.forEach((ax) => {
      const row = document.createElement('div');
      row.className = 'h2h-row';

      const cells = players.map((p, idx) => {
        const val = ax.getValue(p);
        const base = ax.getBaseline(p);
        const delta = +(val - base).toFixed(1);
        const deltaSign = delta > 0 ? `+${delta}` : `${delta}`;

        return `
          <div class="h2h-val-cell p${idx + 1}-val">
            ${val}${ax.unit}
            <span class="h2h-delta">${deltaSign} vs base</span>
          </div>
        `;
      }).join('');

      row.innerHTML = `
        <div class="h2h-axis-label">${ax.label}</div>
        ${cells}
        ${players.length < 3 ? '<div style="color:rgba(255,255,255,0.2);">-</div>' : ''}
      `;
      radarH2hTable.appendChild(row);
    });
  }

  if (selP1) selP1.addEventListener('change', updateRadarChartFromSelectors);
  if (selP2) selP2.addEventListener('change', updateRadarChartFromSelectors);
  if (selP3) selP3.addEventListener('change', updateRadarChartFromSelectors);

  function duelPlayerInRadar(p) {
    const isBatter = 'sr_hp' in p;
    const targetCohort = isBatter ? 'batters' : 'bowlers';

    if (currentCategory !== targetCohort) {
      currentCategory = targetCohort;
      syncCohortButtons();
      updateChamberView();
      populateRadarSelectors(currentCategory);
    }

    if (selP2) {
      selP2.value = p.name;
    }

    updateRadarChartFromSelectors();

    const radarSec = document.getElementById('section-radar-duel');
    if (radarSec) {
      lenis.scrollTo(radarSec, { duration: 1.2 });
    }
  }

  // ============================================================
  // AUCTION CATALOGUE LEDGER (EDITORIAL STYLE TILE)
  // ============================================================
  const shortlistTableBody = document.getElementById('shortlist-table-body');
  const shortlistSrBody = document.getElementById('shortlist-sr-table-body');
  const shortlistMobileLedger = document.getElementById('shortlist-mobile-ledger');
  const ledgerPills = document.querySelectorAll('.ledger-pill');

  let activeLedgerFilter = 'all'; // 'all' | 'eligible' | 'batters' | 'bowlers'

  function renderShortlist() {
    let filtered = [];
    const all = [...topBatters, ...topBowlers];
    if (activeLedgerFilter === 'batters') {
      filtered = topBatters.filter(matchesActiveFilters);
    } else if (activeLedgerFilter === 'bowlers') {
      filtered = topBowlers.filter(matchesActiveFilters);
    } else if (activeLedgerFilter === 'eligible') {
      filtered = all.filter((p) => p.is_available && matchesActiveFilters(p)).sort((a, b) => (b.rating || 0) - (a.rating || 0));
    } else {
      filtered = all.filter(matchesActiveFilters).sort((a, b) => (b.rating || 0) - (a.rating || 0));
    }
    renderEditorialLedger(filtered);
  }

  function renderEditorialLedger(list) {
    renderLedgerDesktopTable(list);
    renderLedgerMobileCards(list);
  }

  function renderLedgerDesktopTable(list) {
    if (!shortlistTableBody) return;
    shortlistTableBody.innerHTML = '';
    if (shortlistSrBody) shortlistSrBody.innerHTML = '';

    if (!list.length) {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td colspan="9" class="td-empty">No candidate targets match active filters. Reset filters to restore registry.</td>`;
      shortlistTableBody.appendChild(tr);
      return;
    }

    list.forEach((p, idx) => {
      const tr = document.createElement('tr');
      tr.className = `ledger-row ${p.is_available ? 'row-available' : 'row-locked'}`;

      const credit = creditsData[p.name];
      const imgSrc = credit && credit.file ? `./${credit.file}` : '';
      const isBatter = 'sr_hp' in p;
      const rankNum = idx + 1 < 10 ? `0${idx + 1}` : `${idx + 1}`;

      const meta = p.verified_meta;
      const priceDisplay = meta && meta.price ? meta.price : 'Not listed yet';
      const isVerified = meta && meta.verified;
      const sourceUrl = meta && meta.source_url;
      const sourceName = (meta && meta.source_name) || 'Public Record';

      const verificationTag = (isVerified && sourceUrl)
        ? `<a href="${sourceUrl}" target="_blank" rel="noopener noreferrer" class="ledger-verified-link" title="Open public record: ${sourceName}">✓ VERIFIED <span class="ext-icon">↗</span></a>`
        : `<span class="ledger-unverified-tag">UNVERIFIED</span>`;

      let statusTag = '';
      if (p.is_available) {
        statusTag = `<span class="ledger-status-available">${ICONS.check} AVAILABLE</span>`;
      } else {
        const fullReason = (meta && meta.locked_reason) || p.locked_reason || 'Ineligible';
        let shortReason = 'LOCKED';
        if (fullReason.toLowerCase().includes('contracted to rr') || fullReason.toLowerCase().includes('retained')) {
          shortReason = 'CONTRACTED TO RR';
        } else if (fullReason.toLowerCase().includes('pakistan')) {
          shortReason = 'PAKISTANI (BCCI POLICY)';
        } else if (fullReason.toLowerCase().includes('retire')) {
          shortReason = 'RETIRED (POST-2024)';
        }
        statusTag = `<span class="ledger-status-locked" title="${fullReason}">${ICONS.lock} ${shortReason}</span>`;
      }

      tr.innerHTML = `
        <td class="td-rank">
          <span class="ledger-rank-mono">${rankNum}</span>
          <span class="ledger-cat-micro" style="display:block; font-size:0.62rem; color:var(--color-text-dim);">${isBatter ? 'BAT' : 'BWL'}</span>
        </td>
        <td class="td-candidate">
          <div class="ledger-player-lockup">
            <div class="ledger-avatar-box">
              <img src="${imgSrc}" alt="${p.name}" class="ledger-avatar duotone-img" onerror="this.style.display='none'" />
            </div>
            <div class="ledger-player-identity">
              <span class="ledger-player-name">${p.name}</span>
              <span class="ledger-player-meta">${p.display_nationality || p.team} · ${p.team}</span>
            </div>
          </div>
        </td>
        <td class="td-role">
          <span class="ledger-role-tag">${p.display_role}</span>
        </td>
        <td class="td-rating">
          <span class="rating-gold">${(p.rating || 0).toFixed(3)}</span>
        </td>
        <td class="td-ci">
          <span class="mono-ci">[${p.ci_low} – ${p.ci_high}]</span>
        </td>
        <td class="td-stability">
          <span class="mono-stability">${p.top10_pct}%</span>
        </td>
        <td class="td-price">
          <div class="ledger-price-block">
            <span class="ledger-price-figure">${priceDisplay}</span>
            ${verificationTag}
          </div>
        </td>
        <td class="td-status">
          ${statusTag}
        </td>
        <td class="td-actions">
          <div class="ledger-actions-group">
            <button class="ledger-btn-action btn-duel" data-name="${p.name}" title="Duel in Radar Matrix">${ICONS.radar} DUEL</button>
            ${p.is_available ? `<button class="ledger-btn-action btn-draft" data-name="${p.name}" title="Draft into Auction Simulator">${ICONS.building} DRAFT</button>` : ''}
            <button class="ledger-btn-action btn-dossier" data-name="${p.name}" title="Open Scouting Dossier">DOSSIER</button>
          </div>
        </td>
      `;

      const btnDuel = tr.querySelector('.btn-duel');
      if (btnDuel) btnDuel.addEventListener('click', () => duelPlayerInRadar(p));

      const btnDraft = tr.querySelector('.btn-draft');
      if (btnDraft) btnDraft.addEventListener('click', () => draftPlayerIntoSimulator(p));

      const btnDossier = tr.querySelector('.btn-dossier');
      if (btnDossier) btnDossier.addEventListener('click', () => openPlayerModal(p));

      shortlistTableBody.appendChild(tr);

      // Accessible Screen Reader Table
      if (shortlistSrBody) {
        const srTr = document.createElement('tr');
        srTr.innerHTML = `
          <td>${rankNum}</td>
          <td>${p.name}</td>
          <td>${p.display_role}</td>
          <td>${priceDisplay}</td>
          <td>${p.is_available ? 'Available' : (meta && meta.locked_reason) || p.locked_reason}</td>
        `;
        shortlistSrBody.appendChild(srTr);
      }
    });
  }

  function renderLedgerMobileCards(list) {
    if (!shortlistMobileLedger) return;
    shortlistMobileLedger.innerHTML = '';

    if (!list.length) {
      shortlistMobileLedger.innerHTML = `
        <div class="mobile-ledger-empty">
          No targets match active filters. Reset filters to restore registry.
        </div>
      `;
      return;
    }

    list.forEach((p, idx) => {
      const card = document.createElement('div');
      card.className = `mobile-ledger-item ${p.is_available ? 'item-available' : 'item-locked'}`;

      const credit = creditsData[p.name];
      const imgSrc = credit && credit.file ? `./${credit.file}` : '';
      const isBatter = 'sr_hp' in p;
      const rankNum = idx + 1 < 10 ? `0${idx + 1}` : `${idx + 1}`;

      const meta = p.verified_meta;
      const priceDisplay = meta && meta.price ? meta.price : 'Not listed yet';
      const isVerified = meta && meta.verified;
      const sourceUrl = meta && meta.source_url;
      const sourceName = (meta && meta.source_name) || 'Public Record';

      const verificationTag = (isVerified && sourceUrl)
        ? `<a href="${sourceUrl}" target="_blank" rel="noopener noreferrer" class="ledger-verified-link" title="Open public record: ${sourceName}">✓ VERIFIED <span class="ext-icon">↗</span></a>`
        : `<span class="ledger-unverified-tag">UNVERIFIED</span>`;

      let statusTag = '';
      if (p.is_available) {
        statusTag = `<span class="ledger-status-available">${ICONS.check} AVAILABLE</span>`;
      } else {
        const fullReason = (meta && meta.locked_reason) || p.locked_reason || 'Ineligible';
        let shortReason = 'LOCKED';
        if (fullReason.toLowerCase().includes('contracted to rr') || fullReason.toLowerCase().includes('retained')) {
          shortReason = 'CONTRACTED TO RR';
        } else if (fullReason.toLowerCase().includes('pakistan')) {
          shortReason = 'PAKISTANI (BCCI POLICY)';
        } else if (fullReason.toLowerCase().includes('retire')) {
          shortReason = 'RETIRED (POST-2024)';
        }
        statusTag = `<span class="ledger-status-locked" title="${fullReason}">${ICONS.lock} ${shortReason}</span>`;
      }

      card.innerHTML = `
        <div class="ml-top-row">
          <div class="ml-rank-name">
            <span class="ml-rank">${rankNum}</span>
            <span class="ml-cat" style="font-family:var(--font-mono); font-size:0.65rem; color:var(--color-text-dim); margin-right:0.3rem;">[${isBatter ? 'BAT' : 'BWL'}]</span>
            <div class="ml-name-lockup">
              <span class="ml-name">${p.name}</span>
              <span class="ml-sub">${p.display_role} · ${p.display_nationality || p.team}</span>
            </div>
          </div>
          <div class="ml-rating-block">
            <span class="rating-lbl">RATING</span>
            <span class="rating-gold">${(p.rating || 0).toFixed(3)}</span>
          </div>
        </div>

        <div class="ml-metrics-row">
          <div class="ml-metric">
            <span class="mlm-lbl">90% EMPIRICAL CI</span>
            <span class="mlm-val">[${p.ci_low} – ${p.ci_high}]</span>
          </div>
          <div class="ml-metric">
            <span class="mlm-lbl">STABILITY</span>
            <span class="mlm-val">${p.top10_pct}%</span>
          </div>
          <div class="ml-metric">
            <span class="mlm-lbl">VALUATION</span>
            <span class="mlm-val" style="font-size:0.75rem; line-height:1.2;">${priceDisplay}</span>
            ${verificationTag}
          </div>
        </div>

        <div class="ml-status-row">
          ${statusTag}
          <div class="ml-actions">
            <button class="ml-btn btn-duel" data-name="${p.name}">${ICONS.radar} DUEL</button>
            ${p.is_available ? `<button class="ml-btn btn-draft" data-name="${p.name}">${ICONS.building} DRAFT</button>` : ''}
            <button class="ml-btn btn-dossier" data-name="${p.name}">DOSSIER</button>
          </div>
        </div>
      `;

      const btnDuel = card.querySelector('.btn-duel');
      if (btnDuel) btnDuel.addEventListener('click', () => duelPlayerInRadar(p));

      const btnDraft = card.querySelector('.btn-draft');
      if (btnDraft) btnDraft.addEventListener('click', () => draftPlayerIntoSimulator(p));

      const btnDossier = card.querySelector('.btn-dossier');
      if (btnDossier) btnDossier.addEventListener('click', () => openPlayerModal(p));

      shortlistMobileLedger.appendChild(card);
    });
  }

  // Bind Ledger Filter Tabs
  ledgerPills.forEach((pill) => {
    pill.addEventListener('click', () => {
      ledgerPills.forEach((p) => p.classList.remove('active'));
      pill.classList.add('active');
      const mode = pill.getAttribute('data-filter');
      activeLedgerFilter = mode;

      renderShortlist();
    });
  });

  // FAQ Accordion Handlers
  const faqAccordion = document.getElementById('faq-accordion');
  if (faqAccordion) {
    const faqItems = faqAccordion.querySelectorAll('.faq-item');
    faqItems.forEach((item) => {
      const qBtn = item.querySelector('.faq-question-btn');
      if (qBtn) {
        qBtn.addEventListener('click', () => {
          const isActive = item.classList.contains('active');
          faqItems.forEach((other) => {
            other.classList.remove('active');
            const otherBtn = other.querySelector('.faq-question-btn');
            if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
          });
          if (!isActive) {
            item.classList.add('active');
            qBtn.setAttribute('aria-expanded', 'true');
          }
        });
      }
    });
  }

  // Executive CTA & Footer Buttons
  const ctaBtnDeck = document.getElementById('cta-btn-deck');
  const ctaBtnPrint = document.getElementById('cta-btn-print');
  const ctaBtnTop = document.getElementById('cta-btn-top');
  const footerBtnTop = document.getElementById('footer-btn-top');

  if (ctaBtnDeck) ctaBtnDeck.addEventListener('click', () => deck.open(0));
  if (ctaBtnPrint) ctaBtnPrint.addEventListener('click', () => window.print());
  if (ctaBtnTop) ctaBtnTop.addEventListener('click', () => lenis.scrollTo(0, { duration: 1.5 }));
  if (footerBtnTop) footerBtnTop.addEventListener('click', () => lenis.scrollTo(0, { duration: 1.5 }));

  // ============================================================
  // MOBILE LEADERBOARD & ACCESSIBLE TABLE
  // ============================================================
  const mobileListEl = document.getElementById('mobile-chamber-list');
  const srTableBody = document.getElementById('sr-table-body');

  function renderMobileLeaderboard(list) {
    if (!mobileListEl) return;
    mobileListEl.innerHTML = '';

    list.forEach((p) => {
      const card = document.createElement('div');
      card.className = `mobile-player-card ${p.is_available ? '' : 'is-locked'}`;
      card.setAttribute('role', 'button');
      card.setAttribute('tabindex', '0');

      card.innerHTML = `
        <div class="mp-rank">#${p.rank}</div>
        <div class="mp-info">
          <div class="mp-name">${p.name} ${p.is_available ? '' : '<span class="lock-tag">LOCKED</span>'}</div>
          <div class="mp-sub">${p.display_role} · ${p.display_nationality || p.team}</div>
        </div>
        <div class="mp-rating">${(p.rating || 0).toFixed(3)}</div>
      `;

      card.addEventListener('click', () => openPlayerModal(p));
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openPlayerModal(p);
        }
      });

      mobileListEl.appendChild(card);
    });
  }

  function renderAccessibleTable(list) {
    if (!srTableBody) return;
    srTableBody.innerHTML = '';

    list.forEach((p) => {
      const tr = document.createElement('tr');
      const ci = `[${p.ci_low} - ${p.ci_high}]`;
      const avail = p.is_available ? 'Available' : `Locked: ${p.locked_reason}`;

      tr.innerHTML = `
        <td>${p.rank}</td>
        <td>${p.name}</td>
        <td>${p.display_role}</td>
        <td>${(p.rating || 0).toFixed(3)}</td>
        <td>${ci}</td>
        <td>${p.top10_pct}%</td>
        <td>${p.hp_balls}</td>
        <td>${avail}</td>
        <td><button class="sr-inspect-btn">View Dossier</button></td>
      `;

      const btn = tr.querySelector('button');
      if (btn) {
        btn.addEventListener('click', () => openPlayerModal(p));
      }

      srTableBody.appendChild(tr);
    });
  }

  // ============================================================
  // PLAYER DOSSIER MODAL / DRAWER
  // ============================================================
  const modal = document.getElementById('player-modal');
  const backdrop = document.getElementById('modal-backdrop');
  const btnCloseModal = document.getElementById('btn-close-modal');

  const modalRank = document.getElementById('modal-rank-badge');
  const modalRole = document.getElementById('modal-role-badge');
  const modalLock = document.getElementById('modal-lock-badge');
  const modalName = document.getElementById('modal-player-name');
  const modalTeam = document.getElementById('modal-team-line');

  const modalFrame = document.getElementById('modal-portrait-frame');
  const modalImg = document.getElementById('modal-portrait-img');
  const modalCredit = document.getElementById('modal-credit-line');

  const modalRating = document.getElementById('modal-rating');
  const modalCI = document.getElementById('modal-ci');
  const modalStability = document.getElementById('modal-stability');

  const m1Lbl = document.getElementById('modal-metric-1-lbl');
  const m1Val = document.getElementById('modal-metric-1-val');
  const m2Lbl = document.getElementById('modal-metric-2-lbl');
  const m2Val = document.getElementById('modal-metric-2-val');
  const mDotVal = document.getElementById('modal-dot-val');
  const m3Lbl = document.getElementById('modal-metric-3-lbl');
  const m3Val = document.getElementById('modal-metric-3-val');
  const mSample = document.getElementById('modal-sample-val');

  const modalRrFit = document.getElementById('modal-rr-fit');
  const modalRisk = document.getElementById('modal-risk');
  const modalAuction = document.getElementById('modal-auction-note');

  function openPlayerModal(p) {
    if (!modal || !p) return;

    modalRank.textContent = `RANK #${p.rank}`;
    modalRole.textContent = (p.display_role || p.role || '').toUpperCase();
    modalName.textContent = p.name;
    modalTeam.textContent = `${p.team} · ${p.display_nationality || 'Cricket'}`;

    if (!p.is_available) {
      modalLock.classList.remove('hidden');
      modalLock.innerHTML = `<svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="11" width="18" height="11" rx="2" stroke-width="2"/><path d="M7 11V7a5 5 0 0110 0v4" stroke-width="2" stroke-linecap="round"/></svg> ${p.locked_reason || 'INELIGIBLE'}`;
    } else {
      modalLock.classList.add('hidden');
    }

    // Portrait & Duotone
    const credit = creditsData[p.name];
    if (credit && credit.file) {
      modalImg.src = `./${credit.file}`;
      modalCredit.textContent = credit.fallback
        ? 'Bespoke War Room SVG Monogram'
        : `Photo: ${credit.author || 'Wikimedia'} (${credit.license})`;

      if (credit.file.endsWith('.svg')) {
        modalFrame.classList.remove('duotone-active');
      } else {
        modalFrame.classList.add('duotone-active');
      }
    } else {
      modalImg.src = '';
      modalCredit.textContent = 'War Room Asset';
      modalFrame.classList.remove('duotone-active');
    }

    // Core Ratings
    modalRating.textContent = (p.rating || 0).toFixed(3);
    modalCI.textContent = `[${p.ci_low} - ${p.ci_high}]`;
    modalStability.textContent = `${p.top10_pct || 0}%`;

    // Category Metrics
    const isBatter = 'sr_hp' in p;
    if (isBatter) {
      m1Lbl.textContent = 'HP STRIKE RATE';
      m1Val.textContent = p.sr_hp;
      m2Lbl.textContent = 'BASELINE SR';
      m2Val.textContent = p.sr_lp;
      mDotVal.textContent = `${p.dot_pct_hp || 0}%`;
      m3Lbl.textContent = 'BOUNDARY %';
      m3Val.textContent = `${p.boundary_pct_hp || 0}%`;
    } else {
      m1Lbl.textContent = 'HP ECONOMY';
      m1Val.textContent = p.econ_hp;
      m2Lbl.textContent = 'BASELINE ECON';
      m2Val.textContent = p.econ_lp;
      mDotVal.textContent = `${p.dot_pct_hp || 0}%`;
      m3Lbl.textContent = 'WICKET RATE';
      m3Val.textContent = `${p.wkt_rate_hp || 0}%`;
    }

    mSample.textContent = `${p.hp_balls} High-Pressure Balls (${p.hp_matches} Matches)`;

    // Narratives
    modalRrFit.textContent = p.rr_fit || 'Target profile matches franchise objectives.';
    modalRisk.textContent = p.risk || 'No critical structural risk identified.';
    modalAuction.textContent = `${p.status} · Price: ${p.display_price || 'Not listed yet'}`;

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closePlayerModal() {
    if (!modal) return;
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }

  if (btnCloseModal) btnCloseModal.addEventListener('click', closePlayerModal);
  if (backdrop) backdrop.addEventListener('click', closePlayerModal);

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
      closePlayerModal();
    }
  });

  // ============================================================
  // PHASE 6: WAR ROOM SIMULATOR ENGINE (JHAROKHA ARCHES)
  // ============================================================
  const simContainer = document.getElementById('simulator-container');
  let simulator = null;

  const allEligiblePlayers = [...topBatters, ...topBowlers].filter((p) => p.is_available);

  if (simContainer) {
    simulator = new WarRoomSimulator(simContainer, {
      eligiblePlayers: allEligiblePlayers,
      creditsData,
      metaData
    });
  }

  function draftPlayerIntoSimulator(p) {
    if (!simulator) return;

    const r = (p.display_role || p.role || '').toLowerCase();
    const nat = (p.display_nationality || p.nationality || p.slot || '').toLowerCase();
    const isIndian = nat.includes('india') || (p.slot || '').toLowerCase().includes('indian');

    let targetSlot = 1; // default to finisher / middle order
    if (r.includes('fast') || r.includes('pace') || r.includes('medium')) {
      if (isIndian && !simulator.slots[3].assigned) {
        targetSlot = 3; // Indian Pace Depth
      } else {
        targetSlot = 0; // Death-Overs Pacer
      }
    } else if (r.includes('spin') || r.includes('wrist') || r.includes('orthodox') || r.includes('leg-break')) {
      targetSlot = 2; // Wicket-Taking Spinner
    } else {
      targetSlot = 1; // Middle-Order Finisher
    }

    // If preferred slot is occupied, pick first unoccupied slot
    if (simulator.slots[targetSlot].assigned) {
      const freeIdx = simulator.slots.findIndex((s) => !s.assigned);
      if (freeIdx !== -1) {
        targetSlot = freeIdx;
      }
    }

    simulator.assignPlayerToSlot(targetSlot, p);

    const warRoomSec = document.getElementById('section-war-room');
    if (warRoomSec) {
      lenis.scrollTo(warRoomSec, { duration: 1.3, offset: -85 });
    }
  }

  // Initial renders
  applyFiltersAndUpdateAll();
  populateRadarSelectors(currentCategory);

  // Initialize Present Deck (16:9 Presentation Overlay)
  const deck = new PresentDeck();
  if (btnOpenDeck) btnOpenDeck.addEventListener('click', () => deck.open(0));
  if (cqOpenDeck) cqOpenDeck.addEventListener('click', () => deck.open(0));

  // Populate Print Deck for PDF export (All 5 slides formatted for landscape print)
  const printContainer = document.getElementById('print-all-slides');
  if (printContainer && deck && deck.slidesData) {
    printContainer.innerHTML = deck.slidesData.map((s, idx) => `
      <div class="print-slide-page">
        <div class="print-slide-header">
          <div class="print-slide-tag">RAJASTHAN ROYALS WAR ROOM · ${s.tag} · हल्ला बोल</div>
          <h2 class="print-slide-title">${s.title}</h2>
          <p class="print-slide-subtitle">${s.subtitle}</p>
        </div>
        <div class="print-slide-body">
          ${s.content}
        </div>
        <div class="print-slide-footer">
          <span>SupeRR Selector Season 2 · Round 1 Submission</span>
          <span>Slide ${idx + 1} of ${deck.slidesData.length}</span>
          <span>Target: IPL 2027 Mini-Auction (Goa, 16 Dec 2026)</span>
        </div>
      </div>
    `).join('');
  }

  // Render Sources & Methodology Audit
  const sourcesContainer = document.getElementById('sources-container');
  if (sourcesContainer) {
    renderSourcesAndMethodology(sourcesContainer, reconciliationData, creditsData, metaData);
  }

  // Fade out loader after slight buffer
  setTimeout(() => {
    if (loader) {
      loader.classList.add('hidden');
    }
  }, 400);
});
