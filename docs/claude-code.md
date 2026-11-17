# Galaxy for Claude Code

Connects [Claude Code](https://code.claude.com) to Galaxy with the `galaxy-mcp`
server (48 Galaxy tools) and curated `galaxy-skills`.

## Step A · Get your Galaxy API key and request UDT access

1. **API key:** Log in to [usegalaxy.org](https://usegalaxy.org) (or
   [usegalaxy.eu](https://usegalaxy.eu), [usegalaxy.org.au](https://usegalaxy.org.au),
   or your institution's server) → **User › Preferences › Manage API Key** →
   **Create a new key** → copy it. *(Keep it out of chat; Claude Code saves it in
   your system keychain in Step B.)*
2. **User-Defined Tools beta (UseGalaxy.org):** Submit the 30-second form at
   **[udt-signup.galaxyproject.org](https://udt-signup.galaxyproject.org/)**
   with your UseGalaxy.org email *(optional ORCID sign-in speeds review)*. All
   installed Galaxy tools and workflows work immediately; once approved, Claude
   can also write and run custom containerized YAML tools (`create_user_tool` /
   `run_user_tool`).

## Step B · Install in Claude Code

**Needs:** Claude Code (`claude --version`) and [uv](https://docs.astral.sh/uv/)
on your `PATH` (`uv --version`).

Run inside Claude Code:

```
/plugin marketplace add galaxyproject/agentic-plugins
/plugin install galaxy-mcp@galaxyproject
/plugin install galaxy-skills@galaxyproject
```

Installing `galaxy-mcp` prompts for your **Galaxy URL** (default
`https://usegalaxy.org`, no `/api`) and **API key**. **Start a new Claude Code
session afterwards.**

Building Galaxy XML wrappers or Workflow Foundry casts? Add only what you need
(every installed skill adds its description to each turn's context):

```
/plugin install galaxy-dev-skills@galaxyproject
/plugin install foundry-skills@galaxyproject
```

## Step C · Verify and run

1. Run `/mcp` (`galaxy` shows **connected**), then ask:

   ```
   Connect to Galaxy and tell me who I am.
   ```

   Claude calls `get_user` and reports your Galaxy username and account details.
   *(If anything fails, run `/galaxy-mcp:galaxy-connect`.)*
2. Ask for real work in plain language — uploading FASTQs, running IWC
   workflows, writing in-Galaxy JupyterLite (`gxy`) notebooks, rebuilding
   scratch histories (`reproduciblify`), or authoring containerized UDTs.

<details>
<summary>Skills, terminal install, updates, and reconfiguration</summary>

### Invoke skills directly or in plain language

Claude picks skills automatically from your prompt, or you can invoke them with `/`:

| Command | Purpose |
|---------|---------|
| `/galaxy-mcp:galaxy-connect` | Diagnose or verify the Galaxy connection |
| `/galaxy-skills:galaxy-integration` | Choose between MCP, JupyterLite (`gxy`), and BioBlend scripts |
| `/galaxy-skills:galaxy-mcp-reference` | Galaxy MCP tool catalog and ID pitfalls |
| `/galaxy-skills:collection-manipulation` | Filter, sort, relabel, and reshape dataset collections |
| `/galaxy-skills:udt-authoring` | Author validated `GalaxyUserTool` YAML definitions |
| `/galaxy-skills:workflow-reports` | Draft Galaxy Workflow Editor report templates |
| `/galaxy-skills:reproduciblify` | Rebuild a messy history into a clean, workflow-extractable analysis |
| `/galaxy-dev-skills:tool-dev` | Author and test ToolShed XML wrappers (`galaxy-dev-skills`) |
| `/galaxy-dev-skills:nf-to-galaxy` | Convert Nextflow modules and pipelines (`galaxy-dev-skills`) |
| `/foundry-skills:pipeline-nextflow-to-galaxy` | End-to-end Nextflow-to-Galaxy Foundry pipeline (`foundry-skills`) |

### Install from a terminal (or headlessly)

On Claude Code 2.1.275+, `--marketplace` adds the marketplace automatically
(export `GALAXY_API_KEY` first so the secret stays out of shell history):

```bash
claude plugin install galaxy-mcp --marketplace galaxyproject/agentic-plugins \
  --config galaxy_url=https://usegalaxy.org \
  --config galaxy_api_key="$GALAXY_API_KEY"
claude plugin install galaxy-skills@galaxyproject
```

### Change URL/key or update

Reconfigure anytime with `/plugin configure galaxy-mcp@galaxyproject` (then
start a new session). Update installed plugins with:

```
/plugin marketplace update galaxyproject
/plugin update galaxy-mcp@galaxyproject
/plugin update galaxy-skills@galaxyproject
```

</details>

<details>
<summary>Manual MCP setup and troubleshooting</summary>

### Register `galaxy-mcp` without the plugin

```bash
claude mcp add --scope user galaxy \
  -e GALAXY_URL=https://usegalaxy.org \
  -e GALAXY_API_KEY="$GALAXY_API_KEY" \
  -- uvx galaxy-mcp
```

### Troubleshooting

- **No `galaxy` server in `/mcp`**: start a new session after installing; confirm `uv --version` works.
- **Server fails on first start**: run `uvx galaxy-mcp` in a terminal to inspect the error (first run needs network access to fetch `galaxy-mcp` from PyPI).
- **"Plugin option galaxy_api_key isn't set"** or **"Missing Galaxy URL and API key"**: run `/plugin configure galaxy-mcp@galaxyproject` and fill in both fields, or place `GALAXY_URL` and `GALAXY_API_KEY` in a project `.env` file.
- **"Provided API key is not valid"**: keys are per Galaxy server; create or copy the key from the matching server and reconfigure.

</details>
