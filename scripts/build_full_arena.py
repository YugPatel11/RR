import sys

code = '''import * as THREE from 'three';
import gsap from 'gsap';

/**
 * SuperRR Selector - 3D Stepwell & Cricket Stadium Colosseum Engine
 * Features:
 * - 16-ring Rajasthani stepwell descent (Bands 1-4)
 * - Complete removal of stepwell lines in chamber -> transitions into an open-air cricket stadium
 * - Detailed Sawai Mansingh Stadium night colosseum: curved multi-tier grandstands, VIP suites,
 *   cantilever roof canopy, 22-yd pitch with wooden wickets/bails, sight screens, dugouts, floodlight towers with volumetric beams
 * - Surrounding Jaipur night city skyline: 48 lit towers, glowing window matrices, heritage chhatri spires, pulsing aviation beacons, arterial highways
 * - 10 luxury redesigned pillars: octagonal obsidian plinths, dark titanium shafts, vertical glowing energy conduits,
 *   gold crowns, precision dual-ring orbital halos, and ultra-crisp holographic player cards
 */
export function createStepwellScene(canvas, onPlayerSelect, initialCredits = {}) {
  let creditsData = initialCredits;

  // 1. Scene, Camera, Renderer
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x060B1E, 0.024);

  const camera = new THREE.PerspectiveCamera(
    48,
    window.innerWidth / window.innerHeight,
    0.1,
    200
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

  // 2. Camera & Look-At Spline Curves
  const camPoints = [
    new THREE.Vector3(0.0, 5.0, 16.0),    // 0: Rim / Hero
    new THREE.Vector3(3.2, 1.2, 12.0),    // 1: Band 1 (Calm)
    new THREE.Vector3(-2.8, -2.8, 8.8),   // 2: Band 2 (Rising)
    new THREE.Vector3(2.0, -6.8, 6.8),    // 3: Band 3 (Crucible)
    new THREE.Vector3(0.0, -8.6, 8.2)     // 4: Stadium pitch panoramic
  ];
  const camCurve = new THREE.CatmullRomCurve3(camPoints, false, 'centripetal');

  const lookPoints = [
    new THREE.Vector3(0.0, 3.2, 9.0),
    new THREE.Vector3(0.0, -0.5, 0.0),
    new THREE.Vector3(0.0, -4.5, 0.0),
    new THREE.Vector3(0.0, -8.5, 0.0),
    new THREE.Vector3(0.0, -12.4, -1.0)   // Looking directly at central cricket pitch & 10-pillar arc
  ];
  const lookCurve = new THREE.CatmullRomCurve3(lookPoints, false, 'centripetal');

  // 3. Stepwell Descent Rings (Visible during descent Bands 1-4, hidden in chamber)
  const RINGS = 16;
  const BLOCKS_PER_SIDE = 12;
  const TOTAL_INSTANCES = RINGS * 4 * BLOCKS_PER_SIDE;

  const boxGeo = new THREE.BoxGeometry(1.58, 0.44, 0.78);
  const stepMat = new THREE.MeshStandardMaterial({
    roughness: 0.72,
    metalness: 0.15,
    vertexColors: true
  });
  const instancedSteps = new THREE.InstancedMesh(boxGeo, stepMat, TOTAL_INSTANCES);
  instancedSteps.instanceMatrix.setUsage(THREE.StaticDrawUsage);

  const colors = [];
  const dummy = new THREE.Object3D();
  let idx = 0;

  const cNavy = new THREE.Color('#0C1433');
  const cTwilight = new THREE.Color('#2F1439');
  const cPink = new THREE.Color('#84174D');
  const cGold = new THREE.Color('#C89B38');

  for (let k = 0; k < RINGS; k++) {
    const halfSize = 14.0 - 0.8 * k;
    const yPos = -0.9 * k;
    const bandIdx = Math.floor(k / 4);

    let baseColor = new THREE.Color();
    if (bandIdx === 0) {
      baseColor.copy(cNavy).lerp(new THREE.Color('#16214C'), (k % 4) / 4);
    } else if (bandIdx === 1) {
      baseColor.copy(cTwilight).lerp(new THREE.Color('#541C48'), (k % 4) / 4);
    } else if (bandIdx === 2) {
      baseColor.copy(cPink).lerp(new THREE.Color('#A81A5C'), (k % 4) / 4);
    } else {
      baseColor.copy(cGold).lerp(new THREE.Color('#D4AF37'), (k % 4) / 4);
    }

    const stepDist = (halfSize * 2) / BLOCKS_PER_SIDE;

    for (let side = 0; side < 4; side++) {
      for (let b = 0; b < BLOCKS_PER_SIDE; b++) {
        const offset = -halfSize + b * stepDist + stepDist * 0.5;

        dummy.position.set(0, yPos, 0);
        dummy.rotation.set(0, 0, 0);

        if (side === 0) {
          dummy.position.x = offset;
          dummy.position.z = halfSize;
        } else if (side === 1) {
          dummy.position.x = offset;
          dummy.position.z = -halfSize;
        } else if (side === 2) {
          dummy.position.x = halfSize;
          dummy.position.z = offset;
          dummy.rotation.y = Math.PI / 2;
        } else {
          dummy.position.x = -halfSize;
          dummy.position.z = offset;
          dummy.rotation.y = Math.PI / 2;
        }

        dummy.updateMatrix();
        instancedSteps.setMatrixAt(idx, dummy.matrix);

        const instColor = baseColor.clone();
        const jitter = (Math.random() - 0.5) * 0.05;
        instColor.offsetHSL(jitter * 0.3, jitter * 0.5, jitter);
        colors.push(instColor.r, instColor.g, instColor.b);

        idx++;
      }
    }
  }

  instancedSteps.geometry.setAttribute(
    'color',
    new THREE.InstancedBufferAttribute(new Float32Array(colors), 3)
  );
  instancedSteps.instanceMatrix.needsUpdate = true;
  scene.add(instancedSteps);

  // 4. Top Rim Jharokha Decorative Arches
  const archShape = new THREE.Shape();
  archShape.moveTo(-0.55, 0);
  archShape.lineTo(-0.55, 1.1);
  archShape.quadraticCurveTo(-0.55, 1.7, 0, 2.1);
  archShape.quadraticCurveTo(0.55, 1.7, 0.55, 1.1);
  archShape.lineTo(0.55, 0);
  archShape.closePath();

  const archGeo = new THREE.ExtrudeGeometry(archShape, { depth: 0.28, bevelEnabled: true, bevelThickness: 0.04, bevelSize: 0.04 });
  const archMat = new THREE.MeshStandardMaterial({
    color: 0xB56B60,
    roughness: 0.75,
    metalness: 0.15
  });

  const archGroup = new THREE.Group();
  const NUM_ARCHES = 8;
  for (let i = 0; i < NUM_ARCHES; i++) {
    const angle = (i / NUM_ARCHES) * Math.PI * 2;
    const r = 14.6;
    const archMesh = new THREE.Mesh(archGeo, archMat);
    archMesh.position.set(Math.cos(angle) * r, 0.1, Math.sin(angle) * r);
    archMesh.rotation.y = -angle + Math.PI / 2;
    archGroup.add(archMesh);
  }
  scene.add(archGroup);

  // ============================================================
  // CRICKET STADIUM ARENA & SURROUNDING NIGHT CITY ENVIRONMENT
  // ============================================================
  const stadiumArenaGroup = new THREE.Group();
  stadiumArenaGroup.visible = false;
  scene.add(stadiumArenaGroup);

  // A. Lush Circular Cricket Outfield Turf (Authentic Grass)
  const outfieldGeo = new THREE.CircleGeometry(21.0, 64);
  const outfieldMat = new THREE.MeshStandardMaterial({
    color: 0x134B27,
    roughness: 0.86,
    metalness: 0.03
  });
  const outfield = new THREE.Mesh(outfieldGeo, outfieldMat);
  outfield.rotation.x = -Math.PI / 2;
  outfield.position.y = -14.78;
  stadiumArenaGroup.add(outfield);

  // Concentric Radial Grass Mowing Rings (Alternating Deep & Light Green)
  for (let r = 1; r <= 7; r++) {
    const rGeo = new THREE.RingGeometry(r * 2.85 - 0.4, r * 2.85, 48);
    const rMat = new THREE.MeshBasicMaterial({
      color: r % 2 === 0 ? 0x1E6B39 : 0x0E381C,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.42
    });
    const rMesh = new THREE.Mesh(rGeo, rMat);
    rMesh.rotation.x = -Math.PI / 2;
    rMesh.position.y = -14.77;
    stadiumArenaGroup.add(rMesh);
  }

  // B. Central 22-Yard Cricket Pitch Strip
  const pitchGeo = new THREE.PlaneGeometry(2.2, 9.4);
  const pitchMat = new THREE.MeshStandardMaterial({
    color: 0xC4A46C,
    roughness: 0.90,
    metalness: 0.02
  });
  const pitch = new THREE.Mesh(pitchGeo, pitchMat);
  pitch.rotation.x = -Math.PI / 2;
  pitch.position.set(0, -14.76, -1.8);
  stadiumArenaGroup.add(pitch);

  // Crisp White Popping & Bowling Crease Lines
  const creaseMat = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
  const crease1 = new THREE.Mesh(new THREE.PlaneGeometry(2.0, 0.08), creaseMat);
  crease1.rotation.x = -Math.PI / 2;
  crease1.position.set(0, -14.75, 2.0);
  stadiumArenaGroup.add(crease1);

  const crease2 = new THREE.Mesh(new THREE.PlaneGeometry(2.0, 0.08), creaseMat);
  crease2.rotation.x = -Math.PI / 2;
  crease2.position.set(0, -14.75, -5.6);
  stadiumArenaGroup.add(crease2);

  // Return crease side lines
  [-0.95, 0.95].forEach((rx) => {
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

  // White Slatted Sight Screens behind Bowler's Arm (North & South)
  // Realistic Slatted Cricket Sight Screens at Boundary Edge
  const screenFrameMat = new THREE.MeshStandardMaterial({ color: 0x070B1E, metalness: 0.8, roughness: 0.3 });
  const screenSlatMat = new THREE.MeshStandardMaterial({ color: 0xFAFAFA, roughness: 0.2, metalness: 0.1 });
  const screenGeo = new THREE.BoxGeometry(2.4, 1.1, 0.10);
  const screen1 = new THREE.Mesh(screenGeo, screenSlatMat);
  screen1.position.set(0, -14.76 + 0.55, 17.5);
  stadiumArenaGroup.add(screen1);

  const screen2 = new THREE.Mesh(screenGeo, screenSlatMat);
  screen2.position.set(0, -14.76 + 0.55, -17.5);
  stadiumArenaGroup.add(screen2);

  // Player Dugouts on Boundary Flanks (East & West)
  const dugoutMat = new THREE.MeshStandardMaterial({ color: 0x070B1E, metalness: 0.75, roughness: 0.25 });
  [-13.8, 13.8].forEach((dx) => {
    const dugout = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.2, 1.5), dugoutMat);
    dugout.position.set(dx, -14.76 + 0.6, -1.8);
    dugout.rotation.y = dx > 0 ? -Math.PI / 2 : Math.PI / 2;
    stadiumArenaGroup.add(dugout);
  });

  // White Stadium Boundary Rope Ring
  const ropeGeo = new THREE.TorusGeometry(14.2, 0.07, 8, 64);
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
    wMesh.position.set(Math.sin(wAngle) * 14.35, -14.65, Math.cos(wAngle) * 14.35 - 0.2);
    wMesh.rotation.y = wAngle;
    stadiumArenaGroup.add(wMesh);
  }

  // ============================================================
  // REALISTIC STADIUM GRANDSTAND COLOSSEUM (SAWAI MANSINGH STADIUM)
  // ============================================================

  // Procedural Window Grid Canvas Texture for VIP Suites & City Towers
  const winCanvas = document.createElement('canvas');
  winCanvas.width = 512;
  winCanvas.height = 512;
  const wCtx = winCanvas.getContext('2d');
  wCtx.fillStyle = '#060B1E';
  wCtx.fillRect(0, 0, 512, 512);

  const rows = 32;
  const cols = 32;
  const cw = 512 / cols;
  const ch = 512 / rows;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const rand = Math.random();
      if (rand < 0.38) {
        if (rand < 0.20) {
          wCtx.fillStyle = '#FBBF24'; // Warm tungsten amber
        } else if (rand < 0.32) {
          wCtx.fillStyle = '#FDE68A'; // Soft golden glow
        } else {
          wCtx.fillStyle = '#38BDF8'; // Cool cyan office light
        }
        wCtx.fillRect(c * cw + 2, r * ch + 3, cw - 4, ch - 6);
      }
    }
  }
  const winTex = new THREE.CanvasTexture(winCanvas);
  winTex.wrapS = THREE.RepeatWrapping;
  winTex.wrapT = THREE.RepeatWrapping;

  // Tier 1: Lower Seating Bowl (R = 14.6 to 19.2, Y = -14.76 to -12.2)
  const lowerBowlGeo = new THREE.CylinderGeometry(19.2, 14.6, 2.56, 64, 1, true);
  const lowerBowlMat = new THREE.MeshStandardMaterial({
    color: 0x0A1128,
    roughness: 0.78,
    metalness: 0.22
  });
  const lowerBowl = new THREE.Mesh(lowerBowlGeo, lowerBowlMat);
  lowerBowl.position.y = -13.48;
  stadiumArenaGroup.add(lowerBowl);

  // Concentric Seating Rows (Alternating Deep Royal Blue & Franchise Pink)
  for (let s = 1; s <= 5; s++) {
    const sRad = 14.8 + s * 0.82;
    const sY = -14.76 + s * 0.46;
    const sGeo = new THREE.RingGeometry(sRad - 0.22, sRad, 64);
    sGeo.rotateX(-Math.PI / 2);
    const sMat = new THREE.MeshBasicMaterial({
      color: s % 2 === 0 ? 0xEA1A85 : 0x1E293B,
      side: THREE.DoubleSide
    });
    const sMesh = new THREE.Mesh(sGeo, sMat);
    sMesh.position.y = sY;
    stadiumArenaGroup.add(sMesh);
  }

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

  const ribbonGeo = new THREE.CylinderGeometry(14.65, 14.65, 0.42, 64, 1, true);
  const ribbonMat = new THREE.MeshBasicMaterial({
    map: ribbonTex,
    side: THREE.DoubleSide
  });
  const ribbonMesh = new THREE.Mesh(ribbonGeo, ribbonMat);
  ribbonMesh.position.y = -12.18;
  stadiumArenaGroup.add(ribbonMesh);

  // Tier 2: VIP Hospitality Suites (Corporate Boxes with Glowing Panoramic Windows)
  const suiteBowlGeo = new THREE.CylinderGeometry(22.0, 19.2, 2.0, 64, 1, true);
  const suiteBowlMat = new THREE.MeshStandardMaterial({
    color: 0x070B1E,
    metalness: 0.85,
    roughness: 0.22,
    emissive: 0xF59E0B,
    emissiveIntensity: 0.42,
    map: winTex,
    emissiveMap: winTex
  });
  const suiteBowl = new THREE.Mesh(suiteBowlGeo, suiteBowlMat);
  suiteBowl.position.y = -11.18;
  stadiumArenaGroup.add(suiteBowl);

  // Tier 3: Upper Grandstand Terraces (R = 22.0 to 26.5, Y = -10.2 to -5.8)
  const upperBowlGeo = new THREE.CylinderGeometry(26.5, 22.0, 4.4, 64, 1, true);
  const upperBowlMat = new THREE.MeshStandardMaterial({
    color: 0x080E24,
    roughness: 0.82,
    metalness: 0.18
  });
  const upperBowl = new THREE.Mesh(upperBowlGeo, upperBowlMat);
  upperBowl.position.y = -8.0;
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

  const ribbon2Geo = new THREE.CylinderGeometry(22.1, 22.1, 0.42, 64, 1, true);
  const ribbon2Mat = new THREE.MeshBasicMaterial({ map: ribbon2Tex, side: THREE.DoubleSide });
  const ribbon2Mesh = new THREE.Mesh(ribbon2Geo, ribbon2Mat);
  ribbon2Mesh.position.y = -10.15;
  stadiumArenaGroup.add(ribbon2Mesh);

  // Cantilevered Modern Stadium Roof Structure
  const roofGeo = new THREE.CylinderGeometry(27.5, 24.2, 1.2, 64, 1, true);
  const roofMat = new THREE.MeshStandardMaterial({
    color: 0xE2E8F0,
    metalness: 0.55,
    roughness: 0.25,
    side: THREE.DoubleSide
  });
  const roofMesh = new THREE.Mesh(roofGeo, roofMat);
  roofMesh.position.y = -5.4;
  stadiumArenaGroup.add(roofMesh);

  // 16 Cantilever Structural Steel Trusses
  const trussMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.85, roughness: 0.3 });
  for (let t = 0; t < 16; t++) {
    const tAngle = (t / 16) * Math.PI * 2;
    const truss = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.35, 3.6), trussMat);
    truss.position.set(Math.sin(tAngle) * 25.8, -5.2, Math.cos(tAngle) * 25.8 - 0.2);
    truss.rotation.y = tAngle;
    stadiumArenaGroup.add(truss);
  }

  // ============================================================
  // REALISTIC SURROUNDING JAIPUR NIGHT CITY SKYLINE & URBAN LANDSCAPE
  // ============================================================
  const cityGroup = new THREE.Group();
  stadiumArenaGroup.add(cityGroup);

  const beaconGroup = new THREE.Group();
  stadiumArenaGroup.add(beaconGroup);

  const bldgMat = new THREE.MeshStandardMaterial({
    color: 0x090F26,
    metalness: 0.85,
    roughness: 0.25,
    map: winTex,
    emissive: 0xFFFFFF,
    emissiveMap: winTex,
    emissiveIntensity: 0.65
  });

  const NUM_BLDGS = 48;
  for (let i = 0; i < NUM_BLDGS; i++) {
    const angle = (i / NUM_BLDGS) * Math.PI * 2;
    // Vary radius between 31 and 44
    const rad = 31.0 + (i % 5) * 2.8 + Math.sin(i * 3.7) * 2.2;
    const bx = Math.sin(angle) * rad;
    const bz = Math.cos(angle) * rad - 1.0;

    // Varied building heights: from 12 to 32 units tall!
    const bHeight = 12.0 + (i % 7) * 3.4 + ((i * 13) % 9) * 1.5;
    const bWidth = 2.4 + (i % 4) * 0.9;
    const bDepth = 2.2 + ((i + 2) % 3) * 0.8;

    const bGeo = new THREE.BoxGeometry(bWidth, bHeight, bDepth);
    const bMesh = new THREE.Mesh(bGeo, bldgMat);
    bMesh.position.set(bx, -14.76 + bHeight / 2, bz);
    bMesh.rotation.y = angle + Math.PI / 4;
    cityGroup.add(bMesh);

    // Iconic Rajasthani Spires & Heritage Chhatri Domes on selected towers
    if (i % 3 === 0) {
      const spireH = 2.5 + (i % 3) * 0.8;
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
      const beaconGeo = new THREE.SphereGeometry(0.12, 8, 8);
      const beaconMat = new THREE.MeshBasicMaterial({
        color: i % 2 === 0 ? 0xEF4444 : 0xF59E0B
      });
      const beaconMesh = new THREE.Mesh(beaconGeo, beaconMat);
      beaconMesh.position.set(bx, -14.76 + bHeight + spireH + 0.12, bz);
      beaconGroup.add(beaconMesh);
    }
  }

  // Arterial Highway Light Ribbons around Stadium Perimeter
  const highwayGeo = new THREE.TorusGeometry(28.5, 0.22, 6, 64);
  highwayGeo.rotateX(Math.PI / 2);
  const highwayMat = new THREE.MeshBasicMaterial({
    color: 0xF59E0B,
    transparent: true,
    opacity: 0.55
  });
  const highway = new THREE.Mesh(highwayGeo, highwayMat);
  highway.position.y = -14.65;
  cityGroup.add(highway);

  const highwayOuterGeo = new THREE.TorusGeometry(30.2, 0.16, 6, 64);
  highwayOuterGeo.rotateX(Math.PI / 2);
  const highwayOuterMat = new THREE.MeshBasicMaterial({
    color: 0x38BDF8,
    transparent: true,
    opacity: 0.45
  });
  const highwayOuter = new THREE.Mesh(highwayOuterGeo, highwayOuterMat);
  highwayOuter.position.y = -14.65;
  cityGroup.add(highwayOuter);

  // ============================================================
  // FOUR HIGH-MAST STEEL LATTICE FLOODLIGHT TOWERS WITH BEAMS
  // ============================================================
  const mastPositions = [
    [-10.5, -9.5],
    [10.5, -9.5],
    [-11.5, 2.5],
    [11.5, 2.5]
  ];

  const towerTrussGeo = new THREE.CylinderGeometry(0.14, 0.32, 11.5, 8);
  const towerTrussMat = new THREE.MeshStandardMaterial({
    color: 0x475569,
    metalness: 0.88,
    roughness: 0.25
  });

  const lightBankGeo = new THREE.BoxGeometry(2.4, 1.2, 0.35);
  const lightBankMat = new THREE.MeshStandardMaterial({
    color: 0x0F172A,
    metalness: 0.9,
    roughness: 0.2
  });

  const bulbGeo = new THREE.PlaneGeometry(2.1, 1.0);
  const bulbMat = new THREE.MeshBasicMaterial({
    color: 0xFFFFFF,
    side: THREE.DoubleSide
  });

  // Soft Volumetric Light Beam Cone
  const coneGeo = new THREE.ConeGeometry(5.2, 14.0, 16, 1, true);
  coneGeo.translate(0, -7.0, 0);
  coneGeo.rotateX(Math.PI / 2);
  const coneMat = new THREE.MeshBasicMaterial({
    color: 0xFFFBEB,
    transparent: true,
    opacity: 0.065,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
    depthWrite: false
  });

  mastPositions.forEach(([mx, mz]) => {
    const tower = new THREE.Group();
    tower.position.set(mx, -9.0, mz);

    const mastMesh = new THREE.Mesh(towerTrussGeo, towerTrussMat);
    tower.add(mastMesh);

    // Floodlight bank tilted toward center pitch
    const bankMesh = new THREE.Mesh(lightBankGeo, lightBankMat);
    bankMesh.position.set(0, 5.8, 0);
    bankMesh.lookAt(new THREE.Vector3(-mx * 0.3, -5.5, -mz * 0.3 - 1.8));

    const bulbMesh = new THREE.Mesh(bulbGeo, bulbMat);
    bulbMesh.position.z = 0.18;
    bankMesh.add(bulbMesh);
    tower.add(bankMesh);

    // Volumetric Light Cone
    const coneMesh = new THREE.Mesh(coneGeo, coneMat);
    coneMesh.position.set(0, 5.8, 0);
    coneMesh.lookAt(new THREE.Vector3(-mx * 0.4, -14.76, -mz * 0.4 - 1.8));
    tower.add(coneMesh);

    // Stadium floodlight spotlight beam
    const spot = new THREE.SpotLight(0xFFF8E7, 3.6, 28, Math.PI / 4, 0.45, 1.2);
    spot.position.set(0, 5.8, 0);
    spot.target.position.set(-mx * 0.5, -14.76, -mz * 0.5 - 1.8);
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

  ballGroup.position.set(2.4, 3.2, 11.2);
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
  const ARC_RADIUS = 4.6;
  const START_ANGLE = -Math.PI * 0.38; // -68.4 deg
  const END_ANGLE = Math.PI * 0.38;    // +68.4 deg

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

    // 7. High-Resolution Holographic Avatar Billboard (Scale 1.85)
    const spriteCanvas = document.createElement('canvas');
    spriteCanvas.width = 512;
    spriteCanvas.height = 512;
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
    avatarSprite.scale.set(1.85, 1.85, 1.0);
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

  // Draw High-End Holographic Player Display on 512x512 Sprite Texture
  function updateAvatarTexture(pGroup, player, isBowlers) {
    const canvas = pGroup.userData.spriteCanvas;
    const ctx = canvas.getContext('2d');
    const tex = pGroup.userData.spriteTex;
    const isLocked = !player.is_available;

    const drawCard = (img) => {
      ctx.clearRect(0, 0, 512, 512);

      // A. Radiant Glow Backdrop
      const glowGrad = ctx.createRadialGradient(256, 210, 80, 256, 210, 215);
      const themeGlow = isLocked
        ? 'rgba(100, 116, 139, 0.4)'
        : (isBowlers ? 'rgba(56, 189, 248, 0.55)' : 'rgba(234, 26, 131, 0.58)');
      glowGrad.addColorStop(0, themeGlow);
      glowGrad.addColorStop(1, 'rgba(7, 11, 30, 0)');
      ctx.fillStyle = glowGrad;
      ctx.beginPath();
      ctx.arc(256, 210, 215, 0, Math.PI * 2);
      ctx.fill();

      // B. Large Circular Portrait / Monogram (Radius 145 = 290px wide)
      ctx.save();
      ctx.beginPath();
      ctx.arc(256, 210, 145, 0, Math.PI * 2);
      ctx.closePath();
      ctx.clip();

      if (img && img.complete && img.naturalWidth > 0) {
        const minDim = Math.min(img.naturalWidth, img.naturalHeight);
        const sx = (img.naturalWidth - minDim) / 2;
        const sy = (img.naturalHeight - minDim) / 2;
        ctx.drawImage(img, sx, sy, minDim, minDim, 111, 65, 290, 290);

        // Subtle dark vignette on photo perimeter
        const vigGrad = ctx.createRadialGradient(256, 210, 90, 256, 210, 145);
        vigGrad.addColorStop(0, 'rgba(0,0,0,0)');
        vigGrad.addColorStop(1, 'rgba(7, 11, 30, 0.42)');
        ctx.fillStyle = vigGrad;
        ctx.fillRect(111, 65, 290, 290);
      } else {
        // Handcrafted Monogram Fallback
        const grad = ctx.createLinearGradient(111, 65, 401, 355);
        grad.addColorStop(0, isLocked ? '#1E293B' : '#0B133A');
        grad.addColorStop(1, isLocked ? '#475569' : (isBowlers ? '#0284C7' : '#EA1A85'));
        ctx.fillStyle = grad;
        ctx.fillRect(111, 65, 290, 290);

        const initials = player.name
          .split(' ')
          .map((n) => n[0])
          .join('')
          .slice(0, 2);
        ctx.fillStyle = '#FFD700';
        ctx.font = 'bold 88px "Barlow Condensed", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(initials, 256, 210);
      }
      ctx.restore();

      // C. Golden Circular Beveled Frame
      ctx.beginPath();
      ctx.arc(256, 210, 147, 0, Math.PI * 2);
      ctx.lineWidth = 7;
      ctx.strokeStyle = isLocked ? '#64748B' : '#D4AF37';
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(256, 210, 142, 0, Math.PI * 2);
      ctx.lineWidth = 2.5;
      ctx.strokeStyle = isLocked ? '#94A3B8' : '#FFF0A0';
      ctx.stroke();

      // D. Gilded Rank Badge Pill at the Top (#1 to #10)
      const rankText = `#${player.rank || pGroup.userData.index + 1}`;
      ctx.fillStyle = isLocked ? '#1E293B' : '#070B1E';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(190, 36, 132, 46, 23);
      } else {
        ctx.rect(190, 36, 132, 46);
      }
      ctx.fill();
      ctx.lineWidth = 3.5;
      ctx.strokeStyle = isLocked ? '#94A3B8' : '#FFD700';
      ctx.stroke();

      ctx.fillStyle = isLocked ? '#CBD5E1' : '#FFD700';
      ctx.font = 'bold 30px "Barlow Condensed", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(rankText, 256, 59);

      // E. Player Name Pill at the Bottom
      const lastName = player.name.split(' ').pop().toUpperCase();
      ctx.fillStyle = 'rgba(7, 11, 30, 0.95)';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(118, 368, 276, 52, 26);
      } else {
        ctx.rect(118, 368, 276, 52);
      }
      ctx.fill();
      ctx.lineWidth = 3;
      ctx.strokeStyle = isLocked ? '#64748B' : (isBowlers ? '#38BDF8' : '#EA1A85');
      ctx.stroke();

      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 26px "Barlow Condensed", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(lastName, 256, 394);

      // F. Pressure Rating Sub-Pill
      ctx.fillStyle = isLocked ? '#94A3B8' : '#FFD700';
      ctx.font = '700 20px "JetBrains Mono", monospace';
      ctx.fillText(`RATING: ${(player.rating || 0).toFixed(3)}`, 256, 442);

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
        y: targetH + 1.02,
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

    if (currentProgress < 0.65) return;
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
          y: hoveredPillar.userData.baseY + 0.22,
          duration: 0.25,
          ease: 'power2.out'
        });
        gsap.to(hoveredPillar.userData.avatarSprite.scale, {
          x: 2.05,
          y: 2.05,
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
      x: 1.85,
      y: 1.85,
      duration: 0.35,
      ease: 'power2.out'
    });
    hoveredPillar.userData.conduitMat.emissiveIntensity = Math.max(0.1, hoveredPillar.userData.conduitMat.emissiveIntensity - 0.45);
    hoveredPillar = null;
  }

  function onPointerClick(e) {
    if (currentProgress < 0.65) return;
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

    // Dynamic camera horizontal pan across the 10 pillars during chamber dwell (progress 0.72 - 0.98)
    let stadiumPanX = 0;
    if (currentProgress >= 0.72 && currentProgress <= 0.98) {
      const chamberT = (currentProgress - 0.72) / 0.26;
      stadiumPanX = Math.sin((chamberT - 0.5) * Math.PI) * 1.1;
    }

    const parallaxX = mouse.x * 0.20;
    const parallaxY = mouse.y * 0.20;

    camera.position.set(
      camPos.x + stadiumPanX + parallaxX,
      camPos.y + parallaxY,
      camPos.z
    );
    camera.lookAt(lookTarget.x + stadiumPanX * 0.35, lookTarget.y, lookTarget.z);

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

    // CRITICAL: Complete removal of yellow and red stepwell lines when in the stadium chamber!
    instancedSteps.visible = currentProgress < 0.74;
    archGroup.visible = currentProgress < 0.25;

    // Dynamic Visibility of the Cricket Stadium Arena & Chamber:
    stadiumArenaGroup.visible = currentProgress > 0.58;
    chamberGroup.visible = currentProgress > 0.58;

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

    // Dynamic Lighting & Atmosphere Transition across 4 Bands
    const yLight = 1.0 - currentProgress * 15.0;
    pointLight.position.y = yLight;

    const dynamicColor = new THREE.Color();
    const dynamicFog = new THREE.Color();

    if (currentProgress < 0.25) {
      const t = currentProgress / 0.25;
      dynamicColor.copy(cNavy).lerp(cTwilight, t);
      dynamicFog.setRGB(0.03, 0.04, 0.12).lerp(new THREE.Color(0.05, 0.03, 0.12), t);
    } else if (currentProgress < 0.55) {
      const t = (currentProgress - 0.25) / 0.30;
      dynamicColor.copy(cTwilight).lerp(cPink, t);
      dynamicFog.setRGB(0.05, 0.03, 0.12).lerp(new THREE.Color(0.09, 0.02, 0.11), t);
    } else if (currentProgress < 0.74) {
      const t = (currentProgress - 0.55) / 0.19;
      dynamicColor.copy(cPink).lerp(cGold, t);
      dynamicFog.setRGB(0.09, 0.02, 0.11).lerp(new THREE.Color(0.12, 0.06, 0.06), t);
    } else {
      // Atmospheric Stadium Night Colosseum Twilight
      const t = (currentProgress - 0.74) / 0.26;
      dynamicColor.copy(cGold).lerp(new THREE.Color('#FFE082'), t);
      dynamicFog.setRGB(0.03, 0.05, 0.12).lerp(new THREE.Color(0.04, 0.07, 0.16), t);
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
'''

with open('src/stepwell.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully written updated src/stepwell.js! Length:", len(code))
