# Galaxy agentic plugins

Plugins and setup guides that connect AI coding agents to
[Galaxy](https://galaxyproject.org). One install gives an agent:

1. **A Galaxy connection** through the [galaxy-mcp](https://github.com/galaxyproject/galaxy-mcp)
   MCP server, authenticated with your Galaxy API key.
2. **Curated Galaxy skills** from [galaxyproject/galaxy-skills](https://github.com/galaxyproject/galaxy-skills)
   (tool development, user-defined tools, Nextflow conversion, collections,
   workflow reports, track hubs, hub posts, MCP usage).
3. **Galaxy Workflow Foundry skills** from [galaxyproject/foundry](https://github.com/galaxyproject/foundry)
   (papers, Nextflow and CWL to validated Galaxy workflows).

## Pick your harness

| Harness | Guide | Install in one line |
|---------|-------|---------------------|
| Claude Code | [docs/claude-code.md](docs/claude-code.md) | `/plugin marketplace add galaxyproject/agentic-plugins` then `/plugin install galaxy-mcp@galaxyproject` |
| Codex CLI | [docs/codex.md](docs/codex.md) | `codex plugin marketplace add galaxyproject/agentic-plugins` then `codex plugin add galaxy-mcp@galaxyproject` |
| Antigravity (`agy`) | [docs/antigravity.md](docs/antigravity.md) | `git clone` this repo, then `agy plugin install <clone>/plugins/galaxy-mcp` |
| Pi | [docs/pi.md](docs/pi.md) | `pi install npm:pi-mcp-adapter` then `pi install git:github.com/galaxyproject/agentic-plugins` |

Every guide starts with [getting a Galaxy API key](docs/galaxy-api-key.md).

## What is in the box

Three plugins live under `plugins/`. Each directory is simultaneously a Claude
Code plugin (`.claude-plugin/plugin.json`), a Codex plugin
(`.codex-plugin/plugin.json`) and an Antigravity plugin (`plugin.json`); the
root `package.json` exposes the same directories as a Pi package.

| Plugin | Contents | Origin |
|--------|----------|--------|
| `galaxy-mcp` | MCP server config for `uvx galaxy-mcp` (`mcp/claude.json`, `mcp/pi.json`, `mcp_config.json` for Antigravity, inline in the Codex manifest) and the `galaxy-connect` skill: set up, verify and troubleshoot the connection | this repo |
| `galaxy-skills` | 16 skills: `tool-dev`, `udt-authoring`, `nf-to-galaxy` (+3 sub-skills), `collection-manipulation`, `galaxy-integration` (+2 sub-skills), `reproduciblify`, `workflow-reports`, `trackhubs`, `update-usegalaxy-tool`, `hub-news-posts`, `tool-selection-diagram` | mirror of galaxyproject/galaxy-skills |
| `foundry-skills` | 59 cast skills, e.g. `pipeline-nextflow-to-galaxy`, `discover-shed-tool`, `validate-galaxy-workflow`, `author-galaxy-tool-wrapper` | mirror of galaxyproject/foundry `casts/claude/skills` |

Install only the plugins you need. The two skill plugins add many skill
descriptions to the agent's context; `foundry-skills` in particular is only
worth it if you build Galaxy workflows.

### How credentials reach the MCP server

`galaxy-mcp` reads `GALAXY_URL` and `GALAXY_API_KEY` from its environment or a
project `.env` file. Harnesses differ in how the environment gets there, which
is why the plugin ships one MCP file per harness:

| Harness | Mechanism |
|---------|-----------|
| Claude Code | Prompted at install time (`userConfig`), stored in the keychain, injected via `${user_config.*}` |
| Codex CLI | Only allow-listed variables are forwarded; the Codex manifest lists the two (`env_vars`) |
| Antigravity | Shell environment inherited as-is; `${VAR}` in `mcp_config.json` is not expanded |
| Pi | `pi-mcp-adapter` inherits the shell environment |

## Repository layout

```
.claude-plugin/marketplace.json   Claude Code marketplace "galaxyproject"
.agents/plugins/marketplace.json  Codex marketplace "galaxyproject"
package.json                      Pi package manifest (pi.skills, pi.mcp)
plugins/
  galaxy-mcp/                     MCP config + galaxy-connect skill (hand-written)
  galaxy-skills/                  vendored copy of galaxyproject/galaxy-skills
  foundry-skills/                 vendored copy of galaxyproject/foundry casts/claude/skills
docs/                             per-harness guides (source for the Galaxy Hub pages)
scripts/
  sync-skills.sh                  re-vendor upstream skills, regenerate manifests, validate
  gen-manifests.py                writes generated manifest fields (nested skill lists, versions)
  validate.py                     structural checks (run in CI)
.github/workflows/
  validate.yml                    validate.py + `claude plugin validate --strict`
  sync-skills.yml                 weekly sync that opens a pull request
```

## Why vendor the skills?

Each harness installs plugins by cloning or copying a directory. None of
them is documented to follow git submodules (Pi runs a plain `git clone`),
Claude Code discovers plugin skills only one level deep, Pi stops recursing at a skill root, and Pi can
only install packages that carry a manifest. Vendoring a plain copy is the one
layout that works for all four; `scripts/gen-manifests.py` lists nested skills
explicitly where a harness needs it. The pinned upstream commit is recorded in
each mirror's `UPSTREAM.json`, and the mirror plugins are versioned by sync
date (`YYYY.M.D`).

## Maintaining

```bash
scripts/sync-skills.sh                        # main of both upstreams
FOUNDRY_REF=v0.4.0 scripts/sync-skills.sh     # pin a tag, branch or commit
python3 scripts/validate.py                   # what CI runs
```

Only `plugins/galaxy-mcp/`, `docs/` and the hand-written manifest fields are
edited here; changes to skill content belong upstream. A GitHub Action runs
the sync every Monday and opens a pull request when anything changed.

## Related

- [galaxy-mcp](https://github.com/galaxyproject/galaxy-mcp), the MCP server
- [galaxy-skills](https://github.com/galaxyproject/galaxy-skills), skill sources
- [foundry](https://github.com/galaxyproject/foundry), the Workflow Foundry
- [loom](https://github.com/galaxyproject/loom), a Pi-based Galaxy research harness

## License

MIT (see [LICENSE](LICENSE)). Vendored skills keep their upstream licenses,
copied alongside them.
