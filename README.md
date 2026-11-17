# Galaxy agentic plugins

Plugins, skills, and setup guides that connect AI coding agents to
[Galaxy](https://galaxyproject.org) in three steps:

- **Step 1 — Get a Galaxy API key** ([docs/galaxy-api-key.md](docs/galaxy-api-key.md)):
  **User › Preferences › Manage API Key** on your Galaxy server (`usegalaxy.org`,
  `usegalaxy.eu`, `usegalaxy.org.au`, or institutional).
- **Step 2 — Install for your harness** (table below): add **`galaxy-mcp`** +
  **`galaxy-skills`** for everyday analysis (add `galaxy-dev-skills` or
  `foundry-skills` only if you build tools or workflows).
- **Step 3 — Verify & run**: ask *"Connect to Galaxy and tell me who I am."*
  *(Optional on `usegalaxy.org`: [request User-Defined Tools beta access](https://udt-signup.galaxyproject.org/)
  so your agent can also author and run containerized YAML tools when no
  installed tool fits.)*

Questions, working UDT examples, and beta feedback: **[GitHub Discussions (`Agents & UDTs`)](https://github.com/galaxyproject/galaxy/discussions/categories/agents-udts)**.

## Pick your harness

| Harness | Guide | Analyst install (recommended) |
|---------|-------|-------------------------------|
| Claude Code | [docs/claude-code.md](docs/claude-code.md) | `/plugin marketplace add galaxyproject/agentic-plugins` then `/plugin install galaxy-mcp@galaxyproject` and `/plugin install galaxy-skills@galaxyproject` |
| Codex CLI | [docs/codex.md](docs/codex.md) | `codex plugin marketplace add galaxyproject/agentic-plugins` then `codex plugin add galaxy-mcp@galaxyproject` and `codex plugin add galaxy-skills@galaxyproject` |
| Antigravity (`agy`) | [docs/antigravity.md](docs/antigravity.md) | `git clone` this repo, then `agy plugin install <clone>/plugins/galaxy-mcp` and `.../galaxy-skills` |
| Pi | [docs/pi.md](docs/pi.md) | `pi mcp add galaxy -- uvx galaxy-mcp` then `pi install git:github.com/galaxyproject/agentic-plugins` |
| Cursor | [docs/cursor.md](docs/cursor.md) | **Customize › From GitHub Repository** › `galaxyproject/agentic-plugins` (`galaxy-mcp` + `galaxy-skills`) |
| Orbit (desktop app) | [docs/orbit.md](docs/orbit.md) | Download from [Orbit releases](https://github.com/galaxyproject/orbit/releases/latest) (`galaxy-mcp` + `galaxy-skills` built in; no terminal) |
| Claude Desktop | [docs/claude-desktop.md](docs/claude-desktop.md) | Open `galaxy-mcp.mcpb` from the [latest release](https://github.com/galaxyproject/agentic-plugins/releases/latest) (no terminal; MCP server only) |

## What is in the box

Four plugins live under `plugins/`. Each directory is simultaneously a Claude
Code plugin (`.claude-plugin/plugin.json`), a Codex plugin
(`.codex-plugin/plugin.json`), a Cursor plugin (`.cursor-plugin/plugin.json`)
and an Antigravity plugin (`plugin.json`); the root `package.json` exposes the
same directories as a Pi package. `bundles/claude-desktop/` is a separate
one-click installer for Claude Desktop (MCP server only).

| Plugin | Audience | Contents | Origin |
|--------|----------|----------|--------|
| `galaxy-mcp` | Everyone | MCP server config for `uvx galaxy-mcp` (48 tools: histories, datasets, tools, IWC workflows, UDTs) + `galaxy-connect` skill | this repo |
| `galaxy-skills` | Analysts & researchers | 7 skills for *using* Galaxy: `galaxy-integration` (+`jupyterlite`), `galaxy-mcp-reference`, `collection-manipulation`, `udt-authoring`, `workflow-reports`, `reproduciblify` | mirror of `galaxyproject/galaxy-skills` `skills/` |
| `galaxy-dev-skills` | Tool developers | 9 skills for *building* Galaxy: `tool-dev` (+`tool-selection-diagram`), `nf-to-galaxy` (+3 sub-skills), `update-usegalaxy-tool`, `trackhubs`, `hub-news-posts` | mirror of `galaxyproject/galaxy-skills` `dev-skills/` |
| `foundry-skills` | Workflow engineers | 69 Workflow Foundry casts, e.g. `pipeline-nextflow-to-galaxy`, `discover-shed-tool`, `validate-galaxy-workflow`, `author-galaxy-tool-wrapper` | mirror of `galaxyproject/foundry` `casts/claude/skills` |

Install only the plugins you need. Every skill plugin adds its descriptions to
the agent's context on every session: `galaxy-mcp` + `galaxy-skills` is the lean
pair for data analysis; add `galaxy-dev-skills` only if you write tool wrappers,
and `foundry-skills` only if you construct Galaxy workflows.

### How credentials reach the MCP server

`galaxy-mcp` reads `GALAXY_URL` and `GALAXY_API_KEY` from its environment or a
project `.env` file. Harnesses differ in how the environment gets there:

| Harness | Mechanism |
|---------|-----------|
| Claude Code | Prompted at install time (`userConfig`), stored in the keychain, injected via `${user_config.*}` |
| Claude Desktop | Prompted at install time (bundle `user_config`), stored in the keychain |
| Codex CLI | Only allow-listed variables are forwarded; the Codex manifest lists `GALAXY_URL` and `GALAXY_API_KEY` (`env_vars`) |
| Antigravity | Shell environment inherited as-is (or workspace `.env` for GUI IDE); `${VAR}` in `mcp_config.json` is not expanded |
| Pi | Built-in `mcp` extension (or `pi-mcp-adapter`) inherits the shell environment (or project `.env`) |
| Cursor | `${env:GALAXY_URL}` / `${env:GALAXY_API_KEY}` interpolated in `mcp/cursor.json` (or project `.env`) |

## Repository layout

```
.claude-plugin/marketplace.json   Claude Code marketplace "galaxyproject"
.agents/plugins/marketplace.json  Codex marketplace "galaxyproject"
.cursor-plugin/marketplace.json   Cursor marketplace "galaxyproject"
package.json                      Pi package manifest (pi.skills, pi.mcp)
plugins/
  galaxy-mcp/                     MCP configs (mcp/*.json, mcp_config.json) + galaxy-connect skill
  galaxy-skills/                  vendored copy of galaxy-skills skills/ (using Galaxy)
  galaxy-dev-skills/              vendored copy of galaxy-skills dev-skills/ (building Galaxy)
  foundry-skills/                 vendored copy of galaxyproject/foundry casts/claude/skills
bundles/claude-desktop/           Claude Desktop .mcpb source (uv runtime, no bundled code)
docs/                             per-harness guides (source for the Galaxy Hub page)
scripts/
  sync-skills.sh                  re-vendor upstream skills, regenerate manifests, validate
  gen-manifests.py                writes generated manifest fields (nested skill lists, versions)
  validate.py                     structural checks (run in CI)
  mcp_smoke.py                    starts galaxy-mcp over stdio and checks its tool list
  cursor-deeplink.py              generates / checks the "Add to Cursor" link in docs
  export-hub.py                   renders docs/ as Galaxy Hub page (content/agents/)
.github/
  ci-tools/                       CI-only npm deps (Pi loader check); not part of the Pi package
  workflows/validate.yml          per-harness CI jobs (see Testing)
  workflows/release.yml           packs the .mcpb and attaches it to tagged releases
  workflows/sync-skills.yml       weekly sync that opens a pull request
```

## Why vendor the skills?

Each harness installs plugins by cloning or copying a directory. None of
them is documented to follow git submodules (Pi runs a plain `git clone`),
Claude Code discovers plugin skills only one level deep, Pi stops recursing at a skill root, and Pi can
only install packages that carry a manifest. Vendoring a plain copy is the one
layout that works everywhere; `scripts/gen-manifests.py` lists nested skills
explicitly where a harness needs it. Each upstream tree is vendored into its own
plugin rather than copying the repo root, which keeps upstream's using-vs-building
split intact instead of registering both trees as one bundle. The Antigravity `plugin.json` at each
plugin root must never carry an agent-plugins.org `$schema`: Codex and Cursor
would then read it as an Agent Plugins manifest instead of their own
(`validate.py` enforces this). The pinned upstream commit is recorded in
each mirror's `UPSTREAM.json`, and the mirror plugins are versioned by sync
date (`YYYY.M.D`).

## Testing

`validate.yml` runs one job per harness on every push and pull request without
requiring an API key:

| Job | What it proves |
|-----|----------------|
| `structure` | `validate.py` + `cursor-deeplink.py --check`: manifests parse, marketplaces match `plugins/`, every SKILL.md has frontmatter, nested skill lists and versions are current |
| `claude-code` | `claude plugin validate --strict` on the marketplace and each plugin |
| `codex` | With an isolated `CODEX_HOME`, installs all four plugins from the checkout as a local marketplace, checks `codex mcp list` shows `galaxy`, and asserts >=80 skills appear in `codex debug prompt-input` |
| `antigravity` | `agy plugin validate` on each plugin |
| `pi` | Loads every `pi.skills` root with Pi's `loadSkillsFromDir` and verifies no duplicates |
| `mcp-smoke` | Starts `uvx galaxy-mcp` and the Claude Desktop bundle's `uv run` entry point over stdio, completes the MCP handshake and checks core tools; with `GALAXY_API_KEY` set, calls `get_user` live |
| `claude-desktop-bundle` | `mcpb validate` + `mcpb pack`, uploaded as a build artifact |

Local equivalent:

```bash
python3 scripts/validate.py
python3 scripts/cursor-deeplink.py --check
claude plugin validate --strict . && for p in plugins/*/; do claude plugin validate --strict "$p"; done
for p in plugins/*/; do agy plugin validate "$p"; done
python3 scripts/mcp_smoke.py
npx @anthropic-ai/mcpb validate bundles/claude-desktop/manifest.json
```

## Maintaining

```bash
scripts/sync-skills.sh                        # main of both upstreams
FOUNDRY_REF=v0.4.0 scripts/sync-skills.sh     # pin a tag, branch or commit
python3 scripts/validate.py                   # what CI runs
```

Only `plugins/galaxy-mcp/`, `docs/` and the hand-written manifest fields are
edited here; changes to skill content belong upstream. The Galaxy Hub page
at `/agents/` (plus the `/agents/plugins/` redirect) is generated from `docs/`
with `scripts/export-hub.py <galaxy-hub>/content/agents`; rerun it and
open a hub pull request after changing a guide. A GitHub Action runs
the sync every Monday and opens a pull request when anything changed.

## Related

- [galaxy-mcp](https://github.com/galaxyproject/galaxy-mcp), the MCP server
- [galaxy-skills](https://github.com/galaxyproject/galaxy-skills), skill sources
- [foundry](https://github.com/galaxyproject/foundry), the Workflow Foundry
- [orbit](https://github.com/galaxyproject/orbit), Orbit desktop Galaxy research harness

## License

MIT (see [LICENSE](LICENSE)). Vendored skills keep their upstream licenses,
copied alongside them.
