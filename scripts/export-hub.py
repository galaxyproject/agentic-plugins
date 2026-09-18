#!/usr/bin/env python3
"""Export docs/ as the Galaxy Hub page /tools/ai-agents/ (galaxyproject/galaxy-hub).

Usage: scripts/export-hub.py <hub-content-dir>/tools/ai-agents

Writes ONE page, index.md, that combines:
  - the landing template below (hero + animated shells via <AgentShells />),
  - docs/galaxy-api-key.md as the "Get a Galaxy API key" section,
  - every harness doc as a <HarnessGuide> panel inside <HarnessGuides>,
plus a redirect stub for each old per-harness URL (<slug>/index.md ->
/tools/ai-agents/#guide-<slug>) so existing links keep working.

The docs remain the source of truth; rerun after editing them. Links between
docs become in-page anchors, repo-relative links become GitHub URLs, each H1 is
dropped (the panel supplies the title) and section headings are demoted so the
page outline stays h1 > h2 > h3 > h4. The page carries `generated_from`, and
each panel links back to the docs file it was built from.

The tab strip on the hub is rendered from the agent-shells scene list, so the
set of GUIDES here must match `scenes` in galaxy-hub
(astro/src/components/agent-shells/scenes.ts): same ids, same order.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO_URL = "https://github.com/galaxyproject/agentic-plugins"
HUB_BASE = "/tools/ai-agents"

API_KEY_DOC = "galaxy-api-key.md"
API_KEY_ANCHOR = "#get-a-galaxy-api-key"

GUIDES = [  # (docs file, hub id, display name) — order and ids match scenes.ts
    ("claude-code.md", "claude-code", "Claude Code"),
    ("codex.md", "codex", "Codex CLI"),
    ("antigravity.md", "antigravity", "Antigravity"),
    ("pi.md", "pi", "Pi"),
    ("claude-desktop.md", "claude-desktop", "Claude Desktop"),
    # held back from the hub for now; re-enable together with the Cursor scene in galaxy-hub
    # ("cursor.md", "cursor", "Cursor"),
]

# Old per-page slugs that now redirect into the single page.
REDIRECTS = {"api-key": API_KEY_ANCHOR, **{gid: f"#guide-{gid}" for _, gid, _ in GUIDES}}

LANDING = f"""---
title: "Galaxy for AI Coding Agents"
tease: "Connect Claude Code, Codex, Antigravity or Pi to your Galaxy server with curated Galaxy skills, or Claude Desktop with the Galaxy connection alone."
subsites: [all]
components: true
autotoc: false
skip_title_render: true
full_bleed: true
og_image: /images/galaxy-logos/galaxy_logo_25percent.png
generated_from: {REPO_URL}/blob/main/scripts/export-hub.py
---

<AgentShells />

Galaxy for AI coding agents installs the galaxy-mcp server, the galaxy-skills
and galaxy-dev-skills sets and the Workflow Foundry skills into Claude Code,
Codex, Antigravity or Pi; Claude Desktop gets the galaxy-mcp server as a
one-click bundle. Everything comes from the
[galaxyproject/agentic-plugins]({REPO_URL})
repository, and everything you need is on this page: get an API key, then pick
your harness under [Set up your agent](#set-up-your-agent).

<div class="callout">
Looking for a complete AI research assistant built around Galaxy rather than a
plugin for the agent you already use? See <a href="/tools/orbit/">Orbit</a>.
</div>

## Before you start

- **A Galaxy account** on the server you want to use (for example
  [usegalaxy.org](https://usegalaxy.org), [usegalaxy.eu](https://usegalaxy.eu)
  or [usegalaxy.org.au](https://usegalaxy.org.au)) and its API key.
- **[uv](https://docs.astral.sh/uv/)** on your `PATH` for every harness except
  Claude Desktop; the MCP server runs as `uvx galaxy-mcp`.
- **`git`** for the Antigravity install and **Node.js** for Pi; each guide lists
  its own prerequisites.
- An API key gives full access to your account. Keep it in configuration or an
  environment variable, not in chat.

## Get a Galaxy API key

%%API_KEY%%

## Set up your agent

Pick your harness. Each guide covers install, credentials, verification, the
skills, updates, alternatives and troubleshooting. Other agents that read Agent
Skills from `~/.agents/skills/` can use the skills by cloning
[galaxy-skills](https://github.com/galaxyproject/galaxy-skills) there and
adding the MCP server by hand with `uvx galaxy-mcp`.

<HarnessGuides>

%%GUIDES%%

</HarnessGuides>

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


def body_of(md: str, src: str, shift: int) -> str:
    """Doc body for embedding: no H1, links rewritten, headings demoted by `shift`."""
    lines = md.splitlines()
    assert lines[0].startswith("# "), f"{src}: expected H1 first"
    body = "\n".join(lines[1:]).strip("\n")
    # drop repo-internal sections (build/submission notes) from the hub copy
    body = re.sub(r"\n## For maintainers[^\n]*\n.*?(?=\n## |\Z)", "\n", body, flags=re.S).rstrip("\n")
    # links between docs -> in-page anchors
    body = body.replace(f"({API_KEY_DOC})", f"({API_KEY_ANCHOR})")
    for doc, gid, _ in GUIDES:
        body = body.replace(f"({doc})", f"(#guide-{gid})")
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
    # blank lines around the body keep MDX parsing it as markdown
    return f'<HarnessGuide id="{gid}" name="{name}" source="{source}">\n\n{body}\n\n</HarnessGuide>'


def landing() -> str:
    api_key = body_of((DOCS / API_KEY_DOC).read_text(), API_KEY_DOC, shift=1)
    guides = "\n\n".join(guide_panel(*g) for g in GUIDES)
    return LANDING.replace("%%API_KEY%%", api_key).replace("%%GUIDES%%", guides)


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1]).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.md").write_text(landing())
    print(f"wrote {out / 'index.md'}")
    for slug, anchor in REDIRECTS.items():
        page = out / slug
        page.mkdir(exist_ok=True)
        (page / "index.md").write_text(f'---\nredirect: "{HUB_BASE}/{anchor}"\n---\n')
        print(f"wrote {page / 'index.md'} -> {HUB_BASE}/{anchor}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
