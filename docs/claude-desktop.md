# Galaxy for Claude Desktop

Connects [Claude Desktop](https://claude.com/download) to Galaxy as a
**one-click bundle** (48 Galaxy MCP tools: histories, datasets, tools, IWC
workflows, and User-Defined Tools). **No terminal or Python install required.**

*(Agent Skills apply only to coding agents — Claude Desktop uses the MCP tools directly.)*

## Step A · Get your Galaxy API key and request UDT access

1. **API key:** Log in to [usegalaxy.org](https://usegalaxy.org) (or
   [usegalaxy.eu](https://usegalaxy.eu), [usegalaxy.org.au](https://usegalaxy.org.au),
   or your institution's server) → **User › Preferences › Manage API Key** →
   **Create a new key** → copy it. *(Keep it out of chat; Claude Desktop stores
   it in your system keychain in Step B.)*
2. **User-Defined Tools beta (UseGalaxy.org):** Submit the 30-second form at
   **[udt-signup.galaxyproject.org](https://udt-signup.galaxyproject.org/)**
   with your UseGalaxy.org email *(optional ORCID sign-in speeds review)*. Basic
   tools and workflows work immediately; once approved, Claude can also create
   and run custom containerized tools (`create_user_tool` / `run_user_tool`).

## Step B · Install the one-click bundle

1. Download **`galaxy-mcp.mcpb`** from the
   [latest release](https://github.com/galaxyproject/agentic-plugins/releases/latest)
   and double-click it (or drag onto Claude Desktop / **Settings › Extensions ›
   Advanced settings › Install Extension…**).
2. In the install dialog, fill in **Galaxy URL** (default `https://usegalaxy.org`,
   no `/api`) and **Galaxy API key**, then click **Install**. *(First start takes
   ~30–60 seconds while Claude Desktop's built-in runtime downloads `galaxy-mcp`.)*

## Step C · Verify and run

Start a new chat and ask:

```
Connect to Galaxy and tell me who I am.
```

Claude calls `get_user` and reports your Galaxy username and account details.
Then ask it to inspect histories, upload datasets, launch IWC workflows, or
author and run User-Defined Tools.

<details>
<summary>Reconfigure, update, manual setup, and troubleshooting</summary>

### Change the Galaxy URL or API key

Open **Settings › Extensions › Galaxy › Configure**, update your values, and
start a new chat.

### Update

Download the newest `galaxy-mcp.mcpb` from the
[releases page](https://github.com/galaxyproject/agentic-plugins/releases/latest)
and open it — Claude Desktop upgrades in place and keeps your credentials.

### Manual config (without `.mcpb` bundle)

Requires [uv](https://docs.astral.sh/uv/) on your `PATH`. Add to
`claude_desktop_config.json` (**Settings › Developer › Edit Config**):

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

### Troubleshooting

- **Extension error right after install**: check **Settings › Extensions › Galaxy** logs; first launch requires network access to download Python and `galaxy-mcp`.
- **"Missing Galaxy URL and API key"**: open **Settings › Extensions › Galaxy › Configure** and fill both fields.
- **"Provided API key is not valid"**: key belongs to a different Galaxy server or was revoked; generate a fresh key and update **Configure**.
- **Slow first tool call**: `galaxy-mcp` starts on demand; subsequent calls are fast.

</details>

## For maintainers

The bundle source is `bundles/claude-desktop/`. CI validates and packs it on
every push and attaches `galaxy-mcp.mcpb` to tagged releases:

```bash
npx @anthropic-ai/mcpb validate bundles/claude-desktop/manifest.json
npx @anthropic-ai/mcpb pack bundles/claude-desktop dist/galaxy-mcp.mcpb
python3 scripts/mcp_smoke.py uv run --directory bundles/claude-desktop src/server.py
```
