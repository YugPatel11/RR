import { scaleLinear } from 'd3-scale';
import { lineRadial, curveLinearClosed } from 'd3-shape';
import gsap from 'gsap';

// Configuration & Palettes (Editorial: Navy 70 / Bone 20 / Pink 8 / Zero Gold in Radar)
const PLAYER_COLORS = [
  { solid: '#EA1A85', fill: 'rgba(234, 26, 133, 0.18)', ghost: '#EA1A85', name: 'Royals Pink' },
  { solid: '#E6E4DD', fill: 'rgba(230, 228, 221, 0.16)', ghost: '#E6E4DD', name: 'Bone Off-White' },
  { solid: '#38BDF8', fill: 'rgba(56, 189, 248, 0.18)', ghost: '#38BDF8', name: 'Electric Cyan' }
];

export const BATTER_AXES = [
  {
    id: 'sr_hp',
    label: 'HP Strike Rate',
    desc: 'Strike rate in crisis balls',
    domain: [120, 270],
    unit: '',
    getValue: (p) => p.sr_hp || 0,
    getBaseline: (p) => p.sr_lp || 139.1
  },
  {
    id: 'sr_lp',
    label: 'Normal Strike Rate',
    desc: 'Baseline match strike rate',
    domain: [120, 230],
    unit: '',
    getValue: (p) => p.sr_lp || 0,
    getBaseline: (p) => p.sr_lp || 139.1
  },
  {
    id: 'boundary_pct',
    label: 'Boundary %',
    desc: 'Four & six ball percentage',
    domain: [15, 50],
    unit: '%',
    getValue: (p) => p.boundary_pct_hp || 0,
    getBaseline: () => 18.0 // Band 1 baseline
  },
  {
    id: 'dot_pct',
    label: 'Dot % Avoidance',
    desc: 'Lower dot ball rate is superior',
    domain: [48, 24], // Inverted: lower dot% reaches outer perimeter
    unit: '%',
    isInverted: true,
    getValue: (p) => p.dot_pct_hp || 0,
    getBaseline: () => 36.9 // Band 1 baseline
  },
  {
    id: 'impact',
    label: 'Clutch Impact',
    desc: 'Run expectation surplus',
    domain: [0.0, 1.25],
    unit: '',
    getValue: (p) => p.impact || 0,
    getBaseline: () => 0.0
  },
  {
    id: 'stability',
    label: 'Bootstrap Stability',
    desc: '% iterations in Top 10',
    domain: [0, 100],
    unit: '%',
    getValue: (p) => p.top10_pct || 0,
    getBaseline: () => 50.0
  }
];

export const BOWLER_AXES = [
  {
    id: 'econ_hp',
    label: 'HP Economy',
    desc: 'Lower is superior (inverted)',
    domain: [10.5, 4.8], // Inverted: lower economy reaches outer rim!
    unit: ' rpo',
    isInverted: true,
    getValue: (p) => p.econ_hp || 0,
    getBaseline: (p) => p.econ_lp || 8.3
  },
  {
    id: 'econ_lp',
    label: 'Normal Economy',
    desc: 'Baseline economy (lower is superior)',
    domain: [10.5, 6.0], // Inverted
    unit: ' rpo',
    isInverted: true,
    getValue: (p) => p.econ_lp || 0,
    getBaseline: (p) => p.econ_lp || 8.3
  },
  {
    id: 'wkt_rate',
    label: 'Wicket Rate %',
    desc: 'Dismissal frequency per ball',
    domain: [4.0, 16.0],
    unit: '%',
    getValue: (p) => p.wkt_rate_hp || 0,
    getBaseline: () => 4.8 // Band 1 baseline
  },
  {
    id: 'dot_pct',
    label: 'Dot % (Pressure)',
    desc: 'Dot ball containment frequency',
    domain: [35, 62],
    unit: '%',
    getValue: (p) => p.dot_pct_hp || 0,
    getBaseline: () => 36.9 // Band 1 baseline
  },
  {
    id: 'stability',
    label: 'Bootstrap Stability',
    desc: '% iterations in Top 10',
    domain: [0, 100],
    unit: '%',
    getValue: (p) => p.top10_pct || 0,
    getBaseline: () => 50.0
  }
];

