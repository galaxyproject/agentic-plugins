# Galaxy for Antigravity

## Step 1 · Get your Galaxy API key and export it

- **Galaxy API key:** On [usegalaxy.org](https://usegalaxy.org) *(or [usegalaxy.eu](https://usegalaxy.eu) / [usegalaxy.org.au](https://usegalaxy.org.au))*, open **User › Preferences › Manage API Key** → **Create a new key**.
- **Custom tools on UseGalaxy.org *(optional)*:** Request [User-Defined Tools beta access](https://udt-signup.galaxyproject.org/) (~30s). Standard tools work immediately while we approve.
- **Export in `~/.zshrc` / `~/.bashrc`** *(or put in a workspace `.env` when launching the Antigravity IDE from the Dock)*:

```bash
export GALAXY_URL="https://usegalaxy.org"
export GALAXY_API_KEY="paste-your-key-here"
```

## Step 2 · Install the Galaxy plugins

Requires [Antigravity](https://antigravity.google) (`agy` CLI or IDE), [uv](https://docs.astral.sh/uv/), and `git`:

```bash
git clone https://github.com/galaxyproject/agentic-plugins.git ~/.galaxy-agentic-plugins
agy plugin install ~/.galaxy-agentic-plugins/plugins/galaxy-mcp
agy plugin install ~/.galaxy-agentic-plugins/plugins/galaxy-skills
```

**Start a new session afterwards.**

## Step 3 · Verify and run

Check `/mcp` shows `galaxy-mcp_galaxy` **running**, then ask:

```
Connect to Galaxy and tell me who I am.
```

Antigravity calls `get_user` and confirms your account. Then ask in plain language — upload reads, run IWC workflows, write JupyterLite (`gxy`) notebooks, rebuild histories (`/reproduciblify`), or author containerized YAML tools (`/udt-authoring`).

<details>
<summary>Optional developer skills, manual config, updates & troubleshooting</summary>

### Optional plugins & updates

```bash
agy plugin install ~/.galaxy-agentic-plugins/plugins/galaxy-dev-skills
agy plugin install ~/.galaxy-agentic-plugins/plugins/foundry-skills
```

Update anytime with `git -C ~/.galaxy-agentic-plugins pull` and re-run `agy plugin install ...`. Inspect with `agy plugin list` or remove with `agy plugin uninstall <name>`.

### Manual MCP setup & troubleshooting

```bash
agy mcp add --env GALAXY_URL=https://usegalaxy.org \
            --env GALAXY_API_KEY="$GALAXY_API_KEY" \
            galaxy uvx galaxy-mcp
```

- **Missing URL / key in the GUI IDE:** Dock launches often skip `~/.zshrc`; add `GALAXY_URL` and `GALAXY_API_KEY` to your workspace `.env` or use `agy mcp add --env` above (do not install `galaxy-mcp` plugin at the same time).
- **Connection check:** run `/galaxy-connect` or test `uvx galaxy-mcp` in a terminal.

</details>
