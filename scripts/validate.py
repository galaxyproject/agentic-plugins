#!/usr/bin/env python3
"""Structural checks for this repository (run in CI and by sync-skills.sh).

Exit code 1 on any failure. Checks:
  * every JSON manifest parses
  * marketplace entries point at existing plugin dirs whose manifests agree on name/version
  * every SKILL.md has frontmatter with name and description
  * Claude plugin.json "skills" entries and package.json "pi.skills" entries exist and hold a SKILL.md
    (pi entries may also be parent directories)
  * no plugin has a root .mcp.json (it would be auto-loaded twice next to the per-harness files)
  * mirror plugins have UPSTREAM.json and their generated manifests are up to date
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml  # optional: enables strict frontmatter warnings
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        err(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        return None


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def check_skill(skill_md: Path) -> None:
    text = skill_md.read_text(errors="replace")
    m = FRONTMATTER.match(text)
    rel = skill_md.relative_to(ROOT)
    if not m:
        err(f"{rel}: missing YAML frontmatter")
        return
    fm = m.group(1)
    for key in ("name", "description"):
        if not re.search(rf"^{key}:\s*\S", fm, re.M):
            err(f"{rel}: frontmatter lacks '{key}'")
    if yaml is not None:
        try:
            yaml.safe_load(fm)
        except Exception as exc:  # noqa: BLE001
            first = str(exc).splitlines()[0]
            warnings.append(f"{rel}: frontmatter is not strict YAML ({first}); Claude Code and Codex skip such skills. Fix upstream.")


def main() -> int:
    # Marketplaces
    claude_mp = load(ROOT / ".claude-plugin" / "marketplace.json") or {}
    codex_mp = load(ROOT / ".agents" / "plugins" / "marketplace.json") or {}
    pkg = load(ROOT / "package.json") or {}

    plugin_dirs = sorted(p for p in PLUGINS.iterdir() if p.is_dir())
    names = {p.name for p in plugin_dirs}

    for entry in claude_mp.get("plugins", []):
        src = Path(entry["source"])
        pdir = (ROOT / src).resolve()
        if not pdir.is_dir():
            err(f"claude marketplace: {entry['name']} source {src} missing")
            continue
        man = load(pdir / ".claude-plugin" / "plugin.json") or {}
        if man.get("name") != entry["name"]:
            err(f"claude marketplace: entry {entry['name']} vs plugin.json name {man.get('name')}")
        if man.get("version") != entry.get("version"):
            err(f"claude marketplace: {entry['name']} version {entry.get('version')} != plugin.json {man.get('version')}")
    for entry in codex_mp.get("plugins", []):
        pdir = (ROOT / entry["source"]["path"]).resolve()
        if not pdir.is_dir():
            err(f"codex marketplace: {entry['name']} path missing")
            continue
        man = load(pdir / ".codex-plugin" / "plugin.json") or {}
        if man.get("name") != entry["name"]:
            err(f"codex marketplace: entry {entry['name']} vs plugin.json name {man.get('name')}")
    mp_names = {e["name"] for e in claude_mp.get("plugins", [])}
    if mp_names != names:
        err(f"claude marketplace lists {sorted(mp_names)} but plugins/ has {sorted(names)}")

    # Plugins
    for pdir in plugin_dirs:
        rel = pdir.relative_to(ROOT)
        for manifest in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "plugin.json"):
            if not (pdir / manifest).is_file():
                err(f"{rel}: missing {manifest}")
        if (pdir / ".mcp.json").exists():
            err(f"{rel}: root .mcp.json present; use mcp/<harness>.json instead")
        agy = load(pdir / "plugin.json") or {}
        if agy.get("name") != pdir.name:
            err(f"{rel}/plugin.json: name {agy.get('name')} != directory name")
        if "agent-plugins.org" in str(agy.get("$schema", "")):
            # Codex would then treat the root plugin.json as an Agent Plugins manifest and
            # switch to direct-children skill discovery, hiding nested skills.
            err(f"{rel}/plugin.json: must not declare an agent-plugins.org $schema")
        codex = load(pdir / ".codex-plugin" / "plugin.json") or {}
        if not re.fullmatch(r"\d+\.\d+\.\d+([-+][0-9A-Za-z.-]+)?", str(codex.get("version"))):
            err(f"{rel}/.codex-plugin/plugin.json: version must be strict semver")
        for key in ("description", "author", "interface"):
            if key not in codex:
                err(f"{rel}/.codex-plugin/plugin.json: missing {key}")
        for mcp_key in ("mcpServers",):
            for man in (codex, load(pdir / ".claude-plugin" / "plugin.json") or {}):
                ref = man.get(mcp_key)
                if isinstance(ref, str) and not (pdir / ref).is_file():
                    err(f"{rel}: {mcp_key} file {ref} missing")
        for f in pdir.glob("mcp/*.json"):
            load(f)
        if (pdir / "mcp_config.json").exists():
            load(pdir / "mcp_config.json")

        skills_root = pdir / "skills"
        skill_mds = sorted(skills_root.rglob("SKILL.md")) if skills_root.is_dir() else []
        if not skill_mds:
            err(f"{rel}: no skills found under skills/")
        for s in skill_mds:
            check_skill(s)

        claude = load(pdir / ".claude-plugin" / "plugin.json") or {}
        for entry in claude.get("skills", []) or []:
            if not (pdir / entry / "SKILL.md").is_file():
                err(f"{rel}/.claude-plugin/plugin.json: skills entry {entry} has no SKILL.md")

        if pdir.name != "galaxy-mcp":
            up = load(pdir / "UPSTREAM.json")
            if not up or "commit" not in up:
                err(f"{rel}: UPSTREAM.json missing or incomplete")

    # Pi package
    for entry in pkg.get("pi", {}).get("skills", []):
        p = ROOT / entry
        if not p.is_dir():
            err(f"package.json pi.skills: {entry} is not a directory")
        elif not any(p.rglob("SKILL.md")):
            err(f"package.json pi.skills: {entry} contains no SKILL.md")
    mcp_ref = pkg.get("pi", {}).get("mcp")
    if mcp_ref and not (ROOT / mcp_ref).is_file():
        err(f"package.json pi.mcp: {mcp_ref} missing")

    # Generated manifests up to date?
    before = {p: p.read_text() for p in [
        ROOT / "package.json", ROOT / ".claude-plugin" / "marketplace.json",
        *ROOT.glob("plugins/*/.claude-plugin/plugin.json"), *ROOT.glob("plugins/*/.codex-plugin/plugin.json"),
    ]}
    subprocess.run([sys.executable, str(ROOT / "scripts" / "gen-manifests.py")], check=True, capture_output=True)
    for p, text in before.items():
        if p.read_text() != text:
            err(f"{p.relative_to(ROOT)}: out of date; run scripts/gen-manifests.py")
            p.write_text(text)  # leave the tree as we found it

    for w in warnings:
        print(f"warning: {w}")
    if errors:
        print("validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    n_skills = len(list(PLUGINS.rglob("SKILL.md")))
    print(f"validation OK ({len(plugin_dirs)} plugins, {n_skills} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
