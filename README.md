<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Minimal IPA Signer & Tweak Hub</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {
      --bg: #05060a;
      --card: #0c0f18;
      --accent: #4f8cff;
      --accent-soft: rgba(79, 140, 255, 0.12);
      --text: #f5f7ff;
      --muted: #9aa0b8;
      --border: #1a1f2b;
      --danger: #ff4f6a;
      --success: #10b981;
      --radius: 14px;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
      background: radial-gradient(circle at top, #101528 0, #05060a 55%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      padding: 24px 16px;
    }
    .shell {
      width: 100%;
      max-width: 1400px;
      border-radius: 24px;
      background: linear-gradient(145deg, #05060a 0, #090b12 40%, #05060a 100%);
      border: 1px solid rgba(255, 255, 255, 0.02);
      box-shadow: 0 40px 80px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.02);
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
      padding-bottom: 16px;
    }
    .logo {
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }
    .cube {
      width: 32px;
      height: 32px;
      border-radius: 10px;
      background: conic-gradient(from 210deg, #4f8cff, #7b5cff, #4f8cff, #4f8cff);
      position: relative;
      box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.18), 0 12px 30px rgba(0, 0, 0, 0.8);
      overflow: hidden;
    }
    .cube::before {
      content: "";
      position: absolute;
      inset: 6px;
      border-radius: 7px;
      background: var(--bg);
    }
    h1 {
      font-size: 1.15rem;
      font-weight: 600;
      letter-spacing: -0.01em;
    }
    .dashboard-layout {
      display: grid;
      grid-template-columns: 280px 1fr 320px;
      gap: 20px;
    }
    @media (max-width: 1100px) {
      .dashboard-layout {
        grid-template-columns: 1fr;
      }
    }
    .column {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .panel {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .panel-title {
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
      font-weight: 700;
      border-bottom: 1px solid rgba(255,255,255,0.03);
      padding-bottom: 6px;
    }
    .drop-zone {
      border: 2px dashed var(--border);
      border-radius: var(--radius);
      padding: 24px 12px;
      text-align: center;
      background: rgba(12, 15, 24, 0.4);
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .drop-zone.drag-over {
      border-color: var(--accent);
      background: var(--accent-soft);
    }
    .drop-zone p { font-size: 0.85rem; color: var(--text); margin-bottom: 4px; }
    .drop-zone span { font-size: 0.7rem; color: var(--muted); }
    .file-input { display: none; }
    
    /* Library Lists UI */
    .library-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 250px;
      overflow-y: auto;
    }
    .library-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px;
      background: rgba(255,255,255,0.02);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 0.8rem;
      cursor: pointer;
      transition: background 0.2s;
    }
    .library-item:hover {
      background: var(--accent-soft);
      border-color: var(--accent);
    }
    .library-item.selected {
      border-color: var(--success);
      background: rgba(16, 185, 129, 0.08);
    }
    .badge {
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(255,255,255,0.1);
      color: var(--muted);
    }
    .badge.ipa { background: #4f8cff33; color: var(--accent); }
    .badge.dylib { background: #7b5cff33; color: #9b80ff; }

    /* Entitlements Switch Elements */
    .toggle-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.8rem;
    }
    .toggle-label {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .toggle-label span { font-size: 0.7rem; color: var(--muted); }
    .switch {
      position: relative;
      display: inline-block;
      width: 36px;
      height: 20px;
    }
    .switch input { opacity: 0; width: 0; height: 0; }
    .slider {
      position: absolute;
      cursor: pointer;
      inset: 0;
      background-color: var(--border);
      transition: .3s;
      border-radius: 20px;
    }
    .slider:before {
      position: absolute;
      content: "";
      height: 14px;
      width: 14px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
    }
    input:checked + .slider { background-color: var(--accent); }
    input:checked + .slider:before { transform: translateX(16px); }

    /* Keyboard Panel styling */
    .input-field-group { display: flex; flex-direction: column; gap: 4px; font-size: 0.8rem;}
    .text-field {
      width: 100%;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      padding: 8px 12px;
      font-size: 0.85rem;
      outline: none;
    }
    .text-field:focus { border-color: var(--accent); }
    textarea {
      width: 100%;
      height: 70px;
      background: rgba(0,0,0,0.3);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      color: var(--text);
      padding: 12px;
      font-size: 1rem;
      font-family: inherit;
      resize: none;
      outline: none;
    }
    .button-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(36px, 1fr)); gap: 4px; }
    .ipa-btn {
      height: 32px; background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border);
      border-radius: 6px; color: var(--text); font-size: 0.95rem; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
    }
    .ipa-btn:hover { background: var(--accent-soft); border-color: var(--accent); color: var(--accent); }

    /* Real-Time Sideloading Progress Bar Panel */
    .progress-panel {
      display: none;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px;
      flex-direction: column;
      gap: 10px;
    }
    .progress-bar-container {
      width: 100%;
      height: 10px;
      background: rgba(255,255,255,0.05);
      border-radius: 5px;
      overflow: hidden;
      border: 1px solid var(--border);
    }
    .progress-bar-fill {
      width: 0%;
      height: 100%;
      background: linear-gradient(90deg, var(--accent), var(--success));
      transition: width 0.1s linear;
    }
    .progress-meta {
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      color: var(--muted);
    }

    /* Terminal Console Window Layout View */
    .terminal-panel {
      background: #020306;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px;
      font-family: "SF Mono", Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 0.75rem;
      color: #a4b1cd;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .terminal-header {
      display: flex;
      justify-content: space-between;
      color: var(--muted);
      border-bottom: 1px solid rgba(255,255,255,0.05);
      padding-bottom: 6px;
      font-weight: bold;
    }
    .terminal-stream {
      max-height: 140px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .log-line { line-height: 1.4; white-space: pre-wrap; }
    .log-info { color: #4f8cff; }
    .log-success { color: #10b981; }
    .log-warning { color: #ffb94f; }
    .log-error { color: #ff4f6a; }

    .actions { display: flex; gap: 12px; justify-content: flex-end; align-items: center; border-top: 1px solid var(--border); padding-top: 16px; }
    .btn { padding: 10px 18px; border-radius: 10px; font-size: 0.9rem; font-weight: 500; cursor: pointer; border: none; transition: all 0.2s; }
    .btn:hover { opacity: 0.9; }
    .btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .btn-secondary { background: transparent; color: var(--muted); border: 1px solid var(--border); }
    .btn-success { background: var(--success); color: #fff; }
    #statusMessage { font-size: 0.85rem; color: var(--muted); margin-right: auto; }
    .mini-upload { border: 1px dashed var(--border); border-radius: 8px; padding: 10px; text-align: center; background: rgba(0,0,0,0.2); cursor: pointer; font-size: 0.75rem; color: var(--muted); }
    .mini-upload.loaded { border-color: var(--success); color: var(--success); background: rgba(16, 185, 129, 0.05); }
  </style>
</head>
<body>

  <div class="shell">
    <header>
      <div class="logo">
        <div class="cube"></div>
        <h1>Minimal IPA Signer & Tweak Hub</h1>
      </div>
    </header>

    <main class="workspace">
      <div class="dashboard-layout">
        
        <!-- COLUMN 1: IPA APP STORE & DYLIB INJECTION PORTFOLIO -->
        <div class="column">
          <div class="panel">
            <div class="panel-title">📦 Target IPA Library</div>
            <div class="library-list" id="ipaLibraryContainer"></div>
          </div>

          <div class="panel">
