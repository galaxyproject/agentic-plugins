# Galaxy for Codex CLI

## Step 1 · Get your Galaxy API key and export it

- **Galaxy API key:** On [usegalaxy.org](https://usegalaxy.org) *(or [usegalaxy.eu](https://usegalaxy.eu) / [usegalaxy.org.au](https://usegalaxy.org.au))*, open **User › Preferences › Manage API Key** → **Create a new key**.
- **Custom tools on UseGalaxy.org *(optional)*:** Request [User-Defined Tools beta access](https://udt-signup.galaxyproject.org/) (~30s). Standard tools work immediately while we approve.
- **Export in your shell** (`~/.zshrc` / `~/.bashrc`, then open a new terminal — or put in a gitignored `.env`):

```bash
export GALAXY_URL="https://usegalaxy.org"
export GALAXY_API_KEY="paste-your-key-here"
```

## Step 2 · Install the Galaxy plugins

Requires [Codex CLI](https://developers.openai.com/codex/cli) and [uv](https://docs.astral.sh/uv/) (`uv --version`):

```bash
codex plugin marketplace add galaxyproject/agentic-plugins
codex plugin add galaxy-mcp@galaxyproject
codex plugin add galaxy-skills@galaxyproject
```

**Start a new `codex` session afterwards.**

## Step 3 · Verify and run

Ask Codex (approve the one-time MCP prompt on first call):

```
Connect to Galaxy and tell me who I am.
```

Codex calls `get_user` and confirms your account. Then ask in plain language — upload reads, run IWC workflows, write JupyterLite (`gxy`) notebooks, rebuild histories (`$reproduciblify`), or author containerized YAML tools (`$udt-authoring`).

<details>
<summary>Optional developer skills, manual config, updates & troubleshooting</summary>

### Optional plugins (tool wrappers & workflow engineering)

```bash
codex plugin add galaxy-dev-skills@galaxyproject
codex plugin add foundry-skills@galaxyproject
```

### Direct `$skill` invocation & updates

Invoke any skill with `$` (e.g. `$galaxy-connect`, `$udt-authoring`, `$reproduciblify`, `$collection-manipulation`). Update with `codex plugin marketplace upgrade` then re-run `codex plugin add ...`; remove with `codex plugin remove <name>@galaxyproject`.

### Manual `~/.codex/config.toml` & troubleshooting

```toml
[mcp_servers.galaxy]
command = "uvx"
args = ["galaxy-mcp"]
env_vars = ["GALAXY_URL", "GALAXY_API_KEY"]
```

- **Missing URL / key error:** confirm `GALAXY_URL` (no `/api`) and `GALAXY_API_KEY` are exported in the shell that launched `codex`, or place them in `.env`.
- **No `galaxy` in `codex mcp list`:** start a new session and verify `uv --version`.

</details>
