# Galaxy for Codex CLI

Connects [OpenAI Codex CLI](https://developers.openai.com/codex/cli) to Galaxy
with the `galaxy-mcp` server (48 Galaxy tools) and curated `galaxy-skills`.

## Step A · Get your Galaxy API key, request UDT access, and export credentials

1. **API key:** Log in to [usegalaxy.org](https://usegalaxy.org) (or
   [usegalaxy.eu](https://usegalaxy.eu), [usegalaxy.org.au](https://usegalaxy.org.au),
   or your institution's server) → **User › Preferences › Manage API Key** →
   **Create a new key** → copy it.
2. **User-Defined Tools beta (UseGalaxy.org):** Submit the 30-second form at
   **[udt-signup.galaxyproject.org](https://udt-signup.galaxyproject.org/)**
   with your UseGalaxy.org email *(optional ORCID sign-in speeds review)*. Basic
   tools and workflows work immediately while we approve UDT access.
3. **Export credentials:** Codex forwards `GALAXY_URL` (no `/api`) and
   `GALAXY_API_KEY` from your shell. Add both to `~/.zshrc` or `~/.bashrc` (then
   open a new terminal), or place them in a project `.env` file (gitignored):

   ```bash
   export GALAXY_URL="https://usegalaxy.org"
   export GALAXY_API_KEY="paste-your-key-here"
   ```

## Step B · Install in Codex CLI

**Needs:** Codex CLI (`codex --version`) and [uv](https://docs.astral.sh/uv/) on
your `PATH` (`uv --version`).

```bash
codex plugin marketplace add galaxyproject/agentic-plugins
codex plugin add galaxy-mcp@galaxyproject
codex plugin add galaxy-skills@galaxyproject
```

**Start a new `codex` session afterwards.**

Building Galaxy XML wrappers or Workflow Foundry casts? Add only what you need
(every installed skill adds to per-turn context):

```bash
codex plugin add galaxy-dev-skills@galaxyproject
codex plugin add foundry-skills@galaxyproject
```

## Step C · Verify and run

1. Run `codex mcp list` (or `/mcp` inside Codex — `galaxy` shows `enabled`),
   then ask:

   ```
   Connect to Galaxy and tell me who I am.
   ```

   Approve the MCP tool prompt on first use — Codex calls `get_user` and reports
   your Galaxy username and account details. *(If anything fails, type
   `$galaxy-connect`.)*
2. Ask in plain language — upload FASTQs, run IWC workflows, write in-Galaxy
   JupyterLite (`gxy`) notebooks, rebuild scratch histories (`$reproduciblify`),
   or author containerized UDTs (`$udt-authoring`).

<details>
<summary>Skills, updates, and removing plugins</summary>

### Use the skills

Codex picks skills automatically from your prompt, or you can invoke them with
`$` (or `/skills`): `$galaxy-connect`, `$galaxy-integration`,
`$jupyterlite-galaxy`, `$galaxy-mcp-reference`, `$collection-manipulation`,
`$udt-authoring`, `$workflow-reports`, `$reproduciblify` (plus `$tool-dev` and
`$nf-to-galaxy` if `galaxy-dev-skills` is installed).

### Update or remove

```bash
codex plugin marketplace upgrade
codex plugin add galaxy-mcp@galaxyproject
codex plugin add galaxy-skills@galaxyproject
```

Remove any plugin with `codex plugin remove <name>@galaxyproject`.

</details>

<details>
<summary>Manual MCP setup and troubleshooting</summary>

### Register `galaxy-mcp` without the plugin

Add to `~/.codex/config.toml` (forwards variables from your shell without writing
your key to disk):

```toml
[mcp_servers.galaxy]
command = "uvx"
args = ["galaxy-mcp"]
env_vars = ["GALAXY_URL", "GALAXY_API_KEY"]
```

### Troubleshooting

- **No `galaxy` server in `/mcp`**: start a new Codex session; verify `uv --version`.
- **"Missing Galaxy URL and API key"**: variables were not exported in the shell that launched Codex (common with GUI launchers). Put `GALAXY_URL` and `GALAXY_API_KEY` in a project `.env` file or export them before running `codex`.
- **Server fails to start**: run `uvx galaxy-mcp` in a terminal to see the underlying error.
- **"Provided API key is not valid"**: the key belongs to a different Galaxy server or was revoked.

</details>
