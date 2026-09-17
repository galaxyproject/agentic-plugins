#!/usr/bin/env python3
"""Export docs/ as Galaxy Hub pages (galaxyproject/galaxy-hub content/).

Usage: scripts/export-hub.py <hub-content-dir>/tools/ai-agents

Writes:
  index.md              landing page (template below)
  api-key/index.md      from docs/galaxy-api-key.md
  <harness>/index.md    from docs/<harness>.md

The docs remain the source of truth; rerun after editing them. Links between
docs become hub URLs, repo-relative links become GitHub URLs, and the H1 is
replaced by frontmatter.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO_URL = "https://github.com/galaxyproject/agentic-plugins"
HUB_BASE = "/tools/ai-agents"

PAGES = {  # docs file -> (hub slug, tease)
    "galaxy-api-key.md": ("api-key", "Where to find the API key every agent needs, and the two ways to hand it to galaxy-mcp."),
    "claude-code.md": ("claude-code", "Install the Galaxy MCP server and skills into Claude Code from the galaxyproject plugin marketplace."),
    "claude-desktop.md": ("claude-desktop", "One-click Galaxy connection for Claude Desktop, no terminal required."),
    "codex.md": ("codex", "Install the Galaxy MCP server and skills into OpenAI Codex CLI."),
    "cursor.md": ("cursor", "Add the Galaxy MCP server and skills to Cursor, with a one-click link."),
    "antigravity.md": ("antigravity", "Install the Galaxy plugins into Google Antigravity (agy CLI and IDE)."),
    "pi.md": ("pi", "Add the Galaxy MCP server and skills to the Pi coding agent."),
}

LANDING = f"""---
title: "Galaxy for AI Coding Agents"
tease: "Connect Claude Code, Claude Desktop, Codex, Cursor, Antigravity or Pi to your Galaxy server, and give the agent curated Galaxy skills."
subsites: [all]
autotoc: true
---

AI coding agents can drive Galaxy directly: list your histories, upload data,
search and run tools, and invoke workflows on any Galaxy server you have an
account on. The [galaxyproject/agentic-plugins]({REPO_URL}) repository
packages everything needed for that as plugins for the common agent harnesses.
One install gives an agent three things:

1. **A Galaxy connection** through the [galaxy-mcp](https://github.com/galaxyproject/galaxy-mcp)
   server, authenticated with your Galaxy API key.
2. **Curated Galaxy skills** from [galaxy-skills](https://github.com/galaxyproject/galaxy-skills):
   tool development, user-defined tools, Nextflow conversion, dataset
   collections, workflow reports, track hubs, hub posts and MCP usage.
3. **Galaxy Workflow Foundry skills** from [foundry](https://github.com/galaxyproject/foundry):
   turning papers, Nextflow pipelines and CWL workflows into validated Galaxy
   workflows.

<div class="callout">
Looking for a complete AI research assistant built around Galaxy rather than a
plugin for the agent you already use? See <a href="/tools/orbit/">Orbit</a>.
</div>

## Pick your agent

| Agent | Guide | What you get |
|-------|-------|--------------|
| Claude Code | [Set up Claude Code]({HUB_BASE}/claude-code/) | MCP server (prompts for URL and key at install) + skills, via `/plugin` |
| Claude Desktop | [Set up Claude Desktop]({HUB_BASE}/claude-desktop/) | One-click `.mcpb` bundle; MCP server only |
| Codex CLI | [Set up Codex]({HUB_BASE}/codex/) | MCP server + skills via `codex plugin` |
| Cursor | [Set up Cursor]({HUB_BASE}/cursor/) | MCP server + skills via Customize, or a one-click MCP link |
| Antigravity (`agy`) | [Set up Antigravity]({HUB_BASE}/antigravity/) | MCP server + skills via `agy plugin install` |
| Pi | [Set up Pi]({HUB_BASE}/pi/) | MCP server (through pi-mcp-adapter) + skills via `pi install` |

Every guide starts with [getting a Galaxy API key]({HUB_BASE}/api-key/).
Other agents that read Agent Skills from `~/.agents/skills/` can use the skills
by cloning [galaxy-skills](https://github.com/galaxyproject/galaxy-skills)
there and adding the MCP server by hand with `uvx galaxy-mcp`.

## Before you start

- **A Galaxy account** on the server you want to use (for example
  [usegalaxy.org](https://usegalaxy.org), [usegalaxy.eu](https://usegalaxy.eu)
  or [usegalaxy.org.au](https://usegalaxy.org.au)) and its API key.
- **[uv](https://docs.astral.sh/uv/)** on your `PATH` for every harness except
  Claude Desktop; the MCP server runs as `uvx galaxy-mcp`.
- An API key gives full access to your account. Keep it in configuration or an
  environment variable, not in chat.

## What the agent can do once connected

Ask in plain language; the agent picks the Galaxy tools:

- *"Show my recent histories and what's in the latest one."*
- *"Upload these FASTQ files to a new history called 'run 12' and run FastQC on them."*
- *"Find an IWC workflow for variant calling on paired-end reads and run it on history X."*
- *"Convert this Nextflow process into a Galaxy tool wrapper and test it with Planemo."* (uses the `nf-to-galaxy` and `tool-dev` skills from `galaxy-dev-skills`)
- *"Build a Galaxy workflow from this paper's methods section."* (uses the Foundry skills)

## Get help

- Something not working? The `galaxy-connect` skill that ships with the MCP
  plugin walks the agent through diagnosing the connection; each guide has a
  troubleshooting section.
- Issues and contributions: [galaxyproject/agentic-plugins]({REPO_URL}).
- Skill content lives upstream in [galaxy-skills](https://github.com/galaxyproject/galaxy-skills)
  and [foundry](https://github.com/galaxyproject/foundry); the plugins mirror
  them weekly.
"""


def convert(md: str, slug: str, tease: str) -> str:
    lines = md.splitlines()
    assert lines[0].startswith("# "), f"{slug}: expected H1 first"
    title = lines[0][2:].strip()
    body = "\n".join(lines[1:]).strip("\n")
    # drop repo-internal sections (build/submission notes) from the hub copy
    body = re.sub(r"\n## For maintainers[^\n]*\n.*?(?=\n## |\Z)", "\n", body, flags=re.S).rstrip("\n")
    # links between docs -> hub URLs
    for src, (dst_slug, _) in PAGES.items():
        body = body.replace(f"({src})", f"({HUB_BASE}/{dst_slug}/)")
    # repo-relative links (../plugins/..., bundles/...) -> GitHub
    body = re.sub(r"\]\((?:\.\./)+([^)]+)\)", rf"]({REPO_URL}/blob/main/\1)", body)
    fm = f'---\ntitle: "{title}"\ntease: "{tease}"\nsubsites: [all]\nautotoc: true\n---\n\n'
    return fm + body + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1]).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.md").write_text(LANDING)
    print(f"wrote {out / 'index.md'}")
    for src, (slug, tease) in PAGES.items():
        page = out / slug
        page.mkdir(exist_ok=True)
        (page / "index.md").write_text(convert((DOCS / src).read_text(), slug, tease))
        print(f"wrote {page / 'index.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
