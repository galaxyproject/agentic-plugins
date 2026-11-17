# Galaxy for Claude Desktop

## Step 1 · Get your Galaxy API key

- **Galaxy API key:** On [usegalaxy.org](https://usegalaxy.org) *(or [usegalaxy.eu](https://usegalaxy.eu) / [usegalaxy.org.au](https://usegalaxy.org.au))*, open **User › Preferences › Manage API Key** → **Create a new key**.
- **Custom tools on UseGalaxy.org *(optional)*:** Request [User-Defined Tools beta access](https://udt-signup.galaxyproject.org/) (~30s). Standard tools work immediately while we approve.

## Step 2 · Open the one-click bundle

No terminal or Python install required *(connects the 48 Galaxy MCP tools directly)*:

1. Download **`galaxy-mcp.mcpb`** from the **[latest release](https://github.com/galaxyproject/agentic-plugins/releases/latest)** and double-click it *(or drag onto [Claude Desktop](https://claude.com/download))*.
2. Enter your **Galaxy URL** (default `https://usegalaxy.org`, no `/api`) and **Galaxy API key**, then click **Install** *(first start takes ~30–60s)*.

## Step 3 · Verify and run

Open a new chat and ask:

```
Connect to Galaxy and tell me who I am.
```

Claude calls `get_user` and confirms your account. Then ask it to inspect histories, upload datasets, launch IWC workflows, or create and run containerized YAML tools.

<details>
<summary>Reconfigure, update, manual JSON config & troubleshooting</summary>

### Reconfigure or update

Update credentials under **Settings › Extensions › Galaxy › Configure**. Upgrade anytime by opening a newer `galaxy-mcp.mcpb` from [Releases](https://github.com/galaxyproject/agentic-plugins/releases/latest).

### Manual `claude_desktop_config.json` (without `.mcpb`)

Requires [uv](https://docs.astral.sh/uv/) (`Settings › Developer › Edit Config`):

```json
{
  "mcpServers": {
    "galaxy": {
      "command": "uvx",
      "args": ["galaxy-mcp"],
      "env": {
        "GALAXY_URL": "https://usegalaxy.org",
        "GALAXY_API_KEY": "paste-your-key-here"
      }
    }
  }
}
```

- **Startup error:** check **Settings › Extensions › Galaxy** logs; first launch requires internet access to download `galaxy-mcp`.
- **Invalid API key:** keys are per Galaxy server; generate a key on the matching server and update **Configure**.

</details>

## For maintainers

The bundle source is `bundles/claude-desktop/`. CI validates and packs it on every push and attaches `galaxy-mcp.mcpb` to tagged releases:

```bash
npx --yes @anthropic-ai/mcpb validate bundles/claude-desktop
npx --yes @anthropic-ai/mcpb pack bundles/claude-desktop dist/galaxy-mcp.mcpb
```
