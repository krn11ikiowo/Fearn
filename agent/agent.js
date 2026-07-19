const fs = require("fs");
const { execSync } = require("child_process");

function sh(cmd) {
  return execSync(cmd, { stdio: "inherit" });
}

console.log("AI Agent: Scanning README files...");

const readmes = execSync(`find . -maxdepth 4 -type f -iname "README.md"`).toString().trim().split("\n");

for (const file of readmes) {
  if (!file) continue;

  console.log(`Processing ${file}`);

  const extracted = execSync(`grep -E "^(Feature:|TODO:|FIXME:|Planned:|Version:|Release:|Website:|App:|Source:|Branch:|Deploy:|Publish:|\\- \\[x\\]|\\- \\[ \\])" "${file}" || true`).toString();
  const code = execSync(`awk '/\`\`\`/{flag=!flag;next}flag' "${file}" || true`).toString();

  fs.writeFileSync("agent_summary.log", `Instructions:\n${extracted}\n\nCode:\n${code}`);

  // Generate patch file
  fs.writeFileSync("agent.patch", code);

  let branch = `ai-${Date.now()}`;

  if (extracted.includes("Website:")) {
    branch = `website-${Date.now()}`;
    fs.mkdirSync("website", { recursive: true });
    fs.mkdirSync("website/src", { recursive: true });
    fs.mkdirSync("website/public", { recursive: true });
  }

  if (extracted.includes("App:")) {
    branch = `app-${Date.now()}`;
    fs.mkdirSync("app", { recursive: true });
    fs.mkdirSync("app/src", { recursive: true });
    fs.mkdirSync("app/assets", { recursive: true });
  }

  if (extracted.includes("Source:")) {
    branch = `source-${Date.now()}`;
  }

  if (extracted.includes("Planned:")) {
    branch = `experimental-${Date.now()}`;
  }

  // Try applying patch
  try {
    sh(`git apply agent.patch`);
  } catch (err) {
    console.log("Patch failed, creating issue...");

    sh(`curl -X POST \
      -H "Authorization: token ${process.env.GITHUB_TOKEN}" \
      -H "Accept: application/vnd.github+json" \
      https://api.github.com/repos/${process.env.GITHUB_REPOSITORY}/issues \
      -d '{"title":"AI Patch Failed","body":"Patch failed. See logs."}'`);

    continue;
  }

  // Only create branch if source files exist
  const hasSources = execSync(`ls *.js *.ts *.swift *.m *.mm *.py *.html *.css *.json 2>/dev/null || true`).toString().trim();

  if (!hasSources) {
    console.log("No source files found, skipping branch creation.");
    continue;
  }

  // Create branch + PR
  sh(`git checkout -b ${branch}`);
  sh(`git add .`);
  sh(`git commit -m "AI Agent: Auto-applied README updates"`);
  sh(`git push origin ${branch}`);

  sh(`curl -X POST \
    -H "Authorization: token ${process.env.GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/repos/${process.env.GITHUB_REPOSITORY}/pulls \
    -d '{"title":"AI Agent Update","head":"${branch}","base":"main"}'`);
}

console.log("AI Agent: Completed.");
