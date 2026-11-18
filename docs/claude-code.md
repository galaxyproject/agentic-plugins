# Galaxy for Claude Code

## Step 1 · Get your Galaxy API key

- **Galaxy API key:** On [usegalaxy.org](https://usegalaxy.org) *(or [usegalaxy.eu](https://usegalaxy.eu) / [usegalaxy.org.au](https://usegalaxy.org.au))*, open **User › Preferences › Manage API Key** → **Create a new key**.
- **Custom tools on UseGalaxy.org *(optional)*:** Request [User-Defined Tools beta access](https://udt-signup.galaxyproject.org/) (~30s). Standard tools and workflows work immediately while we approve.

## Step 2 · Install the Galaxy plugins

Requires [Claude Code](https://code.claude.com) and [uv](https://docs.astral.sh/uv/) (`uv --version`). Run inside Claude Code:

```
/plugin marketplace add galaxyproject/agentic-plugins
/plugin install galaxy-mcp@galaxyproject
/plugin install galaxy-skills@galaxyproject
```

Enter your **Galaxy URL** (default `https://usegalaxy.org`, no `/api`) and **API key** when prompted (saved to your keychain), then **start a new Claude Code session**.

## Step 3 · Verify and run

Check `/mcp` shows `galaxy` **connected**, then ask:

```
Connect to Galaxy and tell me who I am.
```

Claude calls `get_user` and confirms your account. Then ask in plain language — upload reads, run IWC workflows, write JupyterLite (`gxy`) notebooks, rebuild scratch histories (`reproduciblify`), or author containerized YAML tools (`udt-authoring`).

<details>
<summary>Optional developer skills, CLI install, updates & troubleshooting</summary>

### Optional plugins (tool wrappers & workflow engineering)

Install only if you author ToolShed XML wrappers or Workflow Foundry pipelines (every skill adds to per-turn context):

```
/plugin install galaxy-dev-skills@galaxyproject
/plugin install foundry-skills@galaxyproject
```

### Slash commands

Claude selects skills automatically, or call them directly: `/galaxy-mcp:galaxy-connect`, `/galaxy-skills:galaxy-integration`, `/galaxy-skills:galaxy-mcp-reference`, `/galaxy-skills:collection-manipulation`, `/galaxy-skills:udt-authoring`, `/galaxy-skills:workflow-reports`, `/galaxy-skills:reproduciblify`.

### Terminal install, updates & reconfiguration

Headless install (Claude Code 2.1.275+, with `GALAXY_API_KEY` exported):

```bash
claude plugin install galaxy-mcp --marketplace galaxyproject/agentic-plugins \
  --config galaxy_url=https://usegalaxy.org \
  --config galaxy_api_key="$GALAXY_API_KEY"
claude plugin install galaxy-skills@galaxyproject
```

Reconfigure anytime via `/plugin configure galaxy-mcp@galaxyproject` (then restart). Update via `/plugin marketplace update galaxyproject` followed by `/plugin update galaxy-mcp@galaxyproject` and `/plugin update galaxy-skills@galaxyproject`.

### Manual MCP setup (without plugins) & troubleshooting

```bash
claude mcp add --scope user galaxy \
  -e GALAXY_URL=https://usegalaxy.org \
  -e GALAXY_API_KEY="$GALAXY_API_KEY" \
  -- uvx galaxy-mcp
```

- **No `galaxy` in `/mcp`:** start a new session after installing; check `uv --version`.
- **Key or URL error:** run `/plugin configure galaxy-mcp@galaxyproject` (keys are per Galaxy server; omit `/api` from URL) or run `/galaxy-mcp:galaxy-connect`.

</details>
