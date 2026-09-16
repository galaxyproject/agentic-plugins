// Load every path in the root package.json `pi.skills` with Pi's own skill loader
// and check what a Pi user would actually get. Run from .github/ci-tools after `npm install`.
import { loadSkillsFromDir } from "@earendil-works/pi-coding-agent";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(process.argv[2] ?? "../..");
const pkg = JSON.parse(readFileSync(resolve(root, "package.json"), "utf8"));
const MIN_SKILLS = Number(process.env.MIN_SKILLS ?? 70);
const seen = new Map();
let problems = 0;
for (const dir of pkg.pi.skills) {
  const result = loadSkillsFromDir({ dir: resolve(root, dir), source: "ci" });
  for (const skill of result.skills) {
    if (seen.has(skill.name)) {
      console.log(`DUPLICATE ${skill.name}: ${seen.get(skill.name)} and ${skill.filePath}`);
      problems++;
    }
    seen.set(skill.name, skill.filePath);
  }
  for (const d of result.diagnostics ?? []) {
    console.log(`diagnostic (${d.type ?? "info"}) in ${dir}: ${(d.message ?? JSON.stringify(d)).split("\n")[0]}`);
  }
}
console.log(`${seen.size} skills loaded by Pi from ${pkg.pi.skills.length} roots`);
for (const must of ["galaxy-connect", "tool-dev", "nf-process-to-galaxy-tool", "jupyterlite-galaxy", "discover-shed-tool"]) {
  if (!seen.has(must)) { console.log(`MISSING expected skill ${must}`); problems++; }
}
if (seen.size < MIN_SKILLS) { console.log(`too few skills (${seen.size} < ${MIN_SKILLS})`); problems++; }
process.exit(problems ? 1 : 0);