export class RadarDuelChart {
  constructor(containerEl, srSummaryEl) {
    this.container = containerEl;
    this.srSummaryEl = srSummaryEl;

    this.width = 540;
    this.height = 460;
    this.cx = this.width / 2;
    this.cy = this.height / 2;
    this.rMin = 24;
    this.rMax = 165;

    this.category = 'batters'; // 'batters' | 'bowlers'
    this.axes = BATTER_AXES;
    this.players = []; // Array of up to 3 player objects

    // Internal state for GSAP morphing: current radius values
    this.state = [
      { pressure: [], baseline: [] },
      { pressure: [], baseline: [] },
      { pressure: [], baseline: [] }
    ];

    this.initSVG();
  }

  initSVG() {
    this.container.innerHTML = '';

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', `0 0 ${this.width} ${this.height}`);
    svg.setAttribute('class', 'radar-svg');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Radar Duel chart comparing selected players under pressure versus baseline');

    // Defs for gradients & filters
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    defs.innerHTML = `
      <filter id="radar-glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>
    `;
    svg.appendChild(defs);

    // Group centered at (cx, cy)
    this.chartG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    this.chartG.setAttribute('transform', `translate(${this.cx}, ${this.cy})`);
    svg.appendChild(this.chartG);

    // Web background group
    this.webG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    this.webG.setAttribute('class', 'radar-web');
    this.chartG.appendChild(this.webG);

    // Polygons layer group
    this.polysG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    this.polysG.setAttribute('class', 'radar-polygons');
    this.chartG.appendChild(this.polysG);

    // Labels group
    this.labelsG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    this.labelsG.setAttribute('class', 'radar-labels');
    this.chartG.appendChild(this.labelsG);

    // Tooltip overlay
    this.tooltipG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    this.tooltipG.setAttribute('class', 'radar-tooltip-group');
    this.tooltipG.style.pointerEvents = 'none';
    this.chartG.appendChild(this.tooltipG);

    this.container.appendChild(svg);
    this.svg = svg;

    this.renderGrid();
  }

  setCategory(category) {
    this.category = category;
    this.axes = category === 'bowlers' ? BOWLER_AXES : BATTER_AXES;
    this.renderGrid();
  }

  renderGrid() {
    this.webG.innerHTML = '';
    this.labelsG.innerHTML = '';

    const numAxes = this.axes.length;
    const radialGen = lineRadial()
      .angle((d) => d.angle)
      .radius((d) => d.radius)
      .curve(curveLinearClosed);

    // Concentric Web Rings (5 rings: 20%, 40%, 60%, 80%, 100%)
    const ringPercents = [0.2, 0.4, 0.6, 0.8, 1.0];
    ringPercents.forEach((pct, idx) => {
      const ringRadius = this.rMin + pct * (this.rMax - this.rMin);
      const ringPoints = this.axes.map((_, i) => ({
        angle: (i * 2 * Math.PI) / numAxes,
        radius: ringRadius
      }));

      const ringPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      ringPath.setAttribute('d', radialGen(ringPoints));
      ringPath.setAttribute('class', `radar-ring ${idx === 4 ? 'outer-ring' : ''}`);
      this.webG.appendChild(ringPath);

      // Percentage label on top axis
      const ringLbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      ringLbl.setAttribute('x', '0');
      ringLbl.setAttribute('y', `${-ringRadius + 11}`);
      ringLbl.setAttribute('class', 'radar-ring-text');
      ringLbl.textContent = `${Math.round(pct * 100)}%`;
      this.webG.appendChild(ringLbl);
    });

    // Radial Spokes and Axis Labels
    this.axes.forEach((axis, i) => {
      const angle = (i * 2 * Math.PI) / numAxes;
      const xOuter = Math.sin(angle) * this.rMax;
      const yOuter = -Math.cos(angle) * this.rMax;

      // Spoke line
      const spoke = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      spoke.setAttribute('x1', '0');
      spoke.setAttribute('y1', '0');
      spoke.setAttribute('x2', `${xOuter}`);
      spoke.setAttribute('y2', `${yOuter}`);
      spoke.setAttribute('class', 'radar-spoke');
      this.webG.appendChild(spoke);

      // Label positioning
      const labelDist = this.rMax + 26;
      const lx = Math.sin(angle) * labelDist;
      const ly = -Math.cos(angle) * labelDist;

      const gLbl = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      gLbl.setAttribute('transform', `translate(${lx}, ${ly})`);

      const textMain = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      textMain.setAttribute('class', 'axis-title');
      textMain.setAttribute('text-anchor', 'middle');
      textMain.setAttribute('dy', '-2');
      textMain.textContent = axis.label;
      gLbl.appendChild(textMain);

      const textSub = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      textSub.setAttribute('class', 'axis-sub');
      textSub.setAttribute('text-anchor', 'middle');
      textSub.setAttribute('dy', '11');
      textSub.textContent = axis.isInverted ? '▼ Lower is Better' : '▲ Higher is Better';
      gLbl.appendChild(textSub);

      this.labelsG.appendChild(gLbl);
    });
  }

