# Galaxy agentic plugins

Plugins and setup guides that connect AI coding agents to
[Galaxy](https://galaxyproject.org). One install gives an agent:

1. **A Galaxy connection** through the [galaxy-mcp](https://github.com/galaxyproject/galaxy-mcp)
   MCP server, authenticated with your Galaxy API key.
2. **Curated Galaxy skills** from [galaxyproject/galaxy-skills](https://github.com/galaxyproject/galaxy-skills),
   split the way upstream splits them: skills for *using* Galaxy (MCP tool
   surface, collections, user-defined tools, workflow reports,
   reproducibility) and, separately, skills for *building* it (tool wrappers,
   Nextflow conversion, ToolShed revisions, track hubs, hub posts).
3. **Galaxy Workflow Foundry skills** from [galaxyproject/foundry](https://github.com/galaxyproject/foundry)
   (papers, Nextflow and CWL to validated Galaxy workflows).

## Pick your harness

| Harness | Guide | Install in one line |
|---------|-------|---------------------|
| Claude Code | [docs/claude-code.md](docs/claude-code.md) | `/plugin marketplace add galaxyproject/agentic-plugins` then `/plugin install galaxy-mcp@galaxyproject` |
| Claude Desktop | [docs/claude-desktop.md](docs/claude-desktop.md) | Open `galaxy-mcp.mcpb` from the [latest release](https://github.com/galaxyproject/agentic-plugins/releases/latest) |
| Codex CLI | [docs/codex.md](docs/codex.md) | `codex plugin marketplace add galaxyproject/agentic-plugins` then `codex plugin add galaxy-mcp@galaxyproject` |
| Cursor | [docs/cursor.md](docs/cursor.md) | Customize > From GitHub Repository > `galaxyproject/agentic-plugins`, or the one-click MCP link in the guide |
| Antigravity (`agy`) | [docs/antigravity.md](docs/antigravity.md) | `git clone` this repo, then `agy plugin install <clone>/plugins/galaxy-mcp` |
| Pi | [docs/pi.md](docs/pi.md) | `pi install npm:pi-mcp-adapter` then `pi install git:github.com/galaxyproject/agentic-plugins` |

Every guide starts with [getting a Galaxy API key](docs/galaxy-api-key.md).

## What is in the box

Four plugins live under `plugins/`. Each directory is simultaneously a Claude
Code plugin (`.claude-plugin/plugin.json`), a Codex plugin
(`.codex-plugin/plugin.json`), a Cursor plugin (`.cursor-plugin/plugin.json`)
and an Antigravity plugin (`plugin.json`); the root `package.json` exposes the
same directories as a Pi package. `bundles/claude-desktop/` is a separate
one-click installer for Claude Desktop (MCP server only).

| Plugin | Contents | Origin |
|--------|----------|--------|
| `galaxy-mcp` | MCP server config for `uvx galaxy-mcp` (`mcp/claude.json`, `mcp/pi.json`, `mcp.json` for Cursor, `mcp_config.json` for Antigravity, inline in the Codex manifest) and the `galaxy-connect` skill: set up, verify and troubleshoot the connection | this repo |
| `galaxy-skills` | 7 skills for *using* Galaxy: `galaxy-integration` (+`jupyterlite`), `galaxy-mcp-reference`, `collection-manipulation`, `udt-authoring`, `workflow-reports`, `reproduciblify` | mirror of galaxyproject/galaxy-skills `skills/` |
| `galaxy-dev-skills` | 9 skills for *building* Galaxy: `tool-dev` (+`tool-selection-diagram`), `nf-to-galaxy` (+3 sub-skills), `update-usegalaxy-tool`, `trackhubs`, `hub-news-posts` | mirror of galaxyproject/galaxy-skills `dev-skills/` |
| `foundry-skills` | 59 cast skills, e.g. `pipeline-nextflow-to-galaxy`, `discover-shed-tool`, `validate-galaxy-workflow`, `author-galaxy-tool-wrapper` | mirror of galaxyproject/foundry `casts/claude/skills` |

Install only the plugins you need. Every skill plugin adds its descriptions to
the agent's context on every session: `galaxy-skills` is the one an analyst
wants, `galaxy-dev-skills` is for people who write tool wrappers, and
`foundry-skills` is only worth it if you build Galaxy workflows.

### How credentials reach the MCP server

`galaxy-mcp` reads `GALAXY_URL` and `GALAXY_API_KEY` from its environment or a
project `.env` file. Harnesses differ in how the environment gets there, which
is why the plugin ships one MCP file per harness:

| Harness | Mechanism |
|---------|-----------|
| Claude Code | Prompted at install time (`userConfig`), stored in the keychain, injected via `${user_config.*}` |
| Codex CLI | Only allow-listed variables are forwarded; the Codex manifest lists the two (`env_vars`) |
| Cursor | `${env:GALAXY_URL}` / `${env:GALAXY_API_KEY}` interpolated from the environment in `mcp.json` |
| Antigravity | Shell environment inherited as-is; `${VAR}` in `mcp_config.json` is not expanded |
| Pi | `pi-mcp-adapter` inherits the shell environment |
| Claude Desktop | Prompted at install time (bundle `user_config`), stored in the keychain |

## Repository layout

```
.claude-plugin/marketplace.json   Claude Code marketplace "galaxyproject"
.agents/plugins/marketplace.json  Codex marketplace "galaxyproject"
.cursor-plugin/marketplace.json   Cursor marketplace "galaxyproject"
package.json                      Pi package manifest (pi.skills, pi.mcp)
plugins/
  galaxy-mcp/                     MCP config + galaxy-connect skill (hand-written)
  galaxy-skills/                  vendored copy of galaxy-skills skills/ (using Galaxy)
  galaxy-dev-skills/              vendored copy of galaxy-skills dev-skills/ (building Galaxy)
  foundry-skills/                 vendored copy of galaxyproject/foundry casts/claude/skills
bundles/claude-desktop/           Claude Desktop .mcpb source (uv runtime, no bundled code)
docs/                             per-harness guides (source for the Galaxy Hub pages)
scripts/
  sync-skills.sh                  re-vendor upstream skills, regenerate manifests, validate
  gen-manifests.py                writes generated manifest fields (nested skill lists, versions)
  validate.py                     structural checks (run in CI)
  mcp_smoke.py                    starts galaxy-mcp over stdio and checks its tool list
  cursor-deeplink.py              generates / checks the "Add to Cursor" link in docs
  export-hub.py                   renders docs/ as Galaxy Hub pages (content/tools/ai-agents/)
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

Everything a harness does with these files is deterministic except the model
itself, so CI checks the loaders rather than the models. `validate.yml` runs
one job per harness on every push and pull request; none of them needs an API
key or a login:

| Job | What it proves |
|-----|----------------|
| `structure` | `validate.py`: manifests parse, marketplaces match `plugins/`, every SKILL.md has frontmatter, nested skill lists and versions are regenerated, the Cursor deeplink in the docs is current |
| `claude-code` | `claude plugin validate --strict` on the marketplace and each plugin |
| `codex` | Codex's own plugin validator; then, with an isolated `CODEX_HOME`, installs all three plugins from the checkout as a local marketplace, checks `codex mcp list` shows `galaxy`, and reads the model-visible prompt with `codex debug prompt-input` to assert the skills are listed |
| `antigravity` | installs `agy` and runs `agy plugin validate` on each plugin |
| `pi` | loads every `pi.skills` root with Pi's own `loadSkillsFromDir` and checks the expected skills, no duplicates |
| `mcp-smoke` | starts `uvx galaxy-mcp` and the Claude Desktop bundle's `uv run` entry point over stdio, completes the MCP handshake and checks the core tools exist; with a `GALAXY_API_KEY` repository secret it also calls `get_user` against a live server |
| `claude-desktop-bundle` | `mcpb validate` + `mcpb pack`, uploaded as a build artifact |

What CI does not cover, by design: whether a model picks the right skill. That
needs a model call and a key. To add it later, the same commands used for
manual checks work headlessly: `claude --plugin-dir plugins/galaxy-skills -p
"list your skills"` with `ANTHROPIC_API_KEY`, and `codex exec -m <model>` with
an OpenAI key. `claude plugin eval` can grade such runs if a suite is written
under `evals/`.

Local equivalent of the whole matrix:

```bash
python3 scripts/validate.py
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
edited here; changes to skill content belong upstream. The Galaxy Hub pages
under `/tools/ai-agents/` are generated from `docs/` with
`scripts/export-hub.py <galaxy-hub>/content/tools/ai-agents`; rerun it and
open a hub pull request after changing a guide. A GitHub Action runs
the sync every Monday and opens a pull request when anything changed.

## Related

- [galaxy-mcp](https://github.com/galaxyproject/galaxy-mcp), the MCP server
- [galaxy-skills](https://github.com/galaxyproject/galaxy-skills), skill sources
- [foundry](https://github.com/galaxyproject/foundry), the Workflow Foundry
- [loom](https://github.com/galaxyproject/loom), a Pi-based Galaxy research harness

## License

MIT (see [LICENSE](LICENSE)). Vendored skills keep their upstream licenses,
copied alongside them.
