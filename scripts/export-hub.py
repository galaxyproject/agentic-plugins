#!/usr/bin/env python3
"""Export docs/ as the Galaxy Hub page /agents/ (galaxyproject/galaxy-hub).

Usage: scripts/export-hub.py <hub-content-dir>/agents

Writes:
  - <out>/index.md: single, fast, zero-distraction setup page with the 5
    harness tabs immediately above the fold (Claude Code, Codex CLI,
    Antigravity, Claude Desktop, and Pi / Cursor / Other), each rendering a
    self-contained Step A -> Step B -> Step C checklist;
  - <out>/plugins/index.md: 301 redirect stub (/agents/plugins/ -> /agents/) so
    existing links and #guide-<id> hashes land on /agents/.

The docs remain the source of truth; rerun after editing them. The tab ids in
GUIDES must match `tabs` in galaxy-hub (astro/src/components/mdx/HarnessGuides.astro).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO_URL = "https://github.com/galaxyproject/agentic-plugins"

PRIMARY_GUIDES = [  # (docs file, hub id, display name)
    ("claude-code.md", "claude-code", "Claude Code"),
    ("codex.md", "codex", "Codex CLI"),
    ("antigravity.md", "antigravity", "Antigravity"),
    ("claude-desktop.md", "claude-desktop", "Claude Desktop"),
]

OTHER_PANEL = f"""Connects [Pi](https://pi.dev), [Cursor](https://cursor.com), OpenCode, or any MCP-capable coding agent to Galaxy with `galaxy-mcp` (48 Galaxy tools) and curated `galaxy-skills`.

#### Step A · Get your Galaxy API key, request UDT access, and export credentials

1. **API key:** Log in to [usegalaxy.org](https://usegalaxy.org) (or [usegalaxy.eu](https://usegalaxy.eu), [usegalaxy.org.au](https://usegalaxy.org.au), or your institution's server) → **User › Preferences › Manage API Key** → **Create a new key** → copy it.
2. **User-Defined Tools beta (UseGalaxy.org):** Submit the 30-second form at **[udt-signup.galaxyproject.org](https://udt-signup.galaxyproject.org/)** with your UseGalaxy.org email *(optional ORCID sign-in speeds review)*. Basic tools and workflows work immediately while we approve UDT access.
3. **Export credentials:** Add both variables to `~/.zshrc` or `~/.bashrc` (then open a new terminal), or place them in a project `.env` file (gitignored):

   ```bash
   export GALAXY_URL="https://usegalaxy.org"
   export GALAXY_API_KEY="paste-your-key-here"
   ```

#### Step B · Install for your harness

**Needs:** [uv](https://docs.astral.sh/uv/) on your `PATH` (`uv --version`).

<h5 id="pi">Pi (<code>pi</code> 1.x)</h5>

*(Install or upgrade Pi via `npm i -g @earendil-works/pi-coding-agent`.)*

```bash
pi mcp add galaxy -- uvx galaxy-mcp
pi install git:github.com/galaxyproject/agentic-plugins
```

Restart `pi` afterwards (`pi mcp list` checks the connection). *(Full guide: [docs/pi.md]({REPO_URL}/blob/main/docs/pi.md).)*

<h5 id="cursor">Cursor</h5>

1. Open **Customize** in the Cursor sidebar → **From GitHub Repository** → enter `galaxyproject/agentic-plugins`.
2. Install **`galaxy-mcp`** and **`galaxy-skills`** *(skip `galaxy-dev-skills` and `foundry-skills` unless you build XML wrappers or Foundry workflows)*.
3. Run **Developer: Reload Window**. *(Full guide + one-click MCP link: [docs/cursor.md]({REPO_URL}/blob/main/docs/cursor.md).)*

<h5 id="generic-mcp">OpenCode or any MCP + Agent Skills client</h5>

Clone the skills into `~/.agents/skills/` and register `uvx galaxy-mcp` in your agent's MCP config:

```bash
git clone https://github.com/galaxyproject/galaxy-skills ~/.agents/skills/galaxy-skills
```

```json
{{
  "mcpServers": {{
    "galaxy": {{
      "command": "uvx",
      "args": ["galaxy-mcp"],
      "env": {{
        "GALAXY_URL": "https://usegalaxy.org",
        "GALAXY_API_KEY": "paste-your-key-here"
      }}
    }}
  }}
}}
```

#### Step C · Verify and run

Ask your agent:

```
Connect to Galaxy and tell me who I am.
```

It calls `get_user` and reports your Galaxy username and account details *(troubleshoot anytime with `galaxy-connect`)*. Then ask in plain language — upload FASTQs, run IWC workflows, write in-Galaxy JupyterLite (`gxy`) notebooks, rebuild scratch histories (`reproduciblify`), or author containerized UDTs (`udt-authoring`).

<details>
<summary>Pi skill filtering (context budget) and updates</summary>

##### Keep only analyst skills in Pi

`pi install` loads all 86 skills across `galaxy-skills`, `galaxy-dev-skills`, and `foundry-skills`. Exclude the developer sets in `~/.pi/agent/settings.json` (or `.pi/settings.json`) to save per-turn context:

```json
{{
  "packages": [
    {{
      "source": "git:github.com/galaxyproject/agentic-plugins",
      "skills": ["!plugins/foundry-skills/**", "!plugins/galaxy-dev-skills/**"]
    }}
  ]
}}
```

Update Pi packages anytime with `pi update --extensions`.

</details>"""

LANDING = f"""---
title: "Use Galaxy from Your AI Agent"
tease: "Pick your harness — Claude Code, Codex CLI, Antigravity, Claude Desktop, Pi, or Cursor — and connect to Galaxy in three clear steps (A, B, C)."
subsites: [all]
components: true
autotoc: false
skip_title_render: true
full_bleed: true
og_image: /images/galaxy-logos/galaxy_logo_25percent.png
generated_from: {REPO_URL}/blob/main/scripts/export-hub.py
---

<HarnessGuides>

%%GUIDES%%

</HarnessGuides>

<div class="ag-band">

## What your plugins include

For everyday data analysis, install **`galaxy-mcp`** + **`galaxy-skills`** only. Add the developer sets only if you build XML tool wrappers or construct workflows, since every installed skill adds its description to each turn's context:

| Plugin | Audience | Contents | Default |
|--------|----------|----------|---------|
| **`galaxy-mcp`** | Everyone | Live Galaxy connection (48 MCP tools: histories, datasets, tools, IWC workflows, UDTs) + `galaxy-connect` | **Install** |
| **`galaxy-skills`** | Analysts & researchers | 7 skills for *using* Galaxy: MCP patterns, collections, in-Galaxy JupyterLite notebooks (`gxy`), UDT authoring, workflow reports, `reproduciblify` | **Install** *(coding agents)* |
| **`galaxy-dev-skills`** | Tool developers | 9 skills for *building* Galaxy: ToolShed XML wrappers (`tool-dev`), Nextflow conversion (`nf-to-galaxy`), `usegalaxy-tools`, UCSC track hubs, Hub news | Optional |
| **`foundry-skills`** | Workflow engineers | 69 Workflow Foundry casts turning papers, Nextflow, and CWL into validated Galaxy workflows | Optional |

## More in this section

<div class="ag-examples">
<div class="ag-example">

**[The Galaxy agentic stack](/agents/stack/)**

See an agent write and run a containerized YAML tool when no installed Galaxy tool fits, with every command, container, and dataset recorded in your history.

</div>
<div class="ag-example">

**[User-Defined Tools](/tools/user-defined-tools/)**

YAML tool syntax, sandbox model, real examples, and per-account beta access on UseGalaxy.org via [udt-signup.galaxyproject.org](https://udt-signup.galaxyproject.org/).

</div>
<div class="ag-example">

**[Orbit desktop app (beta)](/agents/orbit/)**

Don't use a coding agent yet? Orbit is a standalone desktop app for macOS, Linux, and Windows with Galaxy and the Galaxy skills already wired in.

</div>
</div>

## Get help & share feedback

- **Agents & User-Defined Tools forum:** [GitHub Discussions](https://github.com/galaxyproject/galaxy-skills/discussions) — Q&A, beta feedback, and **Show & Tell** for working `GalaxyUserTool` YAMLs and agent runs *(real-time Matrix chat: [#galaxyproject:matrix.org](https://matrix.to/#/#galaxyproject:matrix.org))*.
- **Connection diagnostics:** run `galaxy-connect` in your agent or open the **Manual MCP setup and troubleshooting** drawer in your tab above.
- **General Galaxy support:** [Galaxy Help forum](https://help.galaxyproject.org/).
- **Plugin & bundle issues:** [galaxyproject/agentic-plugins]({REPO_URL}) (upstream skills: [galaxy-skills](https://github.com/galaxyproject/galaxy-skills) and [foundry](https://github.com/galaxyproject/foundry)).

</div>
"""


def body_of(md: str, src: str, shift: int) -> str:
    """Doc body for embedding: no H1, links rewritten, headings demoted by `shift`."""
    lines = md.splitlines()
    assert lines[0].startswith("# "), f"{src}: expected H1 first"
    body = "\n".join(lines[1:]).strip("\n")
    # drop repo-internal sections (build/submission notes) from the hub copy
    body = re.sub(r"\n## For maintainers[^\n]*\n.*?(?=\n## |\Z)", "\n", body, flags=re.S).rstrip("\n")
    for doc, gid, _ in PRIMARY_GUIDES:
        body = body.replace(f"({doc})", f"(#guide-{gid})")
    body = body.replace("(pi.md)", "(#guide-pi)").replace("(cursor.md)", "(#guide-cursor)")
    body = body.replace("(galaxy-api-key.md)", f"({REPO_URL}/blob/main/docs/galaxy-api-key.md)")
    # repo-relative links (../plugins/..., bundles/...) -> GitHub
    body = re.sub(r"\]\((?:\.\./)+([^)]+)\)", rf"]({REPO_URL}/blob/main/\1)", body)
    # demote headings, but never inside fenced code
    out, fenced = [], False
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("#"):
            line = "#" * shift + line
        out.append(line)
    return "\n".join(out)


def guide_panel(doc: str, gid: str, name: str) -> str:
    body = body_of((DOCS / doc).read_text(), doc, shift=2)
    source = f"{REPO_URL}/blob/main/docs/{doc}"
    return f'<HarnessGuide id="{gid}" name="{name}" source="{source}">\n\n{body}\n\n</HarnessGuide>'


def other_panel() -> str:
    source = f"{REPO_URL}/tree/main/docs"
    return f'<HarnessGuide id="other" name="Pi / Cursor / Other" source="{source}">\n\n{OTHER_PANEL}\n\n</HarnessGuide>'


def landing() -> str:
    panels = [guide_panel(*g) for g in PRIMARY_GUIDES] + [other_panel()]
    return LANDING.replace("%%GUIDES%%", "\n\n".join(panels))


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1]).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.md").write_text(landing())
    print(f"wrote {out / 'index.md'}")
    plugins_stub = out / "plugins"
    plugins_stub.mkdir(exist_ok=True)
    (plugins_stub / "index.md").write_text(
        '---\ntitle: "Galaxy for AI Coding Agents"\nredirect: "/agents/"\n---\n'
    )
    print(f"wrote {plugins_stub / 'index.md'} -> /agents/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
