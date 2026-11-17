# Galaxy for Antigravity

Connects Google [Antigravity](https://antigravity.google) (`agy` CLI and IDE,
sharing `~/.gemini/config/`) to Galaxy with the `galaxy-mcp` server (48 Galaxy
tools) and curated `galaxy-skills`.

## Step A · Get your Galaxy API key, request UDT access, and export credentials

1. **API key:** Log in to [usegalaxy.org](https://usegalaxy.org) (or
   [usegalaxy.eu](https://usegalaxy.eu), [usegalaxy.org.au](https://usegalaxy.org.au),
   or your institution's server) → **User › Preferences › Manage API Key** →
   **Create a new key** → copy it.
2. **User-Defined Tools beta (UseGalaxy.org):** Submit the 30-second form at
   **[udt-signup.galaxyproject.org](https://udt-signup.galaxyproject.org/)**
   with your UseGalaxy.org email *(optional ORCID sign-in speeds review)*. Basic
   tools and workflows work immediately while we approve UDT access.
3. **Export credentials:** Add both variables to `~/.zshrc` or `~/.bashrc` (then
   open a new terminal), or place them in a workspace `.env` file (recommended
   when launching the Antigravity IDE from the Dock, which may not read
   `~/.zshrc`):

   ```bash
   export GALAXY_URL="https://usegalaxy.org"
   export GALAXY_API_KEY="paste-your-key-here"
   ```

## Step B · Install in Antigravity

**Needs:** Antigravity (`agy --version` or IDE), [uv](https://docs.astral.sh/uv/)
on your `PATH`, and `git`.

```bash
git clone https://github.com/galaxyproject/agentic-plugins.git ~/.galaxy-agentic-plugins
agy plugin install ~/.galaxy-agentic-plugins/plugins/galaxy-mcp
agy plugin install ~/.galaxy-agentic-plugins/plugins/galaxy-skills
```

**Start a new session afterwards.**

Building Galaxy XML wrappers or Workflow Foundry casts? Add only what you need:

```bash
agy plugin install ~/.galaxy-agentic-plugins/plugins/galaxy-dev-skills
agy plugin install ~/.galaxy-agentic-plugins/plugins/foundry-skills
```

## Step C · Verify and run

1. Type `/mcp` (`galaxy-mcp_galaxy` shows **running**), then ask:

   ```
   Connect to Galaxy and tell me who I am.
   ```

   The agent calls `get_user` and reports your Galaxy username and account
   details. *(If anything fails, run `/galaxy-connect`.)*
2. Ask in plain language — upload FASTQs, run IWC workflows, write in-Galaxy
   JupyterLite (`gxy`) notebooks, rebuild scratch histories (`/reproduciblify`),
   or author containerized UDTs (`/udt-authoring`).

<details>
<summary>Skills, workspace scoping, and updates</summary>

### Use the skills

Run `/skills` or type `/<skill-name>` — `/galaxy-connect`, `/galaxy-integration`,
`/galaxy-mcp-reference`, `/collection-manipulation`, `/udt-authoring`,
`/workflow-reports`, `/reproduciblify` (plus `/tool-dev` and `/nf-to-galaxy`
from `galaxy-dev-skills`). Nested sub-skills such as `jupyterlite-galaxy` are
loaded automatically through their parent skill.

To scope a plugin to one workspace instead of installing globally, copy its
folder into `<workspace>/.agents/plugins/`.

### Update or remove

```bash
git -C ~/.galaxy-agentic-plugins pull
agy plugin install ~/.galaxy-agentic-plugins/plugins/galaxy-mcp
agy plugin install ~/.galaxy-agentic-plugins/plugins/galaxy-skills
```

Use `agy plugin list` to inspect installed plugins and `agy plugin uninstall <name>` to remove one.

</details>

<details>
<summary>Manual MCP setup and troubleshooting</summary>

### Register `galaxy-mcp` without the plugin

(`${VAR}` placeholders inside `mcp_config.json` are not expanded by Antigravity; pass values via `--env` from an exported shell variable instead, and skip installing the `galaxy-mcp` plugin so the server is not registered twice.)

```bash
agy mcp add --env GALAXY_URL=https://usegalaxy.org \
            --env GALAXY_API_KEY="$GALAXY_API_KEY" \
            galaxy uvx galaxy-mcp
```

### Troubleshooting

- **No `galaxy-mcp_galaxy` in `/mcp`**: start a new session; check `agy plugin list` and `uv --version`.
- **"Missing Galaxy URL and API key"**: GUI IDE launches often miss `~/.zshrc`; add `GALAXY_URL` and `GALAXY_API_KEY` to a workspace `.env` file or register via `agy mcp add --env` above.
- **Server fails to start**: run `uvx galaxy-mcp` in a terminal to inspect the error.
- **"Provided API key is not valid"**: key belongs to a different Galaxy server or was revoked.

</details>
