# Galaxy for Pi

Connects the [Pi](https://pi.dev) coding agent (`@earendil-works/pi-coding-agent`
1.x) to Galaxy with Pi's built-in MCP client (`galaxy-mcp`, 48 Galaxy tools) and
curated Galaxy skills.

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
   open a new terminal), or put them in a project `.env` file (gitignored):

   ```bash
   export GALAXY_URL="https://usegalaxy.org"
   export GALAXY_API_KEY="paste-your-key-here"
   ```

## Step B · Install in Pi

**Needs:** Pi 1.x (`pi --version`; install/upgrade via
`npm i -g @earendil-works/pi-coding-agent`) and [uv](https://docs.astral.sh/uv/)
on your `PATH` (`uv --version`).

```bash
pi mcp add galaxy -- uvx galaxy-mcp
pi install git:github.com/galaxyproject/agentic-plugins
```

**Restart `pi` afterwards.** *(Add `-l` to either command to scope it to `.pi/`
in your current project instead of `~/.pi/agent/`.)*

## Step C · Verify and run

1. Run `pi mcp list` in a terminal (`galaxy: connected, 48 tools`), then inside
   `pi` ask:

   ```
   Connect to Galaxy and tell me who I am.
   ```

   Pi calls `get_user` and reports your Galaxy username and account details.
   *(If anything fails, run `/skill:galaxy-connect`.)*
2. Ask in plain language — upload FASTQs, run IWC workflows, write in-Galaxy
   JupyterLite (`gxy`) notebooks, rebuild scratch histories
   (`/skill:reproduciblify`), or author containerized UDTs (`/skill:udt-authoring`).

<details>
<summary>Trimming skill sets (context budget), pi-mcp-adapter, and updates</summary>

### Keep only analyst skills (recommended)

`pi install` loads all 86 skills across `galaxy-skills`, `galaxy-dev-skills`, and
`foundry-skills`. Unless you build XML wrappers or Workflow Foundry casts,
exclude those sets in `~/.pi/agent/settings.json` (or `.pi/settings.json`):

```json
{
  "packages": [
    {
      "source": "git:github.com/galaxyproject/agentic-plugins",
      "skills": ["!plugins/foundry-skills/**", "!plugins/galaxy-dev-skills/**"]
    }
  ]
}
```

Or run `pi config` to toggle skills interactively. Update packages anytime with
`pi update --extensions`.

### Alternative: `pi-mcp-adapter`

If you use [pi-mcp-adapter](https://github.com/nicobailon/pi-mcp-adapter) instead
of Pi's built-in MCP extension, `package.json` also declares `pi.mcp` so
`pi install npm:pi-mcp-adapter` auto-registers the server as
`galaxyproject_agentic_plugins__galaxy` (and disables Pi's built-in `mcp` so
they do not collide).

</details>

<details>
<summary>Troubleshooting</summary>

- **`Cannot find module '@earendil-works/pi-coding-agent'`**: your global `pi` binary is from the deprecated `@mariozechner/pi-coding-agent` (`0.73.x`) package; upgrade to `npm install -g @earendil-works/pi-coding-agent`.
- **`galaxy` fails in `pi mcp list`**: confirm `GALAXY_URL` and `GALAXY_API_KEY` are exported in your shell (or present in `.env`) and `uv --version` works.
- **"Provided API key is not valid"**: key belongs to a different Galaxy server or was revoked.

</details>
