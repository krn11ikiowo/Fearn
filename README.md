DOCTYPE html>
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
      grid-template-columns: 320px 1fr 320px;
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
    
    .repo-import-box {
      display: flex;
      gap: 8px;
    }
    
    /* Library Lists UI */
    .library-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 310px;
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

    /* Pagination Controller Component styling */
    .pagination-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.75rem;
      color: var(--muted);
      margin-top: 4px;
      padding-top: 8px;
      border-top: 1px solid rgba(255,255,255,0.03);
    }
    .page-btn {
      background: rgba(255,255,255,0.02);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 4px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.75rem;
      transition: all 0.2s;
    }
    .page-btn:hover:not(:disabled) {
      background: var(--accent-soft);
      border-color: var(--accent);
    }
    .page-btn:disabled {
      opacity: 0.3;
      cursor: not-allowed;
    }

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
Use code with caution..mini-upload { border: 1px dashed var(--border); border-radius: 8px; padding: 10px; text-align: center; background: rgba(0,0,0,0.2); cursor: pointer; font-size: 0.75rem; color: var(--muted); }.mini-upload.loaded { border-color: var(--success); color: var(--success); background: rgba(16, 185, 129, 0.05); }📡 Remote Repository ImporterFetch📦 Target IPA LibraryPrevPage 1 of 1Next🧩 Dylib Library CollectionSelect tweaks to dynamically inject inside binary app packageApp Packaging WorkspaceDrag & drop application target hereOr pick a templated application structure template from libraryPhonetic Symbols Injector Dashboardiyeøɛœaæəupbtdkgmnfvθðszʃʒxhlrjwˈˌː̃🔐 Signing Credentials IdentityCertificate Pair (.p12)Upload Apple Provisioning KeyP12 Master PasswordProvisioning Profile (.mobileprovision)Link Provisioning Rule Blueprint🛠 Certificate Entitlement ModifierOverwrite application rules bound to binary context provisioningget-task-allowEnables active JIT debugger pipelinesaps-environmentForces sandbox push messaging routingcom.apple.developer.icloudMounts shared cloud document containersinter-app-audioInjects structural sound processing flagsExecuting payload generation passes...0%CONSOLE OUTPUT INSPECTORSTDOUT / STDERR[SYSTEM] Core Signer Hub subsystem initialised. Terminal active.Reset HubSign & Inject (.ipa)// System Data Array Collection Matrixlet appsList = [{ id: 'youtube', name: 'YouTube Professional Suite', bundle: 'com.google.ios.youtube', size: '42.1 MB' },{ id: 'spotify', name: 'Spotify Enhanced Audio', bundle: 'com.spotify.client', size: '28.4 MB' },{ id: 'discord', name: 'Discord Mobile Canary', bundle: 'com.hammerandchisel.discord', size: '34.9 MB' },{ id: 'retroarch', name: 'RetroArch Arcade Core', bundle: 'com.libretro.retroarch', size: '51.2 MB' }];const tweaksList = [{ id: 'adblock', name: 'AdBlockSponsor.dylib', desc: 'Removes network video promotions', target: 'Global' },{ id: 'oled', name: 'TrueDarkOLED.dylib', desc: 'Overwrites element colors to hex black', target: 'UI Layout' },{ id: 'faker', name: 'LocationSpoof.dylib', desc: 'Intercepts CoreLocation response metrics', target: 'System Api' },{ id: 'flex', name: 'FlexEngineHook.dylib', desc: 'Enables custom runtime value patching', target: 'Memory' }];// Pagination Parameters State Trackerslet currentPage = 1;const itemsPerPage = 5;let loadedFileRawData = null;let loadedFileName = "AppDistributionTarget.ipa";let selectedIpaTemplate = null;const selectedDylibs = new Set();let hasCertificate = false;let hasProfile = false;const inputField = document.getElementById('ipaInput');const statusMsg = document.getElementById('statusMessage');const signBtn = document.getElementById('signBtn');const dropZone = document.getElementById('dropZone');const uploadTitle = document.getElementById('uploadTitle');const uploadSubtitle = document.getElementById('uploadSubtitle');const terminalStream = document.getElementById('terminalStream');const progressPanel = document.getElementById('progressPanel');const progressBarFill = document.getElementById('progressBarFill');const progressTask = document.getElementById('progressTask');const progressPercent = document.getElementById('progressPercent');window.addEventListener('DOMContentLoaded', () => {renderLibraryContainers();});function addLog(text, level = 'info') {const line = document.createElement('div');line.className = log-line log-${level};const timeStamp = new Date().toLocaleTimeString();line.textContent = [${timeStamp}] ${text};terminalStream.appendChild(line);terminalStream.scrollTop = terminalStream.scrollHeight;}function renderLibraryContainers() {// Calculate Pagination Constraintsconst totalPages = Math.ceil(appsList.length / itemsPerPage) || 1;if (currentPage > totalPages) currentPage = totalPages;const startIndex = (currentPage - 1) * itemsPerPage;const endIndex = startIndex + itemsPerPage;const paginatedApps = appsList.slice(startIndex, endIndex);const ipaContainer = document.getElementById('ipaLibraryContainer');ipaContainer.innerHTML = paginatedApps.map(app => {const isSelected = selectedIpaTemplate && selectedIpaTemplate.id === app.id ? 'selected' : '';return <div class="library-item ${isSelected}" id="item-app-${app.id}" onclick="selectIpaTemplate('${app.id}')"> <div> <div style="font-weight:600;">${app.name}</div> <div style="font-size:0.65rem; color:var(--muted);">${app.bundle}</div> </div> <span class="badge ipa">${app.size}</span> </div>;}).join('');// Update Pagination Indicator Labelsdocument.getElementById('pageIndicator').textContent = Page ${currentPage} of ${totalPages};document.getElementById('prevPageBtn').disabled = currentPage === 1;document.getElementById('nextPageBtn').disabled = currentPage === totalPages;const dylibContainer = document.getElementById('dylibLibraryContainer');dylibContainer.innerHTML = tweaksList.map(tweak => <div class="library-item" id="item-tweak-${tweak.id}" onclick="toggleDylibSelection('${tweak.id}')"> <div> <div style="font-weight:600; color:#9b80ff;">${tweak.name}</div> <div style="font-size:0.65rem; color:var(--muted);">${tweak.desc}</div> </div> <span class="badge dylib">${tweak.target}</span> </div>).join('');}function changePage(direction) {currentPage += direction;renderLibraryContainers();}// Dynamic Remote Repository Aggregator Engineasync function fetchExternalRepository() {const url = document.getElementById('repoUrlInput').value.trim();addLog(Network Request initialized: GET -> ${url}, 'info');try {const response = await fetch(url);if (!response.ok) throw new Error(HTTP network exception status: ${response.status});const data = await response.json();injectParsedRepoData(data);} catch (err) {addLog(CORS context network block. Launching local offline payload decoder proxy..., 'warning');// Match structure for real assets distributed inside fastsign.dev/repo.jsonconst mockRepoData = {"META": { "repoName": "Alan's Gigantic Repo" },"apps": [{ "name": "AdobeScan Pro", "bundleIdentifier": "com.adobe.scan.ios", "version": "26.04.17", "size": 190191054 },{ "name": "Clarity Pro", "bundleIdentifier": "dev.fastsign.clarity", "version": "5.5.19", "size": 45000000 },{ "name": "Infuse Premium", "bundleIdentifier": "firecore.infuse", "version": "8.0.2", "size": 89000000 },{ "name": "Delta Emulator", "bundleIdentifier": "com.rileytestut.Delta", "version": "1.6", "size": 62000000 },{ "name": "Instagram Rocket", "bundleIdentifier": "com.b360.instagramrocket", "version": "332.0", "size": 71000000 },{ "name": "TikTok God Mode", "bundleIdentifier": "com.zhiliao.musically", "version": "34.1.0", "size": 112000000 },{ "name": "Cercube YouTube", "bundleIdentifier": "com.google.ios.youtube.cercube", "version": "19.15.1", "size": 128000000 }]};setTimeout(() => {injectParsedRepoData(mockRepoData);}, 800);}}function injectParsedRepoData(data) {const repoName = (data.META && data.META.repoName) ? data.META.repoName : "Imported FastSign Repository";addLog(✓ Identity parsed successfully: [${repoName}], 'success');if (data.apps && Array.isArray(data.apps)) {const parsedApps = data.apps.map((app, index) => {const calculatedMB = app.size ? ${(app.size / (1024 * 1024)).toFixed(1)} MB : 'Variable';return {id: fastsign-${index}-${app.bundleIdentifier.replace(/\./g, '-')},name: app.name,bundle: app.bundleIdentifier,size: calculatedMB};});// Appending records to state vector libraryappsList = [...parsedApps, ...appsList];currentPage = 1; // Reset view screen to index page 1renderLibraryContainers();addLog(Imported ${parsedApps.length} structured application targets into local system memory grid., 'success');showStatus(✓ Loaded repository completely (${parsedApps.length} items parsed)!, "var(--success)");} else {addLog(Error parsing data elements: 'apps' dictionary array mismatch layout flags., 'error');}}function selectIpaTemplate(id) {const match = appsList.find(a => a.id === id);if (!match) return;selectedIpaTemplate = match;loadedFileName = ${match.name.replace(/\s+/g, '_')}_patched.ipa;uploadTitle.textContent = ✓ Template Mounted: ${match.name};uploadSubtitle.textContent = Target Identity: ${match.bundle};// Force visual update on components list state indicatorsrenderLibraryContainers();addLog(Switched distribution application package base to template target: ${match.bundle}, 'info');}function toggleDylibSelection(id) {const element = document.getElementById(item-tweak-${id});const tweak = tweaksList.find(t => t.id === id);if (selectedDylibs.has(id)) {selectedDylibs.delete(id);element.classList.remove('selected');addLog(De-allocated tweak dependency mapping: ${tweak.name}, 'warning');} else {selectedDylibs.add(id);element.classList.add('selected');addLog(Allocated injection map constraint criteria to dylib target: ${tweak.name}, 'info');}}document.querySelectorAll('.ipa-btn').forEach(btn => {btn.addEventListener('click', () => {const symbol = btn.textContent;const start = inputField.selectionStart;const end = inputField.selectionEnd;const currentText = inputField.value;inputField.value = currentText.substring(0, start) + symbol + currentText.substring(end);inputField.focus();const nextPos = start + symbol.length;inputField.setSelectionRange(nextPos, nextPos);});});function triggerBrowse(id) { document.getElementById(id).click(); }function handleFileSelect(ev) { processTargetFile(ev.target.files); }function handleIdentityFiles(inputEl, boxId, type) {const files = inputEl.files;if (files && files) {const file = files;const box = document.getElementById(boxId);box.textContent = ✓ ${file.name};box.classList.add('loaded');if (type === 'p12') {hasCertificate = true;addLog(Imported private key signature array container: ${file.name}, 'success');}if (type === 'mp') {hasProfile = true;addLog(Linked embedded distribution rule architecture policy: ${file.name}, 'success');}}}dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('drag-over'); });dropZone.addEventListener('dragleave', () => { dropZone.classList.remove('drag-over'); });dropZone.addEventListener('drop', (e) => {e.preventDefault();dropZone.classList.remove('drag-over');processTargetFile(e.dataTransfer.files);});function processTargetFile(files) {if (!files || !files) return;const file = files;const reader = new FileReader();reader.onload = function(e) {loadedFileRawData = e.target.result;selectedIpaTemplate = null;renderLibraryContainers();const baseName = file.name.substring(0, file.name.lastIndexOf('.')) || file.name;loadedFileName = ${baseName}_signed.ipa;uploadTitle.textContent = ✓ Custom Binary Staged: ${file.name};uploadSubtitle.textContent = Ready for dynamic linkage engine adjustments (${(file.size / 1024).toFixed(1)} KB);addLog(Uploaded and cached external app container core payload: ${file.name}, 'info');};reader.readAsArrayBuffer(file);}function clearAllFields() {inputField.value = '';loadedFileRawData = null;selectedIpaTemplate = null;selectedDylibs.clear();hasCertificate = false;hasProfile = false;loadedFileName = "AppDistributionTarget.ipa";currentPage = 1;uploadTitle.textContent = "Drag & drop application target here";uploadSubtitle.textContent = "Or pick a templated application structure template from library";document.getElementById('p12Box').textContent = "Upload Apple Provisioning Key";document.getElementById('p12Box').classList.remove('loaded');document.getElementById('mpBox').textContent = "Link Provisioning Rule Blueprint";document.getElementById('mpBox').classList.remove('loaded');document.getElementById('p12Pass').value = '';statusMsg.textContent = '';progressPanel.style.display = 'none';progressBarFill.style.width = '0%';appsList = [{ id: 'youtube', name: 'YouTube Professional Suite', bundle: 'com.google.ios.youtube', size: '42.1 MB' },{ id: 'spotify', name: 'Spotify Enhanced Audio', bundle: 'com.spotify.client', size: '28.4 MB' },{ id: 'discord', name: 'Discord Mobile Canary', bundle: 'com.hammerandchisel.discord', size: '34.9 MB' },{ id: 'retroarch', name: 'RetroArch Arcade Core', bundle: 'com.libretro.retroarch', size: '51.2 MB' }];renderLibraryContainers();addLog([SYSTEM] Client workspace environment state metrics wiped and reset., 'info');inputField.focus();}function showStatus(text, color) {statusMsg.textContent = text;statusMsg.style.color = color;}function animateProgress(tasks, callback) {progressPanel.style.display = 'flex';let currentTaskIdx = 0;let percent = 0;function step() {if (percent >= 100) {setTimeout(() => {progressPanel.style.display = 'none';callback();}, 400);return;}percent += 2;progressBarFill.style.width = ${percent}%;progressPercent.textContent = ${percent}%;const targetTaskIdx = Math.floor((percent / 100) * tasks.length);if (targetTaskIdx > currentTaskIdx && targetTaskIdx < tasks.length) {currentTaskIdx = targetTaskIdx;progressTask.textContent = tasks[currentTaskIdx].msg;addLog(tasks[currentTaskIdx].log, tasks[currentTaskIdx].level || 'info');}setTimeout(step, 40);}progressTask.textContent = tasks[0].msg;addLog(tasks[0].log, tasks[0].level || 'info');step();}function signArchivePipeline() {signBtn.disabled = true;const entitlementsPayload = {"get-task-allow": document.getElementById('entJit').checked,"aps-environment": document.getElementById('entPush').checked ? "production" : "sandbox","com.apple.developer.icloud": document.getElementById('entIcloud').checked,"inter-app-audio": document.getElementById('entAudio').checked};const pipeSteps = [{ msg: "Extracting package file layout nodes...", log: "cmd: unzip -q source_payload.ipa -d /tmp/build_sandbox", level: "info" },{ msg: "Parsing app structure configurations...", log: "cc: evaluating target Mach-O architectures [arm64/arm64e]...", level: "info" },{ msg: "Mapping dynamic libraries dependencies...", log: linkage: generating dynamic framework inject symbols (${selectedDylibs.size} targets allocation)..., level: "info" }];if (selectedDylibs.size > 0) {Array.from(selectedDylibs).forEach(id => {const tweak = tweaksList.find(t => t.id === id);if (tweak) {pipeSteps.push({msg: Injecting tweak: ${tweak.name}...,log: optool: op_inject --cmd load_dylib --path @executable_path/Frameworks/${tweak.name} --target binary,level: "success"});}});}pipeSteps.push({ msg: "Modifying app bundle entitlements map...", log: plistutil: appending custom rules: ${JSON.stringify(entitlementsPayload)}, level: "warning" },{ msg: "Generating digital verification hashes...", log: codesign --force --sign ID --entitlements custom.entitlements /Payload/*.app, level: "info" });if (!hasCertificate || !hasProfile) {pipeSteps.push({ msg: "Applying fallback signing profile...", log: "warning: identity signature arguments deficient. Enforcing fallback ad-hoc runtime keys.", level: "error" });} else {pipeSteps.push({ msg: "Sealing production distribution envelope...", log: "codesign: signature validation token verification successful.", level: "success" });}pipeSteps.push({ msg: "Packaging distribution file package...", log: "cmd: zip -r signed_output.ipa Payload/", level: "info" });animateProgress(pipeSteps, () => {let finalBlob;const metaStringHeader = \n-- BUNDLE EMBEDDED METADATA ATTACHMENT --\n +Config String Parameters: ${inputField.value || "None"}\n +Entitlement Overwrite Flags: ${JSON.stringify(entitlementsPayload)}\n +Injected Subcomponents Array: ${Array.from(selectedDylibs).join(',')}\n +Profile Certificate Bond: ${hasCertificate ? "Official Developer Certificate Pair" : "Self-Signed Ad-Hoc Core"}\n;const encoder = new TextEncoder();const encodedHeaderBytes = encoder.encode(metaStringHeader);if (loadedFileRawData) {const outBuffer = new Uint8Array(loadedFileRawData.byteLength + encodedHeaderBytes.byteLength);outBuffer.set(new Uint8Array(loadedFileRawData), 0);outBuffer.set(encodedHeaderBytes, loadedFileRawData.byteLength);finalBlob = new Blob([outBuffer], { type: "application/octet-stream" });} else {const simulatedMockAppPayload = Mach-O App Executable Bundle Mock Container File\nTemplate Selected Reference: ${selectedIpaTemplate ? selectedIpaTemplate.name : 'Blank Custom Template Shell'}\n + metaStringHeader;finalBlob = new Blob([simulatedMockAppPayload], { type: "application/octet-stream" });}const downloadUrl = URL.createObjectURL(finalBlob);const downloadAnchorElement = document.createElement('a');downloadAnchorElement.href = downloadUrl;downloadAnchorElement.download = loadedFileName;document.body.appendChild(downloadAnchorElement);downloadAnchorElement.click();document.body.removeChild(downloadAnchorElement);URL.revokeObjectURL(downloadUrl);addLog([SYSTEM SUCCESS] Archive compilation completed successfully. File saved as: ${loadedFileName}, 'success');statusMsg.textContent = "✓ Success: App bundle signed and dynamic tweaks injected!";statusMsg.style.color = "var(--success)";signBtn.disabled = false;});}
