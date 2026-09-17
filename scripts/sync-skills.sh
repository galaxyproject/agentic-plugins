#!/usr/bin/env bash
# Vendor upstream skills into plugins/galaxy-skills and plugins/foundry-skills,
# record the pinned commits in UPSTREAM.json, then regenerate manifests.
#
# Usage: scripts/sync-skills.sh
# Env:   GALAXY_SKILLS_REF (default main), FOUNDRY_REF (default main)
#        Each may be a branch, tag or full commit SHA.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
GALAXY_SKILLS_REPO=${GALAXY_SKILLS_REPO:-https://github.com/galaxyproject/galaxy-skills.git}
GALAXY_SKILLS_REF=${GALAXY_SKILLS_REF:-main}
FOUNDRY_REPO=${FOUNDRY_REPO:-https://github.com/galaxyproject/foundry.git}
FOUNDRY_REF=${FOUNDRY_REF:-main}
FOUNDRY_SKILLS_PATH=casts/claude/skills

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# clone_ref <repo> <ref> <dest> [sparse paths...]
clone_ref() {
  local repo=$1 ref=$2 dest=$3; shift 3
  local sparse=("$@")
  if [[ $ref =~ ^[0-9a-f]{40}$ ]]; then
    git init -q "$dest"
    git -C "$dest" remote add origin "$repo"
    if ((${#sparse[@]})); then
      git -C "$dest" config core.sparseCheckout true
      git -C "$dest" sparse-checkout set --no-cone "${sparse[@]}" 2>/dev/null || printf '%s\n' "${sparse[@]}" > "$dest/.git/info/sparse-checkout"
    fi
    git -C "$dest" fetch -q --depth 1 --filter=blob:none origin "$ref"
    git -C "$dest" checkout -q FETCH_HEAD
  else
    if ((${#sparse[@]})); then
      git clone -q --depth 1 --branch "$ref" --filter=blob:none --sparse "$repo" "$dest"
      git -C "$dest" sparse-checkout set --no-cone "${sparse[@]}"
    else
      git clone -q --depth 1 --branch "$ref" "$repo" "$dest"
    fi
  fi
}

write_upstream() {
  local file=$1 repo=$2 ref=$3 sha=$4 path=$5
  python3 - "$file" "$repo" "$ref" "$sha" "$path" <<'PY'
import json, sys, datetime
file, repo, ref, sha, path = sys.argv[1:]
json.dump({
    "repository": repo.removesuffix(".git"),
    "ref": ref,
    "commit": sha,
    "path": path,
    "synced_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}, open(file, "w"), indent=2)
open(file, "a").write("\n")
PY
}

echo "==> galaxy-skills @ $GALAXY_SKILLS_REF"
clone_ref "$GALAXY_SKILLS_REPO" "$GALAXY_SKILLS_REF" "$TMP/galaxy-skills"
gs_sha=$(git -C "$TMP/galaxy-skills" rev-parse HEAD)

# Upstream keeps two trees: skills/ is for *using* Galaxy, dev-skills/ is for *building*
# it, and no harness scans dev-skills/. Each tree becomes its own plugin here so that
# installing one doesn't drag in the other. Vendoring the repo root instead would bury
# every skill a level deeper and register both trees as one bundle.
# vendor_tree <plugin> <upstream subdir>
vendor_tree() {
  local plugin=$1 subdir=$2
  local src="$TMP/galaxy-skills/$subdir" dest="$ROOT/plugins/$plugin/skills"
  if [ ! -d "$src" ]; then
    echo "ERROR: upstream has no $subdir/ -- layout changed, see galaxyproject/galaxy-skills#35" >&2
    exit 1
  fi
  rm -rf "$dest"; mkdir -p "$dest"
  rsync -a "$src/" "$dest/"
  if [ -f "$TMP/galaxy-skills/LICENSE" ]; then
    cp "$TMP/galaxy-skills/LICENSE" "$dest/LICENSE"
  fi
  write_upstream "$ROOT/plugins/$plugin/UPSTREAM.json" "$GALAXY_SKILLS_REPO" "$GALAXY_SKILLS_REF" "$gs_sha" "$subdir"
  echo "    $plugin @ $gs_sha ($(find "$dest" -name SKILL.md | wc -l | tr -d ' ') skills)"
}

vendor_tree galaxy-skills skills
vendor_tree galaxy-dev-skills dev-skills

echo "==> foundry @ $FOUNDRY_REF ($FOUNDRY_SKILLS_PATH)"
clone_ref "$FOUNDRY_REPO" "$FOUNDRY_REF" "$TMP/foundry" "/$FOUNDRY_SKILLS_PATH/" "/LICENSE"
f_sha=$(git -C "$TMP/foundry" rev-parse HEAD)
dest="$ROOT/plugins/foundry-skills/skills"
rm -rf "$dest"; mkdir -p "$dest"
rsync -a "$TMP/foundry/$FOUNDRY_SKILLS_PATH/" "$dest/"
[ -f "$TMP/foundry/LICENSE" ] && cp "$TMP/foundry/LICENSE" "$dest/LICENSE"
write_upstream "$ROOT/plugins/foundry-skills/UPSTREAM.json" "$FOUNDRY_REPO" "$FOUNDRY_REF" "$f_sha" "$FOUNDRY_SKILLS_PATH"
echo "    $f_sha ($(find "$dest" -name SKILL.md | wc -l | tr -d ' ') skills)"

echo "==> regenerating manifests"
python3 "$ROOT/scripts/gen-manifests.py"
echo "==> validating"
python3 "$ROOT/scripts/validate.py"
echo "done"