  // Update selected players (array of 2 to 3 players)
  updatePlayers(players) {
    this.players = players.filter(Boolean).slice(0, 3);
    const numAxes = this.axes.length;

    // Build scales for each axis
    const scales = this.axes.map((ax) =>
      scaleLinear().domain(ax.domain).range([this.rMin, this.rMax]).clamp(true)
    );

    // Compute target radii for each player
    const targets = this.players.map((p) => {
      const pressureRadii = this.axes.map((ax, i) => scales[i](ax.getValue(p)));
      const baselineRadii = this.axes.map((ax, i) => scales[i](ax.getBaseline(p)));
      return { pressure: pressureRadii, baseline: baselineRadii };
    });

    // Ensure state array matches players length
    while (this.state.length < this.players.length) {
      this.state.push({
        pressure: new Array(numAxes).fill(this.rMin),
        baseline: new Array(numAxes).fill(this.rMin)
      });
    }

    // GSAP morph tween
    this.players.forEach((_, pIdx) => {
      const targetP = targets[pIdx].pressure;
      const targetB = targets[pIdx].baseline;

      // Initialize state if empty
      if (!this.state[pIdx].pressure.length || this.state[pIdx].pressure.length !== numAxes) {
        this.state[pIdx].pressure = new Array(numAxes).fill(this.rMin);
        this.state[pIdx].baseline = new Array(numAxes).fill(this.rMin);
      }

      gsap.to(this.state[pIdx].pressure, {
        endArray: targetP,
        duration: 0.65,
        ease: 'power2.out',
        onUpdate: () => this.drawPolygons()
      });

      gsap.to(this.state[pIdx].baseline, {
        endArray: targetB,
        duration: 0.65,
        ease: 'power2.out'
      });
    });

    this.drawPolygons();
    this.updateScreenReaderSummary();
  }

  drawPolygons() {
    this.polysG.innerHTML = '';
    const numAxes = this.axes.length;

    const radialGen = lineRadial()
      .angle((d) => d.angle)
      .radius((d) => d.radius)
      .curve(curveLinearClosed);

    this.players.forEach((player, pIdx) => {
      const col = PLAYER_COLORS[pIdx % PLAYER_COLORS.length];
      const pRadii = this.state[pIdx].pressure;
      const bRadii = this.state[pIdx].baseline;

      if (!pRadii || !pRadii.length) return;

      const pPoints = pRadii.map((r, i) => ({
        angle: (i * 2 * Math.PI) / numAxes,
        radius: r
      }));

      const bPoints = bRadii.map((r, i) => ({
        angle: (i * 2 * Math.PI) / numAxes,
        radius: r
      }));

      const playerG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      playerG.setAttribute('class', `player-radar-group player-${pIdx + 1}`);

      // 1. Baseline Ghost Layer (Dashed outline, no fill, lower opacity)
      const bPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      bPath.setAttribute('d', radialGen(bPoints));
      bPath.setAttribute('class', 'radar-layer-baseline');
      bPath.setAttribute('stroke', col.ghost);
      bPath.setAttribute('stroke-dasharray', '4,4');
      bPath.setAttribute('stroke-width', '1.6');
      bPath.setAttribute('fill', 'none');
      bPath.setAttribute('opacity', '0.55');
      playerG.appendChild(bPath);

      // 2. Pressure Solid Layer (Solid bold stroke with tinted translucent fill)
      const pPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      pPath.setAttribute('d', radialGen(pPoints));
      pPath.setAttribute('class', 'radar-layer-pressure');
      pPath.setAttribute('stroke', col.solid);
      pPath.setAttribute('stroke-width', '2.5');
      pPath.setAttribute('fill', col.fill);
      pPath.setAttribute('filter', 'url(#radar-glow)');
      playerG.appendChild(pPath);

      // 3. Vertex Dots on Pressure Layer
      pPoints.forEach((pt, i) => {
        const vx = Math.sin(pt.angle) * pt.radius;
        const vy = -Math.cos(pt.angle) * pt.radius;

        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', `${vx}`);
        dot.setAttribute('cy', `${vy}`);
        dot.setAttribute('r', '4');
        dot.setAttribute('fill', col.solid);
        dot.setAttribute('stroke', '#070B1E');
        dot.setAttribute('stroke-width', '1.5');
        dot.setAttribute('class', 'radar-vertex-dot');

        const axis = this.axes[i];
        const val = axis.getValue(player);
        const bVal = axis.getBaseline(player);

        dot.addEventListener('mouseenter', () => {
          this.showTooltip(vx, vy, player.name, axis.label, val, bVal, axis.unit, col.solid);
        });
        dot.addEventListener('mouseleave', () => {
          this.hideTooltip();
        });

        playerG.appendChild(dot);
      });

      this.polysG.appendChild(playerG);
    });
  }

