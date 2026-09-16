#!/usr/bin/env python3
"""Regenerate the generated parts of the plugin manifests.

Hand-written fields are preserved; only these are rewritten:
  * plugins/<mirror>/.claude-plugin/plugin.json  -> "skills" (nested skill dirs) and "version"
  * plugins/<mirror>/.codex-plugin/plugin.json   -> "version"
  * plugins/<mirror>/.cursor-plugin/plugin.json  -> "version"
  * .cursor-plugin/marketplace.json              -> per-plugin "version"
  * bundles/claude-desktop/manifest.json         -> "version" (= galaxy-mcp plugin version)
  * .claude-plugin/marketplace.json              -> per-plugin "version"
  * package.json                                 -> "pi.skills" (all skill roots incl. nested) and "version"

Mirror plugin versions are CalVer derived from UPSTREAM.json synced_at (YYYY.M.D).
Nested skills (a SKILL.md deeper than skills/<name>/) must be listed explicitly for
Claude Code (one level deep only) and Pi (stops recursing at a skill root).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
MIRRORS = ["galaxy-skills", "foundry-skills"]
ALL_PLUGINS = ["galaxy-mcp", *MIRRORS]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def skill_dirs(skills_root: Path) -> list[Path]:
    """All directories containing a SKILL.md, relative to skills_root, sorted."""
    return sorted(p.parent.relative_to(skills_root) for p in skills_root.rglob("SKILL.md"))


def nested_skill_dirs(skills_root: Path) -> list[Path]:
    return [d for d in skill_dirs(skills_root) if len(d.parts) > 1]


def calver(plugin: str) -> str:
    up = load(PLUGINS / plugin / "UPSTREAM.json")
    y, m, d = up["synced_at"][:10].split("-")
    return f"{int(y)}.{int(m)}.{int(d)}"


def main() -> int:
    versions: dict[str, str] = {}
    for plugin in ALL_PLUGINS:
        pdir = PLUGINS / plugin
        claude = pdir / ".claude-plugin" / "plugin.json"
        codex = pdir / ".codex-plugin" / "plugin.json"
        cursor = pdir / ".cursor-plugin" / "plugin.json"
        if plugin in MIRRORS:
            version = calver(plugin)
            nested = [f"./skills/{d.as_posix()}" for d in nested_skill_dirs(pdir / "skills")]
            data = load(claude)
            data["version"] = version
            data["skills"] = nested
            dump(claude, data)
            for manifest in (codex, cursor):
                data = load(manifest)
                data["version"] = version
                dump(manifest, data)
        else:
            version = load(claude)["version"]
        versions[plugin] = version
        print(f"{plugin}: version {version}")

    # Claude and Cursor marketplace versions
    for mp_path in (ROOT / ".claude-plugin" / "marketplace.json", ROOT / ".cursor-plugin" / "marketplace.json"):
        mp = load(mp_path)
        for entry in mp["plugins"]:
            if entry["name"] in versions:
                entry["version"] = versions[entry["name"]]
        dump(mp_path, mp)

    # Claude Desktop bundle follows the galaxy-mcp plugin version
    bundle = ROOT / "bundles" / "claude-desktop" / "manifest.json"
    data = load(bundle)
    data["version"] = versions["galaxy-mcp"]
    dump(bundle, data)

    # Pi package: every skill root, nested ones explicitly
    pkg_path = ROOT / "package.json"
    pkg = load(pkg_path)
    pi_skills: list[str] = []
    for plugin in ALL_PLUGINS:
        skills_root = PLUGINS / plugin / "skills"
        pi_skills.append(f"./plugins/{plugin}/skills")
        pi_skills += [f"./plugins/{plugin}/skills/{d.as_posix()}" for d in nested_skill_dirs(skills_root)]
    pkg["pi"]["skills"] = pi_skills
    pkg["version"] = max((versions[m] for m in MIRRORS), key=lambda v: tuple(int(x) for x in v.split(".")))
    dump(pkg_path, pkg)
    print(f"package.json: version {pkg['version']}, {len(pi_skills)} pi skill roots")
    return 0


if __name__ == "__main__":
    sys.exit(main())
