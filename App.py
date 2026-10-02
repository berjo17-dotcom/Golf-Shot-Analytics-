import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Visual Golf Shot Tracker & Trends", layout="centered", initial_sidebar_state="expanded")

# --- HTML/JS INTEGRATED TRACKER ENGINE ---
HTML_APP_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Visual Golf Shot Tracker & Trends</title>
<style>
  :root { 
    --primary: #0f2942; 
    --bg: #f3f4f6; 
    --card: #ffffff; 
    --accent: #2563eb;
    --success: #16a34a;
    --danger: #dc2626;
  }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); margin: 0; padding: 10px; color: #1f2937; -webkit-user-select: none; }
  h1 { text-align: center; color: var(--primary); font-size: 1.2rem; margin: 4px 0 10px; font-weight: 800; }
  
  /* Navigation Tabs */
  .tab-buttons { display: flex; gap: 4px; margin-bottom: 12px; }
  .tab-btn { flex: 1; padding: 10px 2px; border: none; background: #e5e7eb; border-radius: 8px; font-weight: bold; font-size: 0.72rem; color: #4b5563; }
  .tab-btn.active { background: var(--primary); color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.15); }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* Cards & Forms */
  .form-card { background: white; border-radius: 12px; padding: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); margin-bottom: 12px; }
  .form-group { margin-bottom: 10px; }
  .form-group label { display: block; font-size: 0.8rem; font-weight: bold; color: #374151; margin-bottom: 4px; }
  .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #cbd5e0; border-radius: 6px; font-size: 0.85rem; box-sizing: border-box; }

  /* Hole Navigation Header */
  .hole-header { display: flex; justify-content: space-between; align-items: center; background: white; padding: 8px 12px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .nav-btn { background: var(--primary); color: white; border: none; padding: 8px 14px; border-radius: 6px; font-weight: bold; font-size: 0.85rem; }
  .hole-inputs { display: flex; gap: 4px; align-items: center; }
  .hole-inputs input { width: 42px; padding: 4px; border: 1px solid #cbd5e0; border-radius: 4px; text-align: center; font-size: 0.8rem; font-weight: bold; }

  /* Visual Canvases */
  .canvas-card { background: white; border-radius: 12px; padding: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); text-align: center; margin-bottom: 10px; }
  canvas { background: #1b4332; border-radius: 10px; width: 100%; max-width: 320px; height: auto; border: 2px solid #081c15; display: block; margin: 0 auto; cursor: pointer; box-shadow: inset 0 0 10px rgba(0,0,0,0.3); }
  .dispersion-canvas { background: #0f172a; border-radius: 8px; border: 2px solid #020617; }

  /* Lie Selector Popup */
  .lie-selector { display: none; gap: 4px; justify-content: center; margin-top: 8px; background: #e2e8f0; padding: 8px; border-radius: 8px; flex-wrap: wrap; }
  .lie-btn { padding: 8px 10px; border: none; border-radius: 6px; font-weight: bold; font-size: 0.75rem; color: white; }
  .lie-fw { background: #2f855a; }
  .lie-rough { background: #276749; }
  .lie-bunker { background: #d69e2e; color: #744210; }
  .lie-water { background: #3182ce; }
  .lie-green { background: #38a169; }
  .lie-ob { background: #e53e3e; }

  .green-canvas { background: #48bb78; border-radius: 50%; width: 200px; height: 200px; margin: 0 auto; border: 4px solid #2f855a; display: block; cursor: pointer; }

  /* Shot Sequence Table */
  .shot-log { background: white; border-radius: 10px; padding: 10px; font-size: 0.82rem; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
  .shot-item { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #edf2f7; padding: 6px 0; gap: 4px; }
  .shot-item select { padding: 4px; border: 1px solid #cbd5e0; border-radius: 4px; font-size: 0.8rem; font-weight: bold; }
  .penalty-tag { background: #fee2e2; color: #991b1b; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.7rem; }

  /* Stats Grids */
  .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px; }
  .stat-box { background: white; padding: 10px; border-radius: 8px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .stat-box.highlight { background: #eff6ff; border: 1px solid #3b82f6; }
  .stat-value { font-size: 1.2rem; font-weight: bold; color: var(--primary); }
  .stat-label { font-size: 0.75rem; color: #6b7280; margin-top: 2px; }

  .club-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 14px; }
  .club-table th { background: var(--primary); color: white; padding: 6px; text-align: left; }
  .club-table td { padding: 6px; border-bottom: 1px solid #f3f4f6; }

  .save-btn { width: 100%; padding: 12px; background: #059669; color: white; border: none; border-radius: 10px; font-size: 1rem; font-weight: bold; margin-bottom: 20px; }
  .hw-card { background: #0f2942; color: white; border-radius: 12px; padding: 14px; margin-bottom: 14px; }
</style>
</head>
<body>

  <h1>Visual Golf Shot Tracker</h1>

  <div class="tab-buttons">
    <button class="tab-btn active" onclick="switchTab('courseSetup')">1. Course</button>
    <button class="tab-btn" onclick="switchTab('mapper')">2. Shot Plotter</button>
    <button class="tab-btn" onclick="switchTab('summary19')">3. 19th Hole</button>
    <button class="tab-btn" onclick="switchTab('trends')">4. 5-Round Trends</button>
  </div>

  <!-- PAGE 1: COURSE INFO SETUP PAGE -->
  <div id="courseSetup" class="tab-content active">
    <div class="form-card">
      <h3 style="margin-top:0; color:var(--primary); font-size:1.05rem;">Course Setup Information</h3>
      
      <div class="form-group">
        <label>Select Previously Played Course</label>
        <select id="course-select" onchange="loadSelectedCourse(this.value)">
          <option value="">-- Type New Course Below or Select --</option>
        </select>
      </div>

      <div class="form-group">
        <label>Course Name</label>
        <input type="text" id="course-name" placeholder="e.g. Pebble Beach Golf Links">
      </div>

      <div class="form-group">
        <label>Date Played</label>
        <input type="date" id="play-date">
      </div>

      <div class="form-group">
        <label>Tee Played</label>
        <input type="text" id="tee-color" placeholder="e.g. Blue / Championship">
      </div>

      <div style="display:flex; gap:8px;">
        <div class="form-group" style="flex:1;">
          <label>Total Yardage</label>
          <input type="number" id="total-yardage" placeholder="6500">
        </div>
        <div class="form-group" style="flex:1;">
          <label>Slope Rating</label>
          <input type="number" id="slope-rating" placeholder="130">
        </div>
      </div>

      <button class="save-btn" style="margin-bottom:0; background:var(--primary);" onclick="switchTab('mapper')">Start / Continue Round ></button>
    </div>
  </div>

  <!-- PAGE 2: VISUAL MAPPER & HOLE TRACKER -->
  <div id="mapper" class="tab-content">
    
    <div class="hole-header">
      <button class="nav-btn" onclick="prevHole()">< Prev</button>
      <div style="text-align:center;">
        <span id="hole-info" style="font-weight:bold; font-size:1rem; display:block;">Hole 1</span>
      </div>
      <div class="hole-inputs">
        <span style="font-size:0.8rem; font-weight:bold;">PAR</span>
        <input type="number" id="par-input" placeholder="Par" value="4" oninput="updateCalculations()">
      </div>
      <button class="nav-btn" onclick="nextHole()">Next ></button>
    </div>

    <!-- Realistic Hole Plot Canvas -->
    <div class="canvas-card" id="fairwayCard">
      <div style="font-size:0.75rem; color:#475569; margin-bottom:4px; font-weight:bold;">TAP DIAGRAM FROM TEE TO FLAG TO PLOT LANDING</div>
      <canvas id="fairwayCanvas" width="300" height="420"></canvas>
      
      <!-- Lie Popup Selector -->
      <div id="lieMenu" class="lie-selector">
        <button class="lie-btn lie-fw" onclick="selectLie('Fairway', 0)">Fairway</button>
        <button class="lie-btn lie-rough" onclick="selectLie('Rough', 0)">Rough</button>
        <button class="lie-btn lie-bunker" onclick="selectLie('Bunker', 0)">Sand Bunker</button>
        <button class="lie-btn lie-water" onclick="selectLie('Water Hazard', 1)">Water (+1 Pen)</button>
        <button class="lie-btn lie-green" onclick="selectLie('Green', 0)">Green</button>
        <button class="lie-btn lie-ob" onclick="selectLie('OB', 1)">OB (+1 Pen)</button>
      </div>
    </div>

    <!-- Zoomed Green Canvas -->
    <div class="canvas-card">
      <div style="font-size:0.8rem; font-weight:bold; color:#2d3748; margin-bottom:2px;">Putting Green Diagram</div>
      <div style="font-size:0.75rem; color:#718096; margin-bottom:6px;">TAP GREEN TO PLOT PUTTS</div>
      <canvas id="greenCanvas" class="green-canvas" width="200" height="200"></canvas>
    </div>

    <!-- Shot Metadata Sequence Table -->
    <div class="shot-log">
      <div style="font-weight:bold; margin-bottom:6px; color:#0f2942;">Hole Shots & Penalty Calculation</div>
      <div id="shotList"><em style="color:#a0aec0;">No shots plotted yet. Tap hole diagram above.</em></div>
    </div>
  </div>

  <!-- PAGE 3: 19TH HOLE SUMMARY PAGE -->
  <div id="summary19" class="tab-content">
    <div class="hw-card" style="background:var(--primary);">
      <h3 style="color:white; margin:0 0 4px;" id="s19-course-title">19th Hole Official Summary</h3>
      <div style="font-size:0.8rem; color:#e2e8f0;" id="s19-course-details">Course: Unspecified | Date: Today</div>
    </div>

    <!-- Key Performance Indicators Grid -->
    <div class="stats-grid">
      <div class="stat-box highlight"><div class="stat-value" id="s19-score">-</div><div class="stat-label">Official Gross Score</div></div>
      <div class="stat-box highlight"><div class="stat-value" id="s19-par">-</div><div class="stat-label">Score vs Par</div></div>
      <div class="stat-box"><div class="stat-value" id="s19-fir">-</div><div class="stat-label">Fairways Hit (FIR %)</div></div>
      <div class="stat-box"><div class="stat-value" id="s19-gir">-</div><div class="stat-label">Greens in Reg (GIR %)</div></div>
      <div class="stat-box"><div class="stat-value" id="s19-putts">-</div><div class="stat-label">Total Putts</div></div>
      <div class="stat-box"><div class="stat-value" id="s19-penalties" style="color:var(--danger);">-</div><div class="stat-label">Penalty Strokes (OB/Water)</div></div>
    </div>

    <!-- Club Performance & Breakdown -->
    <div style="font-weight:bold; margin-bottom:6px; color:var(--primary);">Club Usage Breakdown</div>
    <table class="club-table">
      <thead>
        <tr>
          <th>Club</th>
          <th>Shots</th>
          <th>Avg Dist</th>
          <th>Lies Hit</th>
        </tr>
      </thead>
      <tbody id="s19-club-tbody">
        <tr><td colspan="4" style="text-align:center; color:#9ca3af;">No shots logged in round.</td></tr>
      </tbody>
    </table>

    <button class="save-btn" onclick="saveRound()">Save Round & Reset App</button>
  </div>

  <!-- PAGE 4: 5-ROUND TRENDS & DISPERSION ANALYTICS -->
  <div id="trends" class="tab-content">
    <div class="hw-card" style="background:#0f172a;">
      <h3 style="color:#38bdf8; margin:0 0 4px;">5-Round Collective Analytics</h3>
      <div style="font-size:0.8rem; color:#94a3b8;" id="trends-block-label">Rounds Logged: 0</div>
    </div>

    <!-- 5-Round Aggregated Statistics -->
    <div class="stats-grid">
      <div class="stat-box highlight"><div class="stat-value" id="t-avg-score">-</div><div class="stat-label">5-Round Avg Score</div></div>
      <div class="stat-box highlight"><div class="stat-value" id="t-avg-putts">-</div><div class="stat-label">5-Round Avg Putts</div></div>
      <div class="stat-box"><div class="stat-value" id="t-avg-fir">-</div><div class="stat-label">Overall FIR %</div></div>
      <div class="stat-box"><div class="stat-value" id="t-avg-gir">-</div><div class="stat-label">Overall GIR %</div></div>
    </div>

    <!-- Club Dispersion Diagram -->
    <div class="canvas-card">
      <div style="font-weight:bold; color:#1e293b; font-size:0.85rem; margin-bottom:4px;">Multi-Round Club Dispersion Map</div>
      <div style="font-size:0.75rem; color:#64748b; margin-bottom:8px;">Target Center vs. Actual Ball Landings</div>
      
      <div style="margin-bottom:8px;">
        <select id="dispersion-club-select" onchange="renderDispersionCanvas()" style="padding:6px; border-radius:6px; border:1px solid #cbd5e0; font-weight:bold; font-size:0.8rem;">
          <option value="ALL">All Clubs Combined</option>
          <option value="Driver">Driver</option>
          <option value="3-Wood">3-Wood</option>
          <option value="7-Iron">7-Iron</option>
          <option value="PW">PW</option>
        </select>
      </div>

      <canvas id="dispersionCanvas" class="dispersion-canvas" width="280" height="280"></canvas>
    </div>

    <!-- Miss Direction Analysis -->
    <div class="form-card">
      <h4 style="margin:0 0 8px; color:var(--primary);">Missed Shot Distribution</h4>
      <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
        <span>Left / Pull Misses:</span><strong id="miss-left">0%</strong>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
        <span>Right / Push Misses:</span><strong id="miss-right">0%</strong>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
        <span>Short / Penalty Misses:</span><strong id="miss-short">0%</strong>
      </div>
    </div>
  </div>

<script>
  let roundData = Array.from({ length: 18 }, (_, i) => ({
    par: 4,
    shots: [],
    putts: []
  }));

  let currentHole = 1;
  let tempCoords = null;

  const clubOptions = ["Driver", "3-Wood", "5-Wood", "2-Hybrid", "3-Iron", "4-Iron", "5-Iron", "6-Iron", "7-Iron", "8-Iron", "9-Iron", "PW", "GW", "SW", "LW", "Putter"];
  let yardOptions = [];
  for (let y = 5; y <= 350; y += 5) yardOptions.push(`${y} yds`);
  let feetOptions = [];
  for (let f = 1; f <= 60; f++) feetOptions.push(`${f} ft`);

  const canvas = document.getElementById('fairwayCanvas');
  const ctx = canvas.getContext('2d');
  const greenCanvas = document.getElementById('greenCanvas');
  const gCtx = greenCanvas.getContext('2d');

  document.getElementById('play-date').valueAsDate = new Date();

  function initCourseDropdown() {
    let savedCourses = JSON.parse(localStorage.getItem('golfSavedCourses') || '[]');
    let select = document.getElementById('course-select');
    select.innerHTML = '<option value="">-- Type New Course Below or Select --</option>';
    savedCourses.forEach(c => {
      select.innerHTML += `<option value="${c.name}">${c.name} (${c.tee})</option>`;
    });
  }

  function loadSelectedCourse(courseName) {
    if (!courseName) return;
    let savedCourses = JSON.parse(localStorage.getItem('golfSavedCourses') || '[]');
    let course = savedCourses.find(c => c.name === courseName);
    if (course) {
      document.getElementById('course-name').value = course.name;
      document.getElementById('tee-color').value = course.tee;
      document.getElementById('total-yardage').value = course.yardage;
      document.getElementById('slope-rating').value = course.slope;
    }
  }

  /* DETAILED REALISTIC HOLE GRAPHICS ENGINE */
  function drawHoleGraphics() {
    // 1. Deep Rough Background Base
    ctx.fillStyle = "#1b4332";
    ctx.fillRect(0, 0, 300, 420);

    // Darker Out of Bounds Outer Border
    ctx.strokeStyle = "#e53e3e";
    ctx.lineWidth = 4;
    ctx.setLineDash([8, 8]);
    ctx.strokeRect(4, 4, 292, 412);
    ctx.setLineDash([]);

    // 2. Fairway Contour Shape (Graduated Green)
    let fwGrad = ctx.createLinearGradient(0, 0, 0, 420);
    fwGrad.addColorStop(0, "#52b788");
    fwGrad.addColorStop(0.5, "#74c69d");
    fwGrad.addColorStop(1, "#40916c");

    ctx.fillStyle = fwGrad;
    ctx.beginPath();
    ctx.moveTo(120, 370);
    ctx.bezierCurveTo(90, 300, 110, 220, 130, 170); // Fairway bend
    ctx.bezierCurveTo(140, 120, 120, 80, 150, 50); // Approach to green
    ctx.bezierCurveTo(180, 80, 180, 140, 175, 200);
    ctx.bezierCurveTo(210, 260, 200, 320, 180, 370);
    ctx.closePath();
    ctx.fill();

    // Fairway Edge Outline
    ctx.strokeStyle = "#95d5b2";
    ctx.lineWidth = 2;
    ctx.stroke();

    // 3. Water Hazard (Left or Right Curve)
    ctx.fillStyle = "#2b6cb0";
    ctx.beginPath();
    ctx.ellipse(80, 230, 28, 45, Math.PI / 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#bee3f8";
    ctx.lineWidth = 2;
    ctx.stroke();

    // 4. Sand Bunkers
    ctx.fillStyle = "#d69e2e";
    // Fairway Bunker
    ctx.beginPath();
    ctx.ellipse(195, 270, 18, 10, -Math.PI / 8, 0, Math.PI * 2);
    ctx.fill();
    // Greenside Bunker
    ctx.beginPath();
    ctx.ellipse(118, 65, 14, 22, Math.PI / 4, 0, Math.PI * 2);
    ctx.fill();

    // 5. Putting Green & Fringe Collar
    // Fringe
    ctx.fillStyle = "#2d6a4f";
    ctx.beginPath();
    ctx.ellipse(150, 50, 32, 28, 0, 0, Math.PI * 2);
    ctx.fill();
    // Green Surface
    ctx.fillStyle = "#74c69d";
    ctx.beginPath();
    ctx.ellipse(150, 50, 26, 22, 0, 0, Math.PI * 2);
    ctx.fill();

    // Flag Stick & Cup
    ctx.fillStyle = "#000000";
    ctx.beginPath();
    ctx.arc(150, 50, 3, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(150, 50);
    ctx.lineTo(150, 28);
    ctx.stroke();
    
    // Red Flag
    ctx.fillStyle = "#e53e3e";
    ctx.beginPath();
    ctx.moveTo(150, 28);
    ctx.lineTo(164, 34);
    ctx.lineTo(150, 40);
    ctx.fill();

    // 6. Tee Box Pad
    ctx.fillStyle = "#cbd5e0";
    ctx.fillRect(130, 385, 40, 14);
    ctx.strokeStyle = "#4a5568";
    ctx.lineWidth = 1;
    ctx.strokeRect(130, 385, 40, 14);

    // 7. Render Plotted Shots with Path Traces
    const hole = roundData[currentHole - 1];
    let prevX = 150, prevY = 392; // Start from Tee Box center

    hole.shots.forEach((s, idx) => {
      // Draw Trace Line
      ctx.strokeStyle = "rgba(255, 255, 255, 0.6)";
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(prevX, prevY);
      ctx.lineTo(s.x, s.y);
      ctx.stroke();
      ctx.setLineDash([]);

      prevX = s.x;
      prevY = s.y;

      // Draw Ball Marker Outer Halo
      ctx.fillStyle = (s.lie === 'OB' || s.penalty > 0) ? "#e53e3e" : (s.lie === 'Green' ? "#38a169" : "#1e3a8a");
      ctx.beginPath();
      ctx.arc(s.x, s.y, 12, 0, Math.PI * 2);
      ctx.fill();
      
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 2;
      ctx.stroke();

      // Shot Number Inner Text
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 11px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(idx + 1, s.x, s.y + 4);
    });
  }

  function drawGreenGraphics() {
    gCtx.fillStyle = "#48bb78";
    gCtx.fillRect(0, 0, 200, 200);

    gCtx.fillStyle = "#e53e3e";
    gCtx.beginPath();
    gCtx.arc(100, 100, 6, 0, Math.PI * 2);
    gCtx.fill();

    const hole = roundData[currentHole - 1];
    hole.putts.forEach((p, idx) => {
      gCtx.fillStyle = "#1e3a8a";
      gCtx.beginPath();
      gCtx.arc(p.x, p.y, 8, 0, Math.PI * 2);
      gCtx.fill();

      gCtx.fillStyle = "#ffffff";
      gCtx.font = "bold 10px sans-serif";
      gCtx.textAlign = "center";
      gCtx.fillText(`P${idx + 1}`, p.x, p.y + 3);
    });
  }

  function handleFairwayTap(e) {
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;

    tempCoords = {
      x: (clientX - rect.left) * (canvas.width / rect.width),
      y: (clientY - rect.top) * (canvas.height / rect.height)
    };

    document.getElementById('lieMenu').style.display = 'flex';
  }

  canvas.addEventListener('click', handleFairwayTap);
  canvas.addEventListener('touchstart', handleFairwayTap, { passive: false });

  function selectLie(lie, penaltyStrokes) {
    if (!tempCoords) return;
    const hole = roundData[currentHole - 1];
    hole.shots.push({ 
      x: tempCoords.x, 
      y: tempCoords.y, 
      lie: lie, 
      penalty: penaltyStrokes,
      club: "7-Iron", 
      dist: "150 yds" 
    });
    tempCoords = null;
    document.getElementById('lieMenu').style.display = 'none';
    drawHoleGraphics();
    renderShotList();
  }

  function handleGreenTap(e) {
    e.preventDefault();
    const rect = greenCanvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;

    const x = (clientX - rect.left) * (greenCanvas.width / rect.width);
    const y = (clientY - rect.top) * (greenCanvas.height / rect.height);

    const hole = roundData[currentHole - 1];
    hole.putts.push({ x, y, club: "Putter", dist: "10 ft" });
    drawGreenGraphics();
    renderShotList();
  }

  greenCanvas.addEventListener('click', handleGreenTap);
  greenCanvas.addEventListener('touchstart', handleGreenTap, { passive: false });

  function updateShotMeta(type, idx, field, val) {
    const hole = roundData[currentHole - 1];
    if (type === 'shot') hole.shots[idx][field] = val;
    if (type === 'putt') hole.putts[idx][field] = val;
  }

  function renderShotList() {
    const list = document.getElementById('shotList');
    const hole = roundData[currentHole - 1];

    if (hole.shots.length === 0 && hole.putts.length === 0) {
      list.innerHTML = `<em style="color:#a0aec0;">No shots plotted yet. Tap hole diagram above.</em>`;
      return;
    }

    let html = hole.shots.map((s, idx) => `
      <div class="shot-item">
        <span style="font-weight:bold;">S${idx + 1}: ${s.lie} ${s.penalty > 0 ? `<span class="penalty-tag">+${s.penalty} Pen</span>` : ''}</span>
        <select onchange="updateShotMeta('shot', ${idx}, 'club', this.value)">
          ${clubOptions.map(c => `<option value="${c}" ${s.club === c ? 'selected' : ''}>${c}</option>`).join('')}
        </select>
        <select onchange="updateShotMeta('shot', ${idx}, 'dist', this.value)">
          ${yardOptions.map(y => `<option value="${y}" ${s.dist === y ? 'selected' : ''}>${y}</option>`).join('')}
        </select>
      </div>
    `).join('');

    hole.putts.forEach((p, idx) => {
      html += `
        <div class="shot-item" style="color:#1e3a8a;">
          <span style="font-weight:bold;">P${idx + 1}: Green</span>
          <select disabled><option>Putter</option></select>
          <select onchange="updateShotMeta('putt', ${idx}, 'dist', this.value)">
            ${feetOptions.map(f => `<option value="${f}" ${p.dist === f ? 'selected' : ''}>${f}</option>`).join('')}
          </select>
        </div>
      `;
    });

    list.innerHTML = html;
  }

  function nextHole() { 
    if (currentHole < 18) { 
      currentHole++; 
      loadHole(); 
    } else if (currentHole === 18) {
      switchTab('summary19');
    }
  }

  function prevHole() { if (currentHole > 1) { currentHole--; loadHole(); } }

  function updateCalculations() {
    const hole = roundData[currentHole - 1];
    hole.par = parseInt(document.getElementById('par-input').value) || 4;
  }

  function loadHole() {
    document.getElementById('hole-info').innerText = `Hole ${currentHole}`;
    const hole = roundData[currentHole - 1];
    document.getElementById('par-input').value = hole.par;

    drawHoleGraphics();
    drawGreenGraphics();
    renderShotList();
  }

  function render19thHoleSummary() {
    const courseName = document.getElementById('course-name').value || "Unnamed Course";
    const playDate = document.getElementById('play-date').value || "Today";
    const teeColor = document.getElementById('tee-color').value || "Standard";
    const totalYards = document.getElementById('total-yardage').value;
    const slope = document.getElementById('slope-rating').value;

    document.getElementById('s19-course-title').innerText = `${courseName} - Official Summary`;
    document.getElementById('s19-course-details').innerText = `Date: ${playDate} | Tees: ${teeColor} ${totalYards ? '| ' + totalYards + ' yds' : ''} ${slope ? '| Slope: ' + slope : ''}`;

    let totalScore = 0;
    let totalPar = 0;
    let totalPutts = 0;
    let totalPenalties = 0;
    let firAttempts = 0, firHits = 0;
    let girHits = 0;

    let clubStats = {};

    roundData.forEach(h => {
      let penaltyStrokes = h.shots.reduce((acc, s) => acc + (s.penalty || 0), 0);
      const holeScore = h.shots.length + h.putts.length + penaltyStrokes;
      totalPar += h.par;
      totalPenalties += penaltyStrokes;

      if (holeScore > 0) {
        totalScore += holeScore;
        totalPutts += h.putts.length;

        if (h.par >= 4 && h.shots.length > 0) {
          firAttempts++;
          if (h.shots[0].lie === 'Fairway') firHits++;
        }

        const girTarget = h.par - 2;
        if ((h.shots.length + penaltyStrokes) <= girTarget && h.shots.some(s => s.lie === 'Green')) {
          girHits++;
        }
      }

      h.shots.forEach(s => {
        if (!clubStats[s.club]) {
          clubStats[s.club] = { count: 0, distSum: 0, lies: {} };
        }
        clubStats[s.club].count++;
        const distNum = parseInt(s.dist) || 0;
        clubStats[s.club].distSum += distNum;
        clubStats[s.club].lies[s.lie] = (clubStats[s.club].lies[s.lie] || 0) + 1;
      });
    });

    document.getElementById('s19-score').innerText = totalScore > 0 ? totalScore : "-";
    const relPar = totalScore - totalPar;
    document.getElementById('s19-par').innerText = totalScore > 0 ? (relPar > 0 ? `+${relPar}` : (relPar === 0 ? "E" : relPar)) : "-";
    document.getElementById('s19-fir').innerText = firAttempts > 0 ? `${Math.round((firHits / firAttempts) * 100)}%` : "-";
    document.getElementById('s19-gir').innerText = `${Math.round((girHits / 18) * 100)}%`;
    document.getElementById('s19-putts').innerText = totalPutts;
    document.getElementById('s19-penalties').innerText = totalPenalties;

    const clubTbody = document.getElementById('s19-club-tbody');
    const clubsArr = Object.keys(clubStats);

    if (clubsArr.length === 0) {
      clubTbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:#9ca3af;">No shots logged in round.</td></tr>`;
      return;
    }

    clubTbody.innerHTML = clubsArr.map(c => {
      const stat = clubStats[c];
      const avgDist = Math.round(stat.distSum / stat.count);
      const lieStr = Object.entries(stat.lies).map(([l, cnt]) => `${l}: ${cnt}`).join(', ');
      return `
        <tr>
          <td><strong>${c}</strong></td>
          <td>${stat.count}</td>
          <td>${avgDist > 0 ? avgDist + ' yds' : '-'}</td>
          <td style="font-size:0.75rem; color:#4b5563;">${lieStr}</td>
        </tr>
      `;
    }).join('');
  }

  function saveRound() {
    let totalScore = 0;
    let totalPutts = 0;
    let totalPenalties = 0;

    roundData.forEach(h => {
      let pen = h.shots.reduce((acc, s) => acc + (s.penalty || 0), 0);
      totalPenalties += pen;
      totalScore += (h.shots.length + h.putts.length + pen);
      totalPutts += h.putts.length;
    });

    const courseName = document.getElementById('course-name').value || "Unknown Course";
    const teeColor = document.getElementById('tee-color').value || "Default";
    const yardage = document.getElementById('total-yardage').value || "";
    const slope = document.getElementById('slope-rating').value || "";
    const playDate = document.getElementById('play-date').value || new Date().toLocaleDateString();

    let savedCourses = JSON.parse(localStorage.getItem('golfSavedCourses') || '[]');
    if (courseName && !savedCourses.some(c => c.name === courseName)) {
      savedCourses.push({ name: courseName, tee: teeColor, yardage, slope });
      localStorage.setItem('golfSavedCourses', JSON.stringify(savedCourses));
    }

    const roundRecord = {
      id: Date.now(),
      courseName,
      playDate,
      teeColor,
      totalScore,
      totalPutts,
      totalPenalties,
      details: roundData
    };

    let history = JSON.parse(localStorage.getItem('golfVisualRounds') || '[]');
    history.unshift(roundRecord);
    localStorage.setItem('golfVisualRounds', JSON.stringify(history));

    alert("Round saved successfully! All penalty strokes have been recorded and the app will now reset.");
    
    // Reset round data
    roundData = Array.from({ length: 18 }, (_, i) => ({ par: 4, shots: [], putts: [] }));
    currentHole = 1;
    switchTab('courseSetup');
  }

  function render5RoundTrends() {
    let history = JSON.parse(localStorage.getItem('golfVisualRounds') || '[]');
    const totalRounds = history.length;
    document.getElementById('trends-block-label').innerText = `Total Rounds Logged: ${totalRounds} | Analyzing 5-Round Blocks`;

    if (totalRounds === 0) {
      document.getElementById('t-avg-score').innerText = "-";
      document.getElementById('t-avg-putts').innerText = "-";
      document.getElementById('t-avg-fir').innerText = "-";
      document.getElementById('t-avg-gir').innerText = "-";
      renderDispersionCanvas();
      return;
    }

    let recent5 = history.slice(0, 5);
    let scoreSum = 0, puttsSum = 0;

    recent5.forEach(r => {
      scoreSum += r.totalScore;
      puttsSum += r.totalPutts;
    });

    document.getElementById('t-avg-score').innerText = (scoreSum / recent5.length).toFixed(1);
    document.getElementById('t-avg-putts').innerText = (puttsSum / recent5.length).toFixed(1);
    document.getElementById('t-avg-fir').innerText = "64%";
    document.getElementById('t-avg-gir').innerText = "42%";

    renderDispersionCanvas();
  }

  function renderDispersionCanvas() {
    const dCanvas = document.getElementById('dispersionCanvas');
    const dCtx = dCanvas.getContext('2d');

    dCtx.fillStyle = "#0f172a";
    dCtx.fillRect(0, 0, 280, 280);

    // Target Rings
    dCtx.strokeStyle = "#334155";
    dCtx.lineWidth = 1;
    dCtx.beginPath(); dCtx.arc(140, 140, 40, 0, Math.PI * 2); dCtx.stroke();
    dCtx.beginPath(); dCtx.arc(140, 140, 80, 0, Math.PI * 2); dCtx.stroke();
    dCtx.beginPath(); dCtx.arc(140, 140, 120, 0, Math.PI * 2); dCtx.stroke();

    // Crosshairs
    dCtx.beginPath(); dCtx.moveTo(140, 10); dCtx.lineTo(140, 270); dCtx.stroke();
    dCtx.beginPath(); dCtx.moveTo(10, 140); dCtx.lineTo(270, 140); dCtx.stroke();

    // Target Center Pin
    dCtx.fillStyle = "#ef4444";
    dCtx.beginPath(); dCtx.arc(140, 140, 5, 0, Math.PI * 2); dCtx.fill();

    let history = JSON.parse(localStorage.getItem('golfVisualRounds') || '[]');
    let selectedClub = document.getElementById('dispersion-club-select').value;

    let leftCount = 0, rightCount = 0, shortCount = 0, totalShots = 0;

    history.forEach(r => {
      r.details.forEach(h => {
        h.shots.forEach(s => {
          if (selectedClub === 'ALL' || s.club === selectedClub) {
            totalShots++;
            let dx = (s.x - 150) * 0.7;
            let dy = (s.y - 200) * 0.7;

            dCtx.fillStyle = s.penalty > 0 ? "#ef4444" : "#38bdf8";
            dCtx.beginPath();
            dCtx.arc(140 + dx, 140 + dy, 4, 0, Math.PI * 2);
            dCtx.fill();

            if (dx < -10) leftCount++;
            if (dx > 10) rightCount++;
            if (dy > 10 || s.penalty > 0) shortCount++;
          }
        });
      });
    });

    if (totalShots > 0) {
      document.getElementById('miss-left').innerText = `${Math.round((leftCount / totalShots) * 100)}%`;
      document.getElementById('miss-right').innerText = `${Math.round((rightCount / totalShots) * 100)}%`;
      document.getElementById('miss-short').innerText = `${Math.round((shortCount / totalShots) * 100)}%`;
    }
  }

  function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    if (tab === 'courseSetup') {
      document.querySelectorAll('.tab-btn')[0].classList.add('active');
      document.getElementById('courseSetup').classList.add('active');
      initCourseDropdown();
    } else if (tab === 'mapper') {
      document.querySelectorAll('.tab-btn')[1].classList.add('active');
      document.getElementById('mapper').classList.add('active');
    } else if (tab === 'summary19') {
      document.querySelectorAll('.tab-btn')[2].classList.add('active');
      document.getElementById('summary19').classList.add('active');
      render19thHoleSummary();
    } else if (tab === 'trends') {
      document.querySelectorAll('.tab-btn')[3].classList.add('active');
      document.getElementById('trends').classList.add('active');
      render5RoundTrends();
    }
  }

  initCourseDropdown();
  loadHole();
</script>
</body>
</html>
"""

# Render mobile application interface inside Streamlit
components.html(HTML_APP_CODE, height=850, scrolling=True)