  showTooltip(x, y, playerName, axisLabel, val, bVal, unit, color) {
    this.tooltipG.innerHTML = '';

    const ttBox = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    const offsetY = y > -20 ? y - 38 : y + 20;

    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', `${x - 70}`);
    rect.setAttribute('y', `${offsetY}`);
    rect.setAttribute('width', '140');
    rect.setAttribute('height', '36');
    rect.setAttribute('rx', '4');
    rect.setAttribute('fill', '#0B133A');
    rect.setAttribute('stroke', color);
    rect.setAttribute('stroke-width', '1.2');
    rect.setAttribute('filter', 'drop-shadow(0 4px 10px rgba(0,0,0,0.8))');
    ttBox.appendChild(rect);

    const txtName = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    txtName.setAttribute('x', `${x}`);
    txtName.setAttribute('y', `${offsetY + 14}`);
    txtName.setAttribute('text-anchor', 'middle');
    txtName.setAttribute('class', 'tt-name');
    txtName.textContent = `${playerName} · ${axisLabel}`;
    ttBox.appendChild(txtName);

    const txtVals = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    txtVals.setAttribute('x', `${x}`);
    txtVals.setAttribute('y', `${offsetY + 28}`);
    txtVals.setAttribute('text-anchor', 'middle');
    txtVals.setAttribute('class', 'tt-val');
    txtVals.textContent = `HP: ${val}${unit} (Base: ${bVal}${unit})`;
    ttBox.appendChild(txtVals);

    this.tooltipG.appendChild(ttBox);
  }

  hideTooltip() {
    this.tooltipG.innerHTML = '';
  }

  updateScreenReaderSummary() {
    if (!this.srSummaryEl || !this.players.length) return;

    const names = this.players.map((p) => p.name).join(' vs ');
    const isBatter = this.category === 'batters';

    let summary = `Radar Duel comparison for ${names} across ${this.axes.length} key metrics. `;

    this.players.forEach((p, idx) => {
      const pColor = PLAYER_COLORS[idx % PLAYER_COLORS.length].name;
      summary += `${p.name} (${pColor} curve): `;

      if (isBatter) {
        summary += `High Pressure Strike Rate ${p.sr_hp} (Baseline SR: ${p.sr_lp}, delta ${+(p.sr_hp - p.sr_lp).toFixed(1)}), `;
        summary += `Boundary % ${p.boundary_pct_hp}%, Dot % ${p.dot_pct_hp}%, `;
        summary += `Clutch Impact index ${p.impact}, Bootstrap Stability ${p.top10_pct}%. `;
      } else {
        summary += `High Pressure Economy ${p.econ_hp} rpo (Baseline Economy: ${p.econ_lp} rpo, delta ${+(p.econ_hp - p.econ_lp).toFixed(1)} rpo), `;
        summary += `Wicket Rate ${p.wkt_rate_hp}%, Dot % ${p.dot_pct_hp}%, `;
        summary += `Bootstrap Stability ${p.top10_pct}%. Lower economy indicates superior containment. `;
      }
    });

    this.srSummaryEl.textContent = summary;
  }
}

