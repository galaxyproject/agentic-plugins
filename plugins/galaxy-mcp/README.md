# galaxy-mcp plugin

Wires the [galaxy-mcp](https://github.com/galaxyproject/galaxy-mcp) server into
your coding agent and ships one skill, `galaxy-connect`, that helps the agent
set up, verify and troubleshoot the connection.

The MCP server is started with `uvx galaxy-mcp`, so [uv](https://docs.astral.sh/uv/)
must be installed. Credentials come from `GALAXY_URL` and `GALAXY_API_KEY`.

| File | Harness | Notes |
|------|---------|-------|
| `.claude-plugin/plugin.json` + `mcp/claude.json` | Claude Code | Prompts for URL and key at install (`userConfig`) |
| `.codex-plugin/plugin.json` (server inlined under `mcpServers`) | Codex CLI | Forwards `GALAXY_URL` / `GALAXY_API_KEY` from your shell (`env_vars`) |
| `plugin.json` + `mcp_config.json` | Antigravity (`agy`) | Inherits your shell environment |
| `mcp/pi.json` (via root `package.json` -> `pi.mcp`) | Pi | Needs `pi-mcp-adapter`; inherits your shell environment |
| `skills/galaxy-connect/` | all | Setup / verification skill |

Per-harness install instructions live in [`../../docs/`](../../docs/).
