import * as THREE from 'three';
import gsap from 'gsap';

/**
 * SuperRR Selector - 3D Stepwell & Ultimate Cricket Stadium Colosseum Engine
 * Franchise: Rajasthan Royals
 */
export function createStepwellScene(canvas, onPlayerSelect, initialCredits = {}) {
  let creditsData = initialCredits;

  // 1. Scene, Camera, Renderer
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x060B1E, 0.022);

  const camera = new THREE.PerspectiveCamera(
    48,
    window.innerWidth / window.innerHeight,
    0.1,
    250
  );

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance'
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;

  // 2. Camera & Look-At Spline Curves (Epic Stadium Colosseum Aerial Descent & Intimate Pitch Zoom)
  const camPoints = [
    new THREE.Vector3(0.0, 16.0, 26.0),    // 0: High-Altitude Colosseum Overlook (Hero)
    new THREE.Vector3(6.5, 8.5, 20.0),     // 1: Gliding down past Upper Grandstands (Formula)
    new THREE.Vector3(-5.2, 1.0, 15.0),    // 2: Descending past Club Tier & Corporate Suites (Band 1)
    new THREE.Vector3(1.8, -4.5, 11.0),    // 3: Sweeping over Boundary Rope into Inner Circle (Band 2/3)
    new THREE.Vector3(0.0, -9.6, 7.8)      // 4: Uncropped Colosseum Pitch Facing All 10 Pillars (Chamber)
  ];
  const camCurve = new THREE.CatmullRomCurve3(camPoints, false, 'centripetal');

  const lookPoints = [
    new THREE.Vector3(0.0, -8.0, 0.0),     // 0: Looking down into central illuminated arena
    new THREE.Vector3(0.0, -10.0, 0.0),    // 1: Tracking towards outfield
    new THREE.Vector3(0.0, -11.5, -0.5),   // 2: Framing central pitch & wickets
    new THREE.Vector3(0.0, -12.2, -1.0),   // 3: Centering on pitch arc
    new THREE.Vector3(0.0, -12.8, -2.8)    // 4: Direct Balanced Framing of 10-Pillar Arc
  ];
  const lookCurve = new THREE.CatmullRomCurve3(lookPoints, false, 'centripetal');

  // 3. Celestial Twilight Starfield (Jaipur Night Sky)
  const starGeo = new THREE.BufferGeometry();
  const starCount = 650;
  const starPos = new Float32Array(starCount * 3);
  for (let s = 0; s < starCount; s++) {
    const sTheta = Math.random() * Math.PI * 2;
    const sPhi = Math.acos(2 * Math.random() - 1);
    const sR = 90 + Math.random() * 45;
    starPos[s * 3] = sR * Math.sin(sPhi) * Math.cos(sTheta);
    starPos[s * 3 + 1] = Math.abs(sR * Math.cos(sPhi)) + 14; // Upper hemisphere
    starPos[s * 3 + 2] = sR * Math.sin(sPhi) * Math.sin(sTheta);
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  const starMat = new THREE.PointsMaterial({
    color: 0xE2E8F0,
    size: 0.7,
    transparent: true,
    opacity: 0.75,
    sizeAttenuation: true
  });
  const starPoints = new THREE.Points(starGeo, starMat);
  scene.add(starPoints);

  // ============================================================
  // ULTIMATE CRICKET STADIUM COLOSSEUM & JAIPUR NIGHT SKYLINE
  // (Visible across 100% of the scroll journey - ZERO box rings)
  // ============================================================
  const stadiumArenaGroup = new THREE.Group();
  stadiumArenaGroup.visible = true;
  scene.add(stadiumArenaGroup);

  // A. Lush Circular Cricket Outfield Turf (Professional Lawn)
  const outfieldGeo = new THREE.CircleGeometry(21.5, 64);
  const outfieldMat = new THREE.MeshStandardMaterial({
    color: 0x124724,
    roughness: 0.85,
    metalness: 0.03
  });
  const outfield = new THREE.Mesh(outfieldGeo, outfieldMat);
  outfield.rotation.x = -Math.PI / 2;
  outfield.position.y = -14.78;
  stadiumArenaGroup.add(outfield);

  // Concentric Alternating Grass Mowing Bands
  for (let r = 1; r <= 7; r++) {
    const rGeo = new THREE.RingGeometry(r * 2.9 - 0.4, r * 2.9, 64);
    const rMat = new THREE.MeshBasicMaterial({
      color: r % 2 === 0 ? 0x1A6032 : 0x0D361B,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.40
    });
    const rMesh = new THREE.Mesh(rGeo, rMat);
    rMesh.rotation.x = -Math.PI / 2;
    rMesh.position.y = -14.77;
    stadiumArenaGroup.add(rMesh);
  }

  // B. Central 22-Yard Clay Cricket Pitch Strip
  const pitchGeo = new THREE.PlaneGeometry(2.3, 9.6);
  const pitchMat = new THREE.MeshStandardMaterial({
    color: 0xC6A46A,
    roughness: 0.90,
    metalness: 0.02
  });
  const pitch = new THREE.Mesh(pitchGeo, pitchMat);
  pitch.rotation.x = -Math.PI / 2;
  pitch.position.set(0, -14.76, -1.8);
  stadiumArenaGroup.add(pitch);

  // Crisp White Popping, Bowling, and Return Crease Lines
  const creaseMat = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
  const crease1 = new THREE.Mesh(new THREE.PlaneGeometry(2.1, 0.08), creaseMat);
  crease1.rotation.x = -Math.PI / 2;
  crease1.position.set(0, -14.75, 2.0);
  stadiumArenaGroup.add(crease1);

  const crease2 = new THREE.Mesh(new THREE.PlaneGeometry(2.1, 0.08), creaseMat);
  crease2.rotation.x = -Math.PI / 2;
  crease2.position.set(0, -14.75, -5.6);
  stadiumArenaGroup.add(crease2);

  [-1.0, 1.0].forEach((rx) => {
    const retCrease1 = new THREE.Mesh(new THREE.PlaneGeometry(0.06, 1.2), creaseMat);
    retCrease1.rotation.x = -Math.PI / 2;
    retCrease1.position.set(rx, -14.75, 2.0);
    stadiumArenaGroup.add(retCrease1);

    const retCrease2 = new THREE.Mesh(new THREE.PlaneGeometry(0.06, 1.2), creaseMat);
    retCrease2.rotation.x = -Math.PI / 2;
    retCrease2.position.set(rx, -14.75, -5.6);
    stadiumArenaGroup.add(retCrease2);
  });

  // Authentic 3 Wooden Wickets & Cross Bails at Both Pitch Ends
  const stumpMat = new THREE.MeshStandardMaterial({ color: 0xD4A373, roughness: 0.45 });
  const bailMat = new THREE.MeshStandardMaterial({ color: 0xF3C58E, roughness: 0.35 });
  const stumpGeo = new THREE.CylinderGeometry(0.022, 0.022, 0.46, 12);
  const bailGeo = new THREE.CylinderGeometry(0.012, 0.012, 0.22, 8);
  bailGeo.rotateZ(Math.PI / 2);

  [2.0, -5.6].forEach((wz) => {
    [-0.10, 0.0, 0.10].forEach((wx) => {
      const stump = new THREE.Mesh(stumpGeo, stumpMat);
      stump.position.set(wx, -14.76 + 0.23, wz);
      stadiumArenaGroup.add(stump);
    });
    const bail = new THREE.Mesh(bailGeo, bailMat);
    bail.position.set(0, -14.76 + 0.47, wz);
    stadiumArenaGroup.add(bail);
  });

  // Player Dugouts on Boundary Flanks (East & West)
  const dugoutMat = new THREE.MeshStandardMaterial({ color: 0x070B1E, metalness: 0.75, roughness: 0.25 });
  [-14.0, 14.0].forEach((dx) => {
    const dugout = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.2, 1.5), dugoutMat);
    dugout.position.set(dx, -14.76 + 0.6, -1.8);
    dugout.rotation.y = dx > 0 ? -Math.PI / 2 : Math.PI / 2;
    stadiumArenaGroup.add(dugout);
  });

  // White Stadium Boundary Rope Ring
  const ropeGeo = new THREE.TorusGeometry(14.5, 0.07, 8, 64);
  ropeGeo.rotateX(Math.PI / 2);
  const ropeMat = new THREE.MeshStandardMaterial({
    color: 0xFFFFFF,
    roughness: 0.4
  });
  const boundaryRope = new THREE.Mesh(ropeGeo, ropeMat);
  boundaryRope.position.y = -14.72;
  stadiumArenaGroup.add(boundaryRope);

  // 36 Foam Boundary Advertising Wedges along Rope
  const wedgeGeo = new THREE.BoxGeometry(0.8, 0.22, 0.35);
  const wedgeMatRR = new THREE.MeshStandardMaterial({ color: 0xEA1A85, roughness: 0.5 });
  const wedgeMatGold = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.4 });
  for (let w = 0; w < 36; w++) {
    const wAngle = (w / 36) * Math.PI * 2;
    const wMesh = new THREE.Mesh(wedgeGeo, w % 2 === 0 ? wedgeMatRR : wedgeMatGold);
    wMesh.position.set(Math.sin(wAngle) * 14.65, -14.65, Math.cos(wAngle) * 14.65 - 0.2);
    wMesh.rotation.y = wAngle;
    stadiumArenaGroup.add(wMesh);
  }

  // 30-Yard Circle Field Restriction Marker Discs (Radius 10.5)
  const markerDiscGeo = new THREE.CircleGeometry(0.14, 16);
  markerDiscGeo.rotateX(-Math.PI / 2);
  const markerDiscMat = new THREE.MeshBasicMaterial({ color: 0xFFFFFF, side: THREE.DoubleSide });
  for (let m = 0; m < 24; m++) {
    const mAngle = (m / 24) * Math.PI * 2;
    const marker = new THREE.Mesh(markerDiscGeo, markerDiscMat);
    marker.position.set(Math.sin(mAngle) * 10.5, -14.75, Math.cos(mAngle) * 10.5 - 1.8);
    stadiumArenaGroup.add(marker);
  }

  // Authentic Slatted Cricket Sight Screens at Boundary Terminals (North & South)
  const slatGeo = new THREE.BoxGeometry(0.22, 1.45, 0.08);
  const slatMat = new THREE.MeshStandardMaterial({
    color: 0xEEF2F6,
    roughness: 0.5,
    metalness: 0.1
  });
  const screenPoleMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.85 });

  // North Sight Screen (Behind Bowler)
  const northScreenGroup = new THREE.Group();
  northScreenGroup.position.set(0, -13.95, -15.2);
  const NUM_SLATS = 14;
  for (let sl = 0; sl < NUM_SLATS; sl++) {
    const sx = -2.0 + sl * 0.31;
    const slat = new THREE.Mesh(slatGeo, slatMat);
    slat.position.set(sx, 0, 0);
    northScreenGroup.add(slat);
  }
  const northBeam1 = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.10, 0.10), screenPoleMat);
  northBeam1.position.set(0, 0.42, -0.06);
  northScreenGroup.add(northBeam1);
  const northBeam2 = northBeam1.clone();
  northBeam2.position.y = -0.42;
  northScreenGroup.add(northBeam2);

  [-1.8, 1.8].forEach((px) => {
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.2, 8), screenPoleMat);
    pole.position.set(px, -0.7, 0);
    northScreenGroup.add(pole);
  });
  stadiumArenaGroup.add(northScreenGroup);

  // South Sight Screen (Behind Batter)
  const southScreenGroup = new THREE.Group();
  southScreenGroup.position.set(0, -13.95, 15.2);
  for (let sl = 0; sl < NUM_SLATS; sl++) {
    const sx = -2.0 + sl * 0.31;
    const slat = new THREE.Mesh(slatGeo, slatMat);
    slat.position.set(sx, 0, 0);
    southScreenGroup.add(slat);
  }
  const southBeam1 = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.10, 0.10), screenPoleMat);
  southBeam1.position.set(0, 0.42, -0.06);
  southScreenGroup.add(southBeam1);
  const southBeam2 = southBeam1.clone();
  southBeam2.position.y = -0.42;
  southScreenGroup.add(southBeam2);

  [-1.8, 1.8].forEach((px) => {
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.2, 8), screenPoleMat);
    pole.position.set(px, -0.7, 0);
    southScreenGroup.add(pole);
  });
  stadiumArenaGroup.add(southScreenGroup);

  // Ground Heavy Pitch Roller parked on outfield boundary flank
  const rollerGroup = new THREE.Group();
  rollerGroup.position.set(-13.0, -14.3, -8.2);
  const drumGeo = new THREE.CylinderGeometry(0.48, 0.48, 1.4, 16);
  drumGeo.rotateZ(Math.PI / 2);
  const drumMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.85, roughness: 0.35 });
  rollerGroup.add(new THREE.Mesh(drumGeo, drumMat));
  const rollerFrame = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.7, 0.9), new THREE.MeshStandardMaterial({ color: 0x0284C7 }));
  rollerFrame.position.set(0, 0.4, 0.4);
  rollerGroup.add(rollerFrame);
  stadiumArenaGroup.add(rollerGroup);

  // ============================================================
  // ARCHITECTURAL STADIUM GRANDSTANDS & VIP CORPORATE SUITES
  // ============================================================

  // Procedural Window Grid Canvas Texture for VIP Suites
  const winCanvas = document.createElement('canvas');
  winCanvas.width = 512;
  winCanvas.height = 256;
  const wCtx = winCanvas.getContext('2d');
  wCtx.fillStyle = '#050918';
  wCtx.fillRect(0, 0, 512, 256);

  const numFloors = 16;
  const numBays = 32;
  const floorH = 256 / numFloors;
  const bayW = 512 / numBays;
  for (let f = 0; f < numFloors; f++) {
    wCtx.fillStyle = '#091126';
    wCtx.fillRect(0, f * floorH, 512, 2);
    for (let b = 0; b < numBays; b++) {
      const rand = Math.random();
      if (rand < 0.38) {
        if (rand < 0.20) {
          wCtx.fillStyle = '#FBBF24'; // Warm amber
        } else if (rand < 0.30) {
          wCtx.fillStyle = '#FEF08A'; // Soft gold
        } else {
          wCtx.fillStyle = '#38BDF8'; // Cool cyan
        }
        wCtx.fillRect(b * bayW + 3, f * floorH + 3, bayW - 6, floorH - 5);
      }
    }
  }
  const winTex = new THREE.CanvasTexture(winCanvas);
  winTex.wrapS = THREE.RepeatWrapping;
  winTex.wrapT = THREE.RepeatWrapping;
  winTex.repeat.set(6, 1);

  // Realistic Spectator Seating Texture (Deep Navy, Royal Blue, and Subtle Muted Accents)
  const crowdCanvas = document.createElement('canvas');
  crowdCanvas.width = 1024;
  crowdCanvas.height = 512;
  const cCtx = crowdCanvas.getContext('2d');

  // Concrete Terraced Steps Background
  cCtx.fillStyle = '#080E22';
  cCtx.fillRect(0, 0, 1024, 512);

  const seatRows = 24;
  const seatCols = 64;
  const rowH = 512 / seatRows;
  const colW = 1024 / seatCols;

  for (let r = 0; r < seatRows; r++) {
    // Concrete tread shadow line
    cCtx.fillStyle = '#050917';
    cCtx.fillRect(0, r * rowH, 1024, 3);

    // Concrete tread highlight line
    cCtx.fillStyle = '#111C3D';
    cCtx.fillRect(0, r * rowH + 3, 1024, 2);

    for (let c = 0; c < seatCols; c++) {
      // Aisle staircase gap every 16 seats
      if (c % 16 === 0 || c % 16 === 1) {
        cCtx.fillStyle = '#0E1736';
        cCtx.fillRect(c * colW, r * rowH + 4, colW, rowH - 4);
        continue;
      }

      // Authentic Stadium Seating Palette (No thin neon rings)
      const rand = Math.random();
      if (rand < 0.55) {
        cCtx.fillStyle = '#0F2347'; // Deep Royal Navy Seat
      } else if (rand < 0.82) {
        cCtx.fillStyle = '#1D3B73'; // Medium Royal Blue Seat
      } else if (rand < 0.94) {
        cCtx.fillStyle = '#0A1329'; // Shaded Dark Seat
      } else {
        cCtx.fillStyle = '#991B5B'; // Muted Franchise Wine Accent Seat
      }
      cCtx.fillRect(c * colW + 2, r * rowH + 5, colW - 4, rowH - 6);
    }
  }

  const crowdTex = new THREE.CanvasTexture(crowdCanvas);
  crowdTex.wrapS = THREE.RepeatWrapping;
  crowdTex.wrapT = THREE.RepeatWrapping;
  crowdTex.repeat.set(6, 1);

  // Tier 1: Lower Seating Bowl Structure (R = 14.8 to 19.5, Y = -14.76 to -12.0)
  const lowerBowlGeo = new THREE.CylinderGeometry(19.5, 14.8, 2.76, 64, 1, true);
  const lowerBowlMat = new THREE.MeshStandardMaterial({
    color: 0x0A1128,
    map: crowdTex,
    roughness: 0.78,
    metalness: 0.22
  });
  const lowerBowl = new THREE.Mesh(lowerBowlGeo, lowerBowlMat);
  lowerBowl.position.y = -13.38;
  stadiumArenaGroup.add(lowerBowl);

  // Tier 1 LED Fascia Ribbon Board along Lower Grandstand
  const ribbonCanvas = document.createElement('canvas');
  ribbonCanvas.width = 1024;
  ribbonCanvas.height = 64;
  const rCtx = ribbonCanvas.getContext('2d');
  rCtx.fillStyle = '#070B1E';
  rCtx.fillRect(0, 0, 1024, 64);
  rCtx.fillStyle = '#EA1A85';
  rCtx.font = 'bold 26px "Barlow Condensed", sans-serif';
  rCtx.textAlign = 'center';
  rCtx.fillText('★ RAJASTHAN ROYALS ★ HALLA BOL ★ IPL 2027 AUCTION ★ TOP 10 PILLARS OF RELIABILITY ★', 512, 42);

  const ribbonTex = new THREE.CanvasTexture(ribbonCanvas);
  ribbonTex.wrapS = THREE.RepeatWrapping;
  ribbonTex.repeat.set(-3, 1);
  ribbonTex.offset.set(1, 0);

  const ribbonGeo = new THREE.CylinderGeometry(14.85, 14.85, 0.42, 64, 1, true);
  const ribbonMat = new THREE.MeshBasicMaterial({
    map: ribbonTex,
    side: THREE.DoubleSide
  });
  const ribbonMesh = new THREE.Mesh(ribbonGeo, ribbonMat);
  ribbonMesh.position.y = -12.18;
  stadiumArenaGroup.add(ribbonMesh);

  // Tier 2: VIP Hospitality Suites (Corporate Boxes with Glowing Windows)
  const suiteBowlGeo = new THREE.CylinderGeometry(22.5, 19.5, 2.2, 64, 1, true);
  const suiteBowlMat = new THREE.MeshStandardMaterial({
    color: 0x070B1E,
    metalness: 0.85,
    roughness: 0.22,
    emissive: 0xF59E0B,
    emissiveIntensity: 0.45,
    map: winTex,
    emissiveMap: winTex
  });
  const suiteBowl = new THREE.Mesh(suiteBowlGeo, suiteBowlMat);
  suiteBowl.position.y = -10.9;
  stadiumArenaGroup.add(suiteBowl);

  // Tier 3: Upper Grandstand Terraces (R = 22.5 to 27.5, Y = -9.8 to -5.0)
  const upperBowlGeo = new THREE.CylinderGeometry(27.5, 22.5, 4.8, 64, 1, true);
  const upperBowlMat = new THREE.MeshStandardMaterial({
    color: 0x080E24,
    map: crowdTex,
    roughness: 0.82,
    metalness: 0.18
  });
  const upperBowl = new THREE.Mesh(upperBowlGeo, upperBowlMat);
  upperBowl.position.y = -7.4;
  stadiumArenaGroup.add(upperBowl);

  // Tier 2 LED Upper Fascia Ribbon Board
  const ribbon2Canvas = document.createElement('canvas');
  ribbon2Canvas.width = 1024;
  ribbon2Canvas.height = 64;
  const r2Ctx = ribbon2Canvas.getContext('2d');
  r2Ctx.fillStyle = '#070B1E';
  r2Ctx.fillRect(0, 0, 1024, 64);
  r2Ctx.fillStyle = '#D4AF37';
  r2Ctx.font = 'bold 24px "Barlow Condensed", sans-serif';
  r2Ctx.textAlign = 'center';
  r2Ctx.fillText('★ SUPER-RR SELECTOR ★ MATCH-WINNING CLUTCH IMPACT ★ STATISTICAL 99TH PERCENTILE ★', 512, 42);

  const ribbon2Tex = new THREE.CanvasTexture(ribbon2Canvas);
  ribbon2Tex.wrapS = THREE.RepeatWrapping;
  ribbon2Tex.repeat.set(-3, 1);
  ribbon2Tex.offset.set(1, 0);

  const ribbon2Geo = new THREE.CylinderGeometry(22.55, 22.55, 0.42, 64, 1, true);
  const ribbon2Mat = new THREE.MeshBasicMaterial({ map: ribbon2Tex, side: THREE.DoubleSide });
  const ribbon2Mesh = new THREE.Mesh(ribbon2Geo, ribbon2Mat);
  ribbon2Mesh.position.y = -9.75;
  stadiumArenaGroup.add(ribbon2Mesh);

  // Cantilevered Modern Stadium Roof Structure
  const roofGeo = new THREE.CylinderGeometry(28.2, 24.5, 1.2, 64, 1, true);
  const roofMat = new THREE.MeshStandardMaterial({
    color: 0xE2E8F0,
    metalness: 0.55,
    roughness: 0.25,
    side: THREE.DoubleSide
  });
  const roofMesh = new THREE.Mesh(roofGeo, roofMat);
  roofMesh.position.y = -4.8;
  stadiumArenaGroup.add(roofMesh);

  // 16 Cantilever Structural Steel Trusses
  const trussMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.85, roughness: 0.3 });
  for (let t = 0; t < 16; t++) {
    const tAngle = (t / 16) * Math.PI * 2;
    const truss = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.4, 4.0), trussMat);
    truss.position.set(Math.sin(tAngle) * 26.5, -4.6, Math.cos(tAngle) * 26.5 - 0.2);
    truss.rotation.y = tAngle;
    stadiumArenaGroup.add(truss);
  }

  // ============================================================
  // TWO GIANT HIGH-RESOLUTION ELECTRONIC LED JUMBOTRONS (SCOREBOARDS)
  // ============================================================
  // North Stand Jumbotron (Pavilion End - Live Scoreboard)
  const jumbotronCanvas1 = document.createElement('canvas');
  jumbotronCanvas1.width = 1024;
  jumbotronCanvas1.height = 512;
  const j1Ctx = jumbotronCanvas1.getContext('2d');

  j1Ctx.fillStyle = '#030712';
  j1Ctx.fillRect(0, 0, 1024, 512);

  j1Ctx.fillStyle = '#070E22';
  j1Ctx.fillRect(16, 16, 992, 480);
  j1Ctx.strokeStyle = '#D4AF37';
  j1Ctx.lineWidth = 4;
  j1Ctx.strokeRect(16, 16, 992, 480);

  j1Ctx.fillStyle = '#D4AF37';
  j1Ctx.fillRect(16, 16, 992, 54);
  j1Ctx.fillStyle = '#070B1E';
  j1Ctx.font = 'bold 30px "Barlow Condensed", sans-serif';
  j1Ctx.textAlign = 'center';
  j1Ctx.fillText('★ RAJASTHAN ROYALS · SAWAI MANSINGH STADIUM JAIPUR ★', 512, 54);

  j1Ctx.fillStyle = '#FFFFFF';
  j1Ctx.font = 'bold 76px "Barlow Condensed", sans-serif';
  j1Ctx.fillText('RR 208/3  (19.0)', 512, 160);

  j1Ctx.fillStyle = '#38BDF8';
  j1Ctx.font = 'bold 34px "Barlow Condensed", sans-serif';
  j1Ctx.fillText('TARGET: 216  ·  NEED 8 RUNS IN 6 BALLS', 512, 215);

  j1Ctx.fillStyle = 'rgba(234, 26, 133, 0.2)';
  j1Ctx.strokeStyle = '#EA1A85';
  j1Ctx.lineWidth = 3;
  j1Ctx.strokeRect(60, 255, 904, 110);
  j1Ctx.fillRect(60, 255, 904, 110);

  j1Ctx.fillStyle = '#FFD700';
  j1Ctx.font = 'bold 28px "JetBrains Mono", monospace';
  j1Ctx.fillText('MATCH-DEFINING CLUTCH MOMENT  ·  PRESSURE: 0.94 / 1.00', 512, 298);

  j1Ctx.fillStyle = '#FFFFFF';
  j1Ctx.font = 'bold 36px "Barlow Condensed", sans-serif';
  j1Ctx.fillText('CRUCIBLE OVER 20  ·  WIN PROBABILITY: 94.2%  ·  हल्ला बोल', 512, 342);

  j1Ctx.fillStyle = '#EA1A85';
  j1Ctx.fillRect(16, 442, 992, 54);
  j1Ctx.fillStyle = '#FFFFFF';
  j1Ctx.font = 'bold 26px "Barlow Condensed", sans-serif';
  j1Ctx.fillText('★ SUPER-RR SELECTOR  ★  TOP 10 PILLARS OF RELIABILITY  ★  IPL 2027 AUCTION  ★', 512, 478);

  const jumbotronTex1 = new THREE.CanvasTexture(jumbotronCanvas1);
  const jumbotronMat1 = new THREE.MeshStandardMaterial({
    map: jumbotronTex1,
    emissiveMap: jumbotronTex1,
    emissive: 0xFFFFFF,
    emissiveIntensity: 0.95,
    roughness: 0.2,
    metalness: 0.6
  });

  const jumbotronGeo = new THREE.PlaneGeometry(9.6, 4.8);
  const jumbotronMesh1 = new THREE.Mesh(jumbotronGeo, jumbotronMat1);
  jumbotronMesh1.position.set(0, -5.2, -26.0);
  jumbotronMesh1.rotation.x = 0.16;
  stadiumArenaGroup.add(jumbotronMesh1);

  const gantryMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, metalness: 0.85, roughness: 0.3 });
  const gantryMesh1 = new THREE.Mesh(new THREE.BoxGeometry(10.2, 5.4, 0.4), gantryMat);
  gantryMesh1.position.set(0, -5.2, -26.25);
  gantryMesh1.rotation.x = 0.16;
  stadiumArenaGroup.add(gantryMesh1);

  // South Stand Jumbotron (City End - Player Intelligence)
  const jumbotronCanvas2 = document.createElement('canvas');
  jumbotronCanvas2.width = 1024;
  jumbotronCanvas2.height = 512;
  const j2Ctx = jumbotronCanvas2.getContext('2d');

  j2Ctx.fillStyle = '#030712';
  j2Ctx.fillRect(0, 0, 1024, 512);

  j2Ctx.fillStyle = '#070E22';
  j2Ctx.fillRect(16, 16, 992, 480);
  j2Ctx.strokeStyle = '#38BDF8';
  j2Ctx.lineWidth = 4;
  j2Ctx.strokeRect(16, 16, 992, 480);

  j2Ctx.fillStyle = '#38BDF8';
  j2Ctx.fillRect(16, 16, 992, 54);
  j2Ctx.fillStyle = '#070B1E';
  j2Ctx.font = 'bold 30px "Barlow Condensed", sans-serif';
  j2Ctx.textAlign = 'center';
  j2Ctx.fillText('★ SUPER-RR SELECTOR · 2027 WAR ROOM RADAR INTEL ★', 512, 54);

  j2Ctx.fillStyle = '#FFD700';
  j2Ctx.font = 'bold 54px "Barlow Condensed", sans-serif';
  j2Ctx.fillText('BAYESIAN WIN PROBABILITY: 94.2%', 512, 160);

  j2Ctx.fillStyle = '#FFFFFF';
  j2Ctx.font = 'bold 32px "Barlow Condensed", sans-serif';
  j2Ctx.fillText('PRESSURE-INDEX EVALUATED ON 199,208 T20 DELIVERIES', 512, 215);

  j2Ctx.fillStyle = 'rgba(56, 189, 248, 0.15)';
  j2Ctx.strokeStyle = '#38BDF8';
  j2Ctx.lineWidth = 3;
  j2Ctx.strokeRect(60, 255, 904, 110);
  j2Ctx.fillRect(60, 255, 904, 110);

  j2Ctx.fillStyle = '#EA1A85';
  j2Ctx.font = 'bold 28px "JetBrains Mono", monospace';
  j2Ctx.fillText('STRATIFIED LEVERAGE BANDS · 99th PERCENTILE IMPACT', 512, 298);

  j2Ctx.fillStyle = '#FFFFFF';
  j2Ctx.font = 'bold 34px "Barlow Condensed", sans-serif';
  j2Ctx.fillText('VERIFIED AUCTION TARGETS IDENTIFIED FOR GOA 2027', 512, 342);

  j2Ctx.fillStyle = '#38BDF8';
  j2Ctx.fillRect(16, 442, 992, 54);
  j2Ctx.fillStyle = '#070B1E';
  j2Ctx.font = 'bold 26px "Barlow Condensed", sans-serif';
  j2Ctx.fillText('★ RAJASTHAN ROYALS  ★  HALLA BOL  ★  GOA MINI-AUCTION  ★', 512, 478);

  const jumbotronTex2 = new THREE.CanvasTexture(jumbotronCanvas2);
  const jumbotronMat2 = new THREE.MeshStandardMaterial({
    map: jumbotronTex2,
    emissiveMap: jumbotronTex2,
    emissive: 0xFFFFFF,
    emissiveIntensity: 0.95,
    roughness: 0.2,
    metalness: 0.6
  });

  const jumbotronMesh2 = new THREE.Mesh(jumbotronGeo, jumbotronMat2);
  jumbotronMesh2.position.set(0, -5.2, 26.0);
  jumbotronMesh2.rotation.y = Math.PI;
  jumbotronMesh2.rotation.x = 0.16;
  stadiumArenaGroup.add(jumbotronMesh2);

  const gantryMesh2 = new THREE.Mesh(new THREE.BoxGeometry(10.2, 5.4, 0.4), gantryMat);
  gantryMesh2.position.set(0, -5.2, 26.25);
  gantryMesh2.rotation.y = Math.PI;
  gantryMesh2.rotation.x = 0.16;
  stadiumArenaGroup.add(gantryMesh2);

  // ============================================================
  // REALISTIC JAIPUR NIGHT CITY SKYLINE (DISTINCT TOWERS & OPEN SKY)
  // ============================================================
  const cityGroup = new THREE.Group();
  stadiumArenaGroup.add(cityGroup);

  const beaconGroup = new THREE.Group();
  stadiumArenaGroup.add(beaconGroup);

  // 32 Distinctive Individual City Towers (Proper spacing, open night sky between them)
  const NUM_BLDGS = 32;
  for (let i = 0; i < NUM_BLDGS; i++) {
    const angle = (i / NUM_BLDGS) * Math.PI * 2;
    const rad = 36.0 + (i % 4) * 3.5;
    const bx = Math.sin(angle) * rad;
    const bz = Math.cos(angle) * rad - 1.0;

    const bHeight = 14.0 + (i % 6) * 3.8 + ((i * 7) % 5) * 2.2;
    const bWidth = 3.2 + (i % 3) * 0.9;
    const bDepth = 2.8 + ((i + 1) % 3) * 0.8;

    // Individual building canvas texture for crisp non-stretched windows
    const bCanvas = document.createElement('canvas');
    bCanvas.width = 128;
    bCanvas.height = 256;
    const bCtx = bCanvas.getContext('2d');
    bCtx.fillStyle = '#060B1E';
    bCtx.fillRect(0, 0, 128, 256);

    const bFloors = Math.max(8, Math.round(bHeight));
    const bBays = Math.max(4, Math.round(bWidth * 1.5));
    const bfH = 256 / bFloors;
    const bbW = 128 / bBays;

    for (let f = 0; f < bFloors; f++) {
      bCtx.fillStyle = '#091126';
      bCtx.fillRect(0, f * bfH, 128, 2);
      for (let b = 0; b < bBays; b++) {
        const rand = Math.random();
        if (rand < 0.35) {
          if (rand < 0.18) {
            bCtx.fillStyle = '#FBBF24'; // Warm amber
          } else if (rand < 0.28) {
            bCtx.fillStyle = '#FEF08A'; // Soft gold
          } else {
            bCtx.fillStyle = '#38BDF8'; // Cool cyan
          }
          bCtx.fillRect(b * bbW + 2, f * bfH + 2, bbW - 4, bfH - 4);
        }
      }
    }
    const bTex = new THREE.CanvasTexture(bCanvas);

    const bldgMat = new THREE.MeshStandardMaterial({
      color: 0x090F26,
      metalness: 0.85,
      roughness: 0.25,
      map: bTex,
      emissive: 0xFFFFFF,
      emissiveMap: bTex,
      emissiveIntensity: 0.55
    });

    const bGeo = new THREE.BoxGeometry(bWidth, bHeight, bDepth);
    const bMesh = new THREE.Mesh(bGeo, bldgMat);
    bMesh.position.set(bx, -14.76 + bHeight / 2, bz);
    bMesh.rotation.y = angle + Math.PI / 4;
    cityGroup.add(bMesh);

    // Iconic Rajasthani Spires & Heritage Chhatri Domes on selected towers
    if (i % 3 === 0) {
      const spireH = 2.8 + (i % 3) * 0.9;
      const domeGeo = new THREE.ConeGeometry(bWidth * 0.42, spireH, 8);
      const domeMat = new THREE.MeshStandardMaterial({
        color: 0xD4AF37,
        metalness: 0.88,
        roughness: 0.2,
        emissive: 0x946E18,
        emissiveIntensity: 0.35
      });
      const domeMesh = new THREE.Mesh(domeGeo, domeMat);
      domeMesh.position.set(bx, -14.76 + bHeight + spireH / 2, bz);
      cityGroup.add(domeMesh);

      // Red / Amber Aviation Warning Beacon
      const beaconGeo = new THREE.SphereGeometry(0.14, 8, 8);
      const beaconMat = new THREE.MeshBasicMaterial({
        color: i % 2 === 0 ? 0xEF4444 : 0xF59E0B
      });
      const beaconMesh = new THREE.Mesh(beaconGeo, beaconMat);
      beaconMesh.position.set(bx, -14.76 + bHeight + spireH + 0.14, bz);
      beaconGroup.add(beaconMesh);
    }
  }

  // Arterial Highway Light Ribbons around Stadium Perimeter
  const highwayGeo = new THREE.TorusGeometry(32.5, 0.22, 6, 64);
  highwayGeo.rotateX(Math.PI / 2);
  const highwayMat = new THREE.MeshBasicMaterial({
    color: 0xF59E0B,
    transparent: true,
    opacity: 0.55
  });
  const highway = new THREE.Mesh(highwayGeo, highwayMat);
  highway.position.y = -14.65;
  cityGroup.add(highway);

  // ============================================================
  // FOUR HIGH-MAST STEEL LATTICE FLOODLIGHT TOWERS WITH BEAMS
  // ============================================================
  const mastPositions = [
    [-15.0, -13.5],
    [15.0, -13.5],
    [-15.5, 11.5],
    [15.5, 11.5]
  ];

  const steelMat = new THREE.MeshStandardMaterial({
    color: 0x64748B,
    metalness: 0.90,
    roughness: 0.22
  });

  const lightBankGeo = new THREE.BoxGeometry(3.2, 1.6, 0.45);
  const lightBankMat = new THREE.MeshStandardMaterial({
    color: 0x0F172A,
    metalness: 0.92,
    roughness: 0.18
  });

  // Soft Volumetric Light Beam Cone
  const coneGeo = new THREE.ConeGeometry(6.5, 18.0, 16, 1, true);
  coneGeo.translate(0, -9.0, 0);
  coneGeo.rotateX(Math.PI / 2);
  const coneMat = new THREE.MeshBasicMaterial({
    color: 0xFFFBEB,
    transparent: true,
    opacity: 0.075,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
    depthWrite: false
  });

  mastPositions.forEach(([mx, mz]) => {
    const tower = new THREE.Group();
    tower.position.set(mx, -14.76, mz);

    // 4 Corner Tapered Lattice Columns
    const legGeo = new THREE.CylinderGeometry(0.045, 0.09, 19.5, 8);
    legGeo.translate(0, 9.75, 0);
    const legSpreadBottom = 0.85;
    const legSpreadTop = 0.42;

    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([lx, lz]) => {
      const leg = new THREE.Mesh(legGeo, steelMat);
      leg.position.set(lx * (legSpreadBottom + legSpreadTop) * 0.5, 0, lz * (legSpreadBottom + legSpreadTop) * 0.5);
      tower.add(leg);
    });

    // Cross-Brace Horizontal & Diagonal Girders (5 vertical stages)
    for (let st = 1; st <= 5; st++) {
      const gY = st * 3.6;
      const gSpread = legSpreadBottom - (st / 5) * (legSpreadBottom - legSpreadTop);
      const ringGeo = new THREE.BoxGeometry(gSpread * 2.1, 0.08, gSpread * 2.1);
      const ring = new THREE.Mesh(ringGeo, steelMat);
      ring.position.y = gY;
      tower.add(ring);
    }

    // Floodlight bank tilted toward center pitch
    const bankMesh = new THREE.Mesh(lightBankGeo, lightBankMat);
    bankMesh.position.set(0, 19.8, 0);
    bankMesh.lookAt(new THREE.Vector3(-mx * 0.35, -13.0, -mz * 0.35 - 1.8));

    // 36 Bright LED Floodlight Fixtures on headframe (4 rows of 9)
    const bulbMat = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
    const bulbGeo = new THREE.PlaneGeometry(0.24, 0.24);
    for (let row = 0; row < 4; row++) {
      for (let col = 0; col < 9; col++) {
        const bulb = new THREE.Mesh(bulbGeo, bulbMat);
        bulb.position.set(-1.2 + col * 0.30, -0.55 + row * 0.36, 0.24);
        bankMesh.add(bulb);
      }
    }
    tower.add(bankMesh);

    // Pinnacle Red Aviation Warning Beacon
    const mastBeacon = new THREE.Mesh(
      new THREE.SphereGeometry(0.12, 8, 8),
      new THREE.MeshBasicMaterial({ color: 0xEF4444 })
    );
    mastBeacon.position.set(0, 20.8, 0);
    tower.add(mastBeacon);
    beaconGroup.add(mastBeacon);

    // Volumetric Light Cone
    const coneMesh = new THREE.Mesh(coneGeo, coneMat);
    coneMesh.position.set(0, 19.8, 0);
    coneMesh.lookAt(new THREE.Vector3(-mx * 0.45, -14.76, -mz * 0.45 - 1.8));
    tower.add(coneMesh);

    // Stadium floodlight spotlight beam
    const spot = new THREE.SpotLight(0xFFF8E7, 4.2, 35, Math.PI / 4, 0.45, 1.2);
    spot.position.set(0, 19.8, 0);
    spot.target.position.set(-mx * 0.4, -14.76, -mz * 0.4 - 1.8);
    tower.add(spot);
    tower.add(spot.target);

    stadiumArenaGroup.add(tower);
  });

  // 6. Realistic SG Test Cricket Ball (Hero Area)
  const ballGroup = new THREE.Group();
  const ballCoreGeo = new THREE.SphereGeometry(0.85, 36, 36);
  const ballCoreMat = new THREE.MeshStandardMaterial({
    color: 0x8A0D1B,
    roughness: 0.28,
    metalness: 0.14,
    emissive: 0x1A0004
  });
  const ballCore = new THREE.Mesh(ballCoreGeo, ballCoreMat);
  ballGroup.add(ballCore);

  const seamGeo = new THREE.TorusGeometry(0.854, 0.026, 12, 64);
  const seamMat = new THREE.MeshStandardMaterial({
    color: 0xF4F4F4,
    roughness: 0.55,
    metalness: 0.05
  });
  const seam = new THREE.Mesh(seamGeo, seamMat);
  seam.rotation.x = Math.PI / 3.2;
  seam.rotation.y = Math.PI / 4.5;
  ballGroup.add(seam);

  ballGroup.position.set(2.4, 11.8, 21.2);
  scene.add(ballGroup);

  // 7. General Lighting
  const dirLight = new THREE.DirectionalLight(0xFFEEDB, 1.4);
  dirLight.position.set(12, 18, 15);
  scene.add(dirLight);

  const ambLight = new THREE.AmbientLight(0x1B244A, 0.95);
  scene.add(ambLight);

  const pointLight = new THREE.PointLight(0x0C1433, 4.0, 35);
  pointLight.position.set(0, 1.5, 0);
  scene.add(pointLight);

  // Warm Golden Chamber Spotlights Illuminating the 10 Pillars
  const chamberSpot1 = new THREE.PointLight(0xFFD700, 4.5, 24);
  chamberSpot1.position.set(0, -9.2, 2.5);
  scene.add(chamberSpot1);

  const chamberSpot2 = new THREE.PointLight(0xFFE082, 3.0, 20);
  chamberSpot2.position.set(0, -13.0, -1.0);
  scene.add(chamberSpot2);

  // ============================================================
  // PHASE 4: REDESIGNED LUXURY PILLARS OF RELIABILITY
  // ============================================================
  const chamberGroup = new THREE.Group();
  chamberGroup.visible = false;
  scene.add(chamberGroup);

  const pillars = [];
  const pillarMeshes = [];
  const NUM_PILLARS = 10;
  const ARC_RADIUS = 5.2;
  const START_ANGLE = -Math.PI * 0.33; // -59.4 deg (Wide uncropped colosseum arc)
  const END_ANGLE = Math.PI * 0.33;    // +59.4 deg

  // High-End Architectural Geometries:
  // Base: Double-beveled octagonal obsidian pedestal with gold chamfer
  const baseOuterGeo = new THREE.CylinderGeometry(0.52, 0.62, 0.16, 8);
  baseOuterGeo.translate(0, 0.08, 0);

  const baseGoldRingGeo = new THREE.CylinderGeometry(0.46, 0.50, 0.06, 8);
  baseGoldRingGeo.translate(0, 0.18, 0);

  // Shaft: Faceted Octagonal Column in Dark Titanium Carbon
  const colGeo = new THREE.CylinderGeometry(0.28, 0.36, 1.0, 8);
  colGeo.translate(0, 0.5, 0);

  // Vertical Illuminated Energy Conduits (4 Vertical Strips)
  const conduitGeo = new THREE.BoxGeometry(0.06, 0.98, 0.04);
  conduitGeo.translate(0, 0.5, 0);

  // Capital: Sculpted Gold Crown Collar
  const capGeo = new THREE.CylinderGeometry(0.46, 0.32, 0.12, 8);
  capGeo.translate(0, 0.06, 0);

  // Precision Horizontal Dual-Ring Orbital Halo
  const haloGeo = new THREE.TorusGeometry(0.66, 0.022, 10, 48);
  haloGeo.rotateX(Math.PI / 2);

  const innerHaloGeo = new THREE.TorusGeometry(0.54, 0.012, 8, 36);
  innerHaloGeo.rotateX(Math.PI / 2);

  // Ground Turf LED Emitter Glow Ring
  const rippleGeo = new THREE.RingGeometry(0.52, 0.84, 32);
  rippleGeo.rotateX(-Math.PI / 2);

  for (let i = 0; i < NUM_PILLARS; i++) {
    const t = i / (NUM_PILLARS - 1);
    const angle = START_ANGLE + t * (END_ANGLE - START_ANGLE);
    const px = Math.sin(angle) * ARC_RADIUS;
    const pz = -Math.cos(angle) * ARC_RADIUS - 0.2;

    const pGroup = new THREE.Group();
    pGroup.position.set(px, -14.76, pz);

    // 1. Base Pedestal: Polished Obsidian with Gold Chamfer
    const baseMat = new THREE.MeshStandardMaterial({
      color: 0x070B1E,
      roughness: 0.18,
      metalness: 0.92
    });
    const baseMesh = new THREE.Mesh(baseOuterGeo, baseMat);
    pGroup.add(baseMesh);

    const baseGoldMat = new THREE.MeshStandardMaterial({
      color: 0xD4AF37,
      roughness: 0.25,
      metalness: 0.88
    });
    const baseGoldMesh = new THREE.Mesh(baseGoldRingGeo, baseGoldMat);
    pGroup.add(baseGoldMesh);

    // 2. Shaft: Faceted Titanium Carbon Column
    const shaftMat = new THREE.MeshStandardMaterial({
      color: 0x0A1128,
      roughness: 0.22,
      metalness: 0.88,
      transparent: true,
      opacity: 0.98
    });
    const colMesh = new THREE.Mesh(colGeo, shaftMat);
    colMesh.userData = { pillarIndex: i };
    pGroup.add(colMesh);
    pillarMeshes.push(colMesh);

    // 3. Four Inset Vertical Glowing Energy Conduits
    const conduitMat = new THREE.MeshStandardMaterial({
      color: 0xEA1A85,
      emissive: 0xEA1A85,
      emissiveIntensity: 0.85,
      roughness: 0.2,
      metalness: 0.4
    });
    const conduitGroup = new THREE.Group();
    [0, Math.PI / 2, Math.PI, (3 * Math.PI) / 2].forEach((cAngle) => {
      const cMesh = new THREE.Mesh(conduitGeo, conduitMat);
      cMesh.rotation.y = cAngle;
      cMesh.position.set(Math.sin(cAngle) * 0.32, 0, Math.cos(cAngle) * 0.32);
      conduitGroup.add(cMesh);
    });
    colMesh.add(conduitGroup);

    // 4. Capital Plinth Collar (Gold Crown)
    const capMat = new THREE.MeshStandardMaterial({
      color: 0xD4AF37,
      roughness: 0.25,
      metalness: 0.88,
      emissive: 0xD4AF37,
      emissiveIntensity: 0.45
    });
    const capMesh = new THREE.Mesh(capGeo, capMat);
    pGroup.add(capMesh);

    // 5. Precision Dual-Ring Orbital Halo
    const haloMat = new THREE.MeshStandardMaterial({
      color: 0xFFD700,
      roughness: 0.15,
      metalness: 0.85,
      transparent: true,
      opacity: 0.85,
      emissive: 0xD4AF37,
      emissiveIntensity: 0.9
    });
    const haloGroup = new THREE.Group();
    const haloMesh = new THREE.Mesh(haloGeo, haloMat);
    haloGroup.add(haloMesh);
    const innerHaloMesh = new THREE.Mesh(innerHaloGeo, haloMat);
    haloGroup.add(innerHaloMesh);
    pGroup.add(haloGroup);

    // 6. Ground Turf LED Glow Ring
    const rippleMat = new THREE.MeshBasicMaterial({
      color: 0xFFD700,
      transparent: true,
      opacity: 0.42,
      side: THREE.DoubleSide
    });
    const rippleMesh = new THREE.Mesh(rippleGeo, rippleMat);
    rippleMesh.position.y = 0.02;
    pGroup.add(rippleMesh);

    // 7. Ultra-High-Resolution Holographic Avatar Billboard (1024x1024 Retina Texture, Scale 1.48)
    const spriteCanvas = document.createElement('canvas');
    spriteCanvas.width = 1024;
    spriteCanvas.height = 1024;
    const spriteTex = new THREE.CanvasTexture(spriteCanvas);
    spriteTex.minFilter = THREE.LinearFilter;
    spriteTex.magFilter = THREE.LinearFilter;

    const spriteMat = new THREE.SpriteMaterial({
      map: spriteTex,
      transparent: true,
      depthTest: true,
      depthWrite: false
    });
    const avatarSprite = new THREE.Sprite(spriteMat);
    avatarSprite.scale.set(1.48, 1.48, 1.0);
    pGroup.add(avatarSprite);

    pGroup.userData = {
      index: i,
      baseMesh,
      baseGoldMesh,
      colMesh,
      shaftMat,
      conduitMat,
      conduitGroup,
      capMesh,
      haloMesh: haloGroup,
      rippleMesh,
      avatarSprite,
      spriteCanvas,
      spriteTex,
      baseY: -14.76,
      targetH: 2.2,
      isHovered: false,
      isLocked: false,
      player: null
    };

    chamberGroup.add(pGroup);
    pillars.push(pGroup);
  }

  // Draw Crystal-Clear Holographic Player Card on 1024x1024 Texture
  function updateAvatarTexture(pGroup, player, isBowlers) {
    const canvas = pGroup.userData.spriteCanvas;
    const ctx = canvas.getContext('2d');
    const tex = pGroup.userData.spriteTex;
    const isLocked = !player.is_available;

    const drawCard = (img) => {
      ctx.clearRect(0, 0, 1024, 1024);

      // A. Radiant Glow Backdrop
      const glowGrad = ctx.createRadialGradient(512, 450, 160, 512, 450, 440);
      const themeGlow = isLocked
        ? 'rgba(100, 116, 139, 0.45)'
        : (isBowlers ? 'rgba(56, 189, 248, 0.65)' : 'rgba(234, 26, 131, 0.70)');
      glowGrad.addColorStop(0, themeGlow);
      glowGrad.addColorStop(1, 'rgba(7, 11, 30, 0)');
      ctx.fillStyle = glowGrad;
      ctx.beginPath();
      ctx.arc(512, 450, 440, 0, Math.PI * 2);
      ctx.fill();

      // B. Large Circular Portrait (Radius 280 = 560px wide)
      ctx.save();
      ctx.beginPath();
      ctx.arc(512, 450, 280, 0, Math.PI * 2);
      ctx.closePath();
      ctx.clip();

      if (img && img.complete && img.naturalWidth > 0) {
        const minDim = Math.min(img.naturalWidth, img.naturalHeight);
        const sx = (img.naturalWidth - minDim) / 2;
        const sy = (img.naturalHeight - minDim) / 2;
        ctx.drawImage(img, sx, sy, minDim, minDim, 232, 170, 560, 560);

        // Subtle dark vignette on photo perimeter
        const vigGrad = ctx.createRadialGradient(512, 450, 180, 512, 450, 280);
        vigGrad.addColorStop(0, 'rgba(0,0,0,0)');
        vigGrad.addColorStop(1, 'rgba(7, 11, 30, 0.45)');
        ctx.fillStyle = vigGrad;
        ctx.fillRect(232, 170, 560, 560);
      } else {
        // Bespoke Royal Franchise Heritage Crest (Non-AI Handcrafted Insignia)
        const radGrad = ctx.createRadialGradient(512, 450, 40, 512, 450, 280);
        radGrad.addColorStop(0, isLocked ? '#2A364F' : '#142052');
        radGrad.addColorStop(0.7, isLocked ? '#121A29' : '#070D22');
        radGrad.addColorStop(1, isLocked ? '#0A0F18' : '#030612');
        ctx.fillStyle = radGrad;
        ctx.fillRect(232, 170, 560, 560);

        // Guilloche concentric heritage rings
        ctx.strokeStyle = isLocked ? 'rgba(148, 163, 184, 0.25)' : 'rgba(212, 175, 55, 0.35)';
        ctx.lineWidth = 2;
        [240, 210, 180, 150].forEach((r) => {
          ctx.beginPath();
          ctx.arc(512, 450, r, 0, Math.PI * 2);
          ctx.stroke();
        });

        // Top Crown Emblem Icon
        ctx.fillStyle = isLocked ? '#94A3B8' : '#D4AF37';
        ctx.font = 'bold 36px "Fraunces", serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('♛', 512, 350);

        // Heritage Serif Initials
        const initials = player.name
          .split(' ')
          .map((n) => n[0])
          .join('')
          .slice(0, 2);
        ctx.fillStyle = isLocked ? '#CBD5E1' : '#FFD700';
        ctx.font = '700 130px "Fraunces", serif';
        ctx.fillText(initials, 512, 470);
      }
      ctx.restore();

      // C. Golden Circular Beveled Frame
      ctx.beginPath();
      ctx.arc(512, 450, 284, 0, Math.PI * 2);
      ctx.lineWidth = 14;
      ctx.strokeStyle = isLocked ? '#64748B' : '#D4AF37';
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(512, 450, 276, 0, Math.PI * 2);
      ctx.lineWidth = 5;
      ctx.strokeStyle = isLocked ? '#94A3B8' : '#FFF0A0';
      ctx.stroke();

      // D. Gilded Rank Badge Pill at the Top (№ 1 to № 10)
      const rankText = `№ ${player.rank || pGroup.userData.index + 1}`;
      ctx.fillStyle = isLocked ? '#1E293B' : '#070B1E';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(386, 68, 252, 92, 46);
      } else {
        ctx.rect(386, 68, 252, 92);
      }
      ctx.fill();
      ctx.lineWidth = 6;
      ctx.strokeStyle = isLocked ? '#94A3B8' : '#FFD700';
      ctx.stroke();

      ctx.fillStyle = isLocked ? '#CBD5E1' : '#FFD700';
      ctx.font = 'bold 58px "Fraunces", serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(rankText, 512, 114);

      // E. Full Player Name Banner at the Bottom
      const fullName = player.name.toUpperCase();
      ctx.fillStyle = 'rgba(7, 11, 30, 0.98)';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(120, 746, 784, 108, 54);
      } else {
        ctx.rect(120, 746, 784, 108);
      }
      ctx.fill();
      ctx.lineWidth = 6;
      ctx.strokeStyle = isLocked ? '#64748B' : (isBowlers ? '#38BDF8' : '#EA1A85');
      ctx.stroke();

      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 54px "Barlow Condensed", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(fullName, 512, 800);

      // F. Pressure Rating Sub-Pill
      ctx.fillStyle = 'rgba(7, 11, 30, 0.96)';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(240, 872, 544, 80, 40);
      } else {
        ctx.rect(240, 872, 544, 80);
      }
      ctx.fill();
      ctx.lineWidth = 4;
      ctx.strokeStyle = isLocked ? '#475569' : '#D4AF37';
      ctx.stroke();

      ctx.fillStyle = isLocked ? '#94A3B8' : '#FFD700';
      ctx.font = '700 36px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`CLUTCH: ${(player.rating || 0).toFixed(3)}`, 512, 912);

      tex.needsUpdate = true;
    };

    // Check creditsData for real photo
    const credit = creditsData[player.name];
    if (credit && credit.file && !credit.fallback) {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => drawCard(img);
      img.onerror = () => drawCard(null);
      img.src = `./${credit.file}`;
    } else {
      drawCard(null);
    }
  }

  // Update Pillars Data (GSAP Morphing)
  function setPillarsData(playerList, isBowlers = false, credits = null) {
    if (credits) creditsData = credits;

    playerList.forEach((player, i) => {
      if (i >= NUM_PILLARS) return;
      const pGroup = pillars[i];
      pGroup.userData.player = player;

      const rating = player.rating || 0.6;
      // Proportional Pillar Height: maps 0.5-1.0 to 1.1 - 2.8 for comfortable framing
      const targetH = Math.max(1.1, (rating - 0.5) * 5.2 + 0.9);
      pGroup.userData.targetH = targetH;

      // Halo ring scaled by 90% Confidence Interval spread (Delta CI)
      const ciSpread = Math.abs((player.ci_high || 0) - (player.ci_low || 0));
      let haloScale = 1.0;
      if (isBowlers) {
        haloScale = Math.max(0.70, Math.min(1.40, ciSpread * 0.28));
      } else {
        haloScale = Math.max(0.70, Math.min(1.40, ciSpread * 0.022));
      }

      const stability = player.top10_pct || 50;
      const emissiveInt = 0.35 + (stability / 100.0) * 0.65;

      const isLocked = !player.is_available;
      pGroup.userData.isLocked = isLocked;

      let colHex = isBowlers ? 0x0284C7 : 0xEA1A85;
      if (isLocked) {
        colHex = 0x334155;
      }

      // Smooth Tweening of 3D Pillar Geometry
      gsap.to(pGroup.userData.colMesh.scale, {
        y: targetH,
        duration: 0.85,
        ease: 'power2.out'
      });

      gsap.to(pGroup.userData.capMesh.position, {
        y: targetH,
        duration: 0.85,
        ease: 'power2.out'
      });

      gsap.to(pGroup.userData.haloMesh.position, {
        y: targetH + 0.08,
        duration: 0.85,
        ease: 'power2.out'
      });

      gsap.to(pGroup.userData.haloMesh.scale, {
        x: haloScale,
        z: haloScale,
        duration: 0.85,
        ease: 'power2.out'
      });

      gsap.to(pGroup.userData.avatarSprite.position, {
        y: targetH + 1.15,
        duration: 0.85,
        ease: 'power2.out'
      });

      const targetCol = new THREE.Color(colHex);
      gsap.to(pGroup.userData.conduitMat.color, {
        r: targetCol.r,
        g: targetCol.g,
        b: targetCol.b,
        duration: 0.6
      });
      gsap.to(pGroup.userData.conduitMat.emissive, {
        r: targetCol.r,
        g: targetCol.g,
        b: targetCol.b,
        duration: 0.6
      });
      pGroup.userData.conduitMat.emissiveIntensity = isLocked ? 0.08 : emissiveInt;

      // Update High-Resolution Avatar Sprite Texture
      updateAvatarTexture(pGroup, player, isBowlers);
    });
  }

  // Auction-Eligible Filter: Sinks locked players into pool
  function setAuctionFilter(onlyEligible) {
    pillars.forEach((pGroup) => {
      if (pGroup.userData.isLocked) {
        if (onlyEligible) {
          gsap.to(pGroup.position, {
            y: -19.8,
            duration: 0.9,
            ease: 'power2.in'
          });
        } else {
          gsap.to(pGroup.position, {
            y: pGroup.userData.baseY,
            duration: 0.9,
            ease: 'back.out(1.2)'
          });
        }
      }
    });
  }

  // Dynamic Multi-Attribute Pillar Filter
  function applyPillarFilter(filterFn) {
    pillars.forEach((pGroup) => {
      const p = pGroup.userData.player;
      const matches = p && (!filterFn || filterFn(p));

      if (matches) {
        gsap.to(pGroup.position, {
          y: pGroup.userData.baseY,
          duration: 0.85,
          ease: 'power2.out'
        });
        pGroup.visible = true;
      } else {
        gsap.to(pGroup.position, {
          y: -19.8,
          duration: 0.85,
          ease: 'power2.in'
        });
      }
    });
  }

  // 8. Raycasting & Hover / Click Interactions
  const raycaster = new THREE.Raycaster();
  const mouseVec = new THREE.Vector2();
  let hoveredPillar = null;

  function onPointerMove(e) {
    mouseVec.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseVec.y = -(e.clientY / window.innerHeight) * 2 + 1;

    if (currentProgress < 0.38) return;
    raycaster.setFromCamera(mouseVec, camera);
    const intersects = raycaster.intersectObjects(pillarMeshes);

    if (intersects.length > 0) {
      const hitCol = intersects[0].object;
      const hitIndex = hitCol.userData.pillarIndex;
      const targetPillar = pillars[hitIndex];

      if (hoveredPillar !== targetPillar) {
        resetHoveredPillar();
        hoveredPillar = targetPillar;
        document.body.style.cursor = 'pointer';

        gsap.to(hoveredPillar.position, {
          y: hoveredPillar.userData.baseY + 0.32,
          duration: 0.25,
          ease: 'power2.out'
        });
        gsap.to(hoveredPillar.userData.avatarSprite.scale, {
          x: 1.82,
          y: 1.82,
          duration: 0.25,
          ease: 'power2.out'
        });
        hoveredPillar.userData.conduitMat.emissiveIntensity += 0.45;
      }
    } else {
      if (hoveredPillar) {
        resetHoveredPillar();
        document.body.style.cursor = 'default';
      }
    }
  }

  function resetHoveredPillar() {
    if (!hoveredPillar) return;
    gsap.to(hoveredPillar.position, {
      y: hoveredPillar.userData.baseY,
      duration: 0.35,
      ease: 'power2.out'
    });
    gsap.to(hoveredPillar.userData.avatarSprite.scale, {
      x: 1.48,
      y: 1.48,
      duration: 0.35,
      ease: 'power2.out'
    });
    hoveredPillar.userData.conduitMat.emissiveIntensity = Math.max(0.1, hoveredPillar.userData.conduitMat.emissiveIntensity - 0.45);
    hoveredPillar = null;
  }

  function onPointerClick(e) {
    if (currentProgress < 0.38) return;
    raycaster.setFromCamera(mouseVec, camera);
    const intersects = raycaster.intersectObjects(pillarMeshes);

    if (intersects.length > 0) {
      const hitCol = intersects[0].object;
      const hitIndex = hitCol.userData.pillarIndex;
      const targetPillar = pillars[hitIndex];
      if (targetPillar && targetPillar.userData.player && onPlayerSelect) {
        onPlayerSelect(targetPillar.userData.player);
      }
    }
  }

  window.addEventListener('mousemove', onPointerMove);
  window.addEventListener('click', onPointerClick);

  // 9. Animation & State
  let currentProgress = 0.0;
  const mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };

  window.addEventListener('mousemove', (e) => {
    mouse.targetX = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.targetY = -(e.clientY / window.innerHeight) * 2 + 1;
  });

  function updateProgress(prog) {
    currentProgress = Math.max(0, Math.min(1, prog));
  }

  function render() {
    mouse.x += (mouse.targetX - mouse.x) * 0.05;
    mouse.y += (mouse.targetY - mouse.y) * 0.05;

    const camPos = camCurve.getPoint(currentProgress);
    const lookTarget = lookCurve.getPoint(currentProgress);

    // Centered Balanced Framing across all 10 pillars (Zero sideways crop)
    const parallaxX = mouse.x * 0.15;
    const parallaxY = mouse.y * 0.15;

    camera.position.set(
      camPos.x + parallaxX,
      camPos.y + parallaxY,
      camPos.z
    );
    camera.lookAt(lookTarget.x, lookTarget.y, lookTarget.z);

    // Ball Animation in Hero
    if (currentProgress < 0.22) {
      ballGroup.visible = true;
      ballGroup.rotation.y += 0.007;
      ballGroup.rotation.z += 0.003;
      ballGroup.rotation.x = mouse.y * 0.35;
      const ballScale = Math.max(0.001, 1.0 - currentProgress * 4.5);
      ballGroup.scale.set(ballScale, ballScale, ballScale);
    } else {
      ballGroup.visible = false;
    }

    // STADIUM COLOSSEUM VISIBILITY (100% visible from Hero to Chamber)
    stadiumArenaGroup.visible = true;
    chamberGroup.visible = currentProgress >= 0.35;

    // Subtle gentle rotation of ribbon boards
    if (stadiumArenaGroup.visible) {
      ribbonMesh.rotation.y += 0.002;
      ribbon2Mesh.rotation.y -= 0.0015;

      // Soft pulsing of rooftop aviation beacons
      const beaconPulse = 0.5 + Math.sin(Date.now() * 0.004) * 0.5;
      beaconGroup.children.forEach((b) => {
        b.scale.setScalar(0.85 + beaconPulse * 0.35);
      });
    }

    // Dynamic Atmospheric Lighting across Stadium Descent
    const yLight = 10.0 - currentProgress * 22.0;
    pointLight.position.y = yLight;

    const dynamicColor = new THREE.Color();
    const dynamicFog = new THREE.Color();

    if (currentProgress < 0.25) {
      const t = currentProgress / 0.25;
      dynamicColor.setRGB(0.12, 0.18, 0.45).lerp(new THREE.Color(0.20, 0.26, 0.55), t);
      dynamicFog.setRGB(0.025, 0.04, 0.10).lerp(new THREE.Color(0.03, 0.05, 0.12), t);
    } else if (currentProgress < 0.55) {
      const t = (currentProgress - 0.25) / 0.30;
      dynamicColor.setRGB(0.20, 0.26, 0.55).lerp(new THREE.Color(0.35, 0.38, 0.65), t);
      dynamicFog.setRGB(0.03, 0.05, 0.12).lerp(new THREE.Color(0.035, 0.06, 0.14), t);
    } else if (currentProgress < 0.74) {
      const t = (currentProgress - 0.55) / 0.19;
      dynamicColor.setRGB(0.35, 0.38, 0.65).lerp(new THREE.Color(0.75, 0.70, 0.55), t);
      dynamicFog.setRGB(0.035, 0.06, 0.14).lerp(new THREE.Color(0.04, 0.07, 0.16), t);
    } else {
      // Atmospheric Stadium Floodlit Night Pitch
      const t = (currentProgress - 0.74) / 0.26;
      dynamicColor.setRGB(0.95, 0.88, 0.70).lerp(new THREE.Color(1.0, 0.94, 0.80), t);
      dynamicFog.setRGB(0.03, 0.05, 0.12).lerp(new THREE.Color(0.035, 0.065, 0.15), t);
    }

    pointLight.color.copy(dynamicColor);
    scene.fog.color.copy(dynamicFog);
    renderer.setClearColor(dynamicFog);

    // Serene, horizontal rotation of halo rings around vertical Y axis
    if (!isLowPower && chamberGroup.visible) {
      pillars.forEach((p) => {
        if (p.userData.haloMesh) {
          p.userData.haloMesh.rotation.y += 0.006;
        }
      });
    }

    renderer.render(scene, camera);
  }

  let isLowPower = false;
  function setLowPower(enabled) {
    isLowPower = !!enabled;
    renderer.setPixelRatio(isLowPower ? 1 : Math.min(window.devicePixelRatio, 2));
  }

  function handleResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }

  window.addEventListener('resize', handleResize);

  return {
    render,
    updateProgress,
    setPillarsData,
    setAuctionFilter,
    applyPillarFilter,
    setLowPower,
    dispose: () => {
      window.removeEventListener('mousemove', onPointerMove);
      window.removeEventListener('click', onPointerClick);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
    }
  };
}
