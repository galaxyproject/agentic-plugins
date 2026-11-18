#!/usr/bin/env python3
"""Export docs/ as the Galaxy Hub page /agents/ (galaxyproject/galaxy-hub).

Usage: scripts/export-hub.py <hub-content-dir>/agents

Writes:
  - <out>/index.md: single, wide, zero-distraction setup page with 6 harness
    tabs immediately above the fold (Claude Code, Codex CLI, Antigravity,
    Orbit, Claude Desktop, and Pi / Cursor / Other), each rendering numbered
    Step 1 -> Step 2 -> Step 3 cards;
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
    ("orbit.md", "orbit", "Orbit"),
    ("claude-code.md", "claude-code", "Claude Code"),
    ("codex.md", "codex", "Codex CLI"),
    ("antigravity.md", "antigravity", "Antigravity"),
    ("claude-desktop.md", "claude-desktop", "Claude Desktop"),
]

OTHER_PANEL = f"""#### Step 1 · Get your Galaxy API key and export it

- **Galaxy API key:** On [usegalaxy.org](https://usegalaxy.org) *(or [usegalaxy.eu](https://usegalaxy.eu) / [usegalaxy.org.au](https://usegalaxy.org.au))*, open **User › Preferences › Manage API Key** → **Create a new key**.
- **Custom tools on UseGalaxy.org *(optional)*:** Request [User-Defined Tools beta access](https://udt-signup.galaxyproject.org/) (~30s). Standard tools work immediately while we approve.
- **Export in `~/.zshrc` / `~/.bashrc`** *(or place in a gitignored `.env`)*:

```bash
export GALAXY_URL="https://usegalaxy.org"
export GALAXY_API_KEY="paste-your-key-here"
```

#### Step 2 · Install for your harness

Requires [uv](https://docs.astral.sh/uv/) (`uv --version`).

<h5 id="pi">Pi (<code>pi</code> 1.x)</h5>

```bash
pi mcp add galaxy -- uvx galaxy-mcp
pi install git:github.com/galaxyproject/agentic-plugins
```

Restart `pi` afterwards *(install/upgrade Pi via `npm i -g @earendil-works/pi-coding-agent`; [full Pi guide]({REPO_URL}/blob/main/docs/pi.md))*.

<h5 id="cursor">Cursor</h5>

Open **Customize › From GitHub Repository** → `galaxyproject/agentic-plugins` → install **`galaxy-mcp`** + **`galaxy-skills`** → **Developer: Reload Window** *([full Cursor guide]({REPO_URL}/blob/main/docs/cursor.md))*.

<h5 id="generic-mcp">OpenCode or any MCP + Agent Skills client</h5>

Clone `galaxy-skills` and add `uvx galaxy-mcp` to your MCP config:

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

#### Step 3 · Verify and run

Ask your agent:

```
Connect to Galaxy and tell me who I am.
```

It calls `get_user` and confirms your account. Then ask in plain language — upload reads, run IWC workflows, write JupyterLite (`gxy`) notebooks, rebuild histories (`reproduciblify`), or author containerized YAML tools (`udt-authoring`).

<details>
<summary>Pi skill filtering (context budget) & updates</summary>

`pi install` loads all 86 skills. Exclude the optional developer sets in `~/.pi/agent/settings.json` to keep per-turn context lean:

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
tease: "Pick your agent — Orbit, Claude Code, Codex CLI, Antigravity, Claude Desktop, Pi, or Cursor — and connect to Galaxy in four clear numbered steps."
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

<div class="ag-band ag-band--white">

## What your plugins include

Install **`galaxy-mcp`** + **`galaxy-skills`** for everyday analysis. Add the developer sets only if you build XML tool wrappers or construct workflows:

| Plugin | Audience | Contents | Default |
|--------|----------|----------|---------|
| **`galaxy-mcp`** | Everyone | Live Galaxy connection (48 MCP tools: histories, datasets, tools, IWC workflows, UDTs) + `galaxy-connect` | **Install** |
| **`galaxy-skills`** | Analysts & researchers | 7 skills for *using* Galaxy: MCP patterns, collections, JupyterLite notebooks (`gxy`), UDT authoring, workflow reports, `reproduciblify` | **Install** *(coding agents)* |
| **`galaxy-dev-skills`** | Tool developers | 9 skills for *building* Galaxy: ToolShed XML wrappers (`tool-dev`), Nextflow conversion (`nf-to-galaxy`), `usegalaxy-tools`, UCSC track hubs, Hub news | Optional |
| **`foundry-skills`** | Workflow engineers | 69 Workflow Foundry casts turning papers, Nextflow, and CWL into validated Galaxy workflows | Optional |

## More in this section

<div class="ag-examples">
<div class="ag-example">

**[The Galaxy agentic stack](/agents/stack/)**

Watch an agent write and run a containerized YAML tool when no installed Galaxy tool fits, with every command, container, and dataset recorded in your history.

</div>
<div class="ag-example">

**[User-Defined Tools](/tools/user-defined-tools/)**

YAML tool syntax, sandbox model, real examples, and per-account beta access on UseGalaxy.org via [udt-signup.galaxyproject.org](https://udt-signup.galaxyproject.org/).

</div>
<div class="ag-example">

**[Orbit desktop app guide](/agents/orbit/)**

Model selection & pricing, mid-session `/model` switching, local + Galaxy execution, and visual tour of the Orbit desktop app.

</div>
</div>

## Get help & share feedback

- **Agents & User-Defined Tools forum:** [GitHub Discussions (`Agents & UDTs`)](https://github.com/galaxyproject/galaxy/discussions/categories/agents-udts) — Q&A, beta feedback, and working `GalaxyUserTool` YAMLs *(real-time Matrix chat: [#galaxyproject:matrix.org](https://matrix.to/#/#galaxyproject:matrix.org))*.
- **Connection diagnostics:** run `galaxy-connect` in your agent or open the troubleshooting drawer at the bottom of your harness tab above.
- **General Galaxy support:** [Galaxy Help forum](https://help.galaxyproject.org/).
- **Plugin & bundle issues:** [galaxyproject/agentic-plugins]({REPO_URL}) (upstream skills: [galaxy-skills](https://github.com/galaxyproject/galaxy-skills) and [foundry](https://github.com/galaxyproject/foundry)).

</div>
"""

STEP_RE = re.compile(r"^#### Step (\d+)\s*[·—-]\s*(.+)$", re.M)


def wrap_step_cards(md: str, offset: int = 1) -> str:
    """Wrap each `#### Step N · Title` block in a numbered `.hstep` card.

    `offset=1` shifts per-agent Steps 1..3 to Steps 2..4 underneath Box 1 ("Pick your agent").
    """
    tail = ""
    details_idx = md.find("\n<details>")
    if details_idx != -1:
        md, tail = md[:details_idx], md[details_idx:]

    matches = list(STEP_RE.finditer(md))
    if not matches:
        return md + tail

    out: list[str] = []
    preamble = md[: matches[0].start()].strip()
    if preamble:
        out.append(preamble)

    for idx, m in enumerate(matches):
        num = int(m.group(1)) + offset
        title = m.group(2).strip()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(md)
        content = md[m.end() : end].strip()
        card = (
            f'<div class="hstep">\n'
            f'<div class="hstep__badge not-prose" aria-hidden="true">{num}</div>\n'
            f'<div class="hstep__body">\n\n'
            f'#### <span class="hstep__kicker">Step {num}</span> {title}\n\n'
            f"{content}\n\n"
            f"</div>\n"
            f"</div>"
        )
        out.append(card)

    result = "\n\n".join(out)
    if tail:
        result += "\n\n" + tail.strip()
    return result


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
    body = body.replace("(https://galaxyproject.org/agents/orbit/)", "(/agents/orbit/)")
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
    return wrap_step_cards("\n".join(out))


def guide_panel(doc: str, gid: str, name: str) -> str:
    body = body_of((DOCS / doc).read_text(), doc, shift=2)
    if gid == "orbit":
        source = "https://github.com/galaxyproject/galaxy-hub/blob/main/content/agents/orbit/index.md"
        return (
            f'<HarnessGuide id="{gid}" name="{name}" source="{source}" '
            f'sourceLabel="the Orbit guide in galaxy-hub">\n\n{body}\n\n</HarnessGuide>'
        )
    source = f"{REPO_URL}/blob/main/docs/{doc}"
    return f'<HarnessGuide id="{gid}" name="{name}" source="{source}">\n\n{body}\n\n</HarnessGuide>'


def other_panel() -> str:
    source = f"{REPO_URL}/tree/main/docs"
    body = wrap_step_cards(OTHER_PANEL)
    return f'<HarnessGuide id="other" name="Pi / Cursor / Other" source="{source}">\n\n{body}\n\n</HarnessGuide>'


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
