---
name: galaxy-connect
description: Set up, verify and troubleshoot the connection between this agent and a Galaxy server through the galaxy-mcp MCP server. Use when the user wants to connect to Galaxy, configure a Galaxy URL or API key, check whether Galaxy tools are available, or when a Galaxy MCP call fails with a connection or authentication error.
---

# Connect this agent to Galaxy

The `galaxy` MCP server (package `galaxy-mcp`, started with `uvx galaxy-mcp`)
exposes Galaxy operations as tools: `get_server_info`, `get_user`,
`get_histories`, `search_tools_by_name`, `run_tool`, `invoke_workflow`, and
more. It authenticates with a Galaxy URL and a per-user API key.

Tool names may carry a harness-specific prefix (for example
`mcp__plugin_galaxy-mcp_galaxy__get_user` in Claude Code, `galaxy-mcp_galaxy`
in Antigravity, or a `galaxyproject_agentic_plugins__galaxy` server name in Pi).
Search the available tools for `get_user` rather than assuming an exact name.

## 1. Check the current state

1. Look for the Galaxy MCP tools in your tool list. If none are present, the
   MCP server is not installed or not running; go to *Troubleshooting*.
2. Call `get_user` (or `get_server_info`). Success means credentials are set
   and valid; report the username, email and server version to the user and
   stop here.
3. If the call reports missing URL or API key, continue with step 2.

## 2. Help the user obtain an API key

Each Galaxy server issues its own keys. In the Galaxy web UI:

1. Log in, open the **User** menu, choose **Preferences**.
2. Choose **Manage API Key**.
3. Click **Create a new key** (or copy the existing one).

Public servers: `https://usegalaxy.org`, `https://usegalaxy.eu`,
`https://usegalaxy.org.au`. Institutional servers use their own URL. The URL
must be the base of the server (no `/api`, trailing slash optional).

An API key grants full access to the user's account. Ask the user to store it
in configuration, not to paste it into chat, unless they choose to.

## 3. Configure credentials

`galaxy-mcp` reads `GALAXY_URL` and `GALAXY_API_KEY` from its environment, or
from a `.env` file in the current working directory or any parent directory.
How the environment reaches the server depends on the harness:

| Harness | Where credentials come from |
|---------|-----------------------------|
| Claude Code (`galaxy-mcp` plugin) | Values entered when the plugin was installed (`userConfig`). Change them under `/plugin manage`, or use `claude mcp add` with `-e` for a manual server. |
| Codex CLI | `GALAXY_URL` and `GALAXY_API_KEY` exported in the shell that starts Codex (the plugin forwards exactly these two variables). Or `codex mcp add galaxy --env GALAXY_URL=... --env GALAXY_API_KEY=... -- uvx galaxy-mcp`. |
| Antigravity (`agy`) | Variables exported in the shell that starts `agy` (the server inherits the environment). Or `agy mcp add --env GALAXY_URL=... --env GALAXY_API_KEY=... galaxy uvx galaxy-mcp`. |
| Pi (`pi-mcp-adapter`) | Variables exported in the shell that starts `pi`. |
| Any harness | A `.env` file in the project directory containing `GALAXY_URL=...` and `GALAXY_API_KEY=...` (add `.env` to `.gitignore`). |

Shell example (add to `~/.zshrc` or `~/.bashrc`, then open a new terminal):

```bash
export GALAXY_URL="https://usegalaxy.org"
export GALAXY_API_KEY="paste-your-key-here"
```

Project `.env` example:

```
GALAXY_URL=https://usegalaxy.org
GALAXY_API_KEY=paste-your-key-here
```

After changing the environment the harness must be restarted so the MCP
server is relaunched with the new values.

If the user explicitly provides a URL and key in chat, call the `connect` tool
with them; this sets credentials for the current session only. Recommend that
they also store the values in configuration and consider rotating the key.

## 4. Verify

Call `get_user`. Then call `get_histories` and summarise the first few
histories so the user sees real data. Report the server URL you connected to.

## Troubleshooting

- **No Galaxy tools at all**: the plugin is not installed or the harness was not
  restarted after installing. Also confirm `uv` is installed
  (`uv --version`); `uvx galaxy-mcp` downloads the server on first use and
  needs network access.
- **`uvx: command not found`**: install uv from https://docs.astral.sh/uv/
  and make sure it is on `PATH` for GUI-launched harnesses too.
- **Missing URL / API key**: credentials did not reach the server. Re-check the
  table above; in Codex only allow-listed variables are forwarded, in
  Antigravity `${VAR}` placeholders in `mcp_config.json` are not expanded.
- **401 / 403 / "Provided API key is not valid"**: wrong server for that key,
  or key revoked. Keys are per server.
- **Connection refused / timeouts**: check the URL in a browser; corporate
  proxies and VPNs are the usual cause.
- **Server started but an older tool set is visible**: `uvx --refresh galaxy-mcp`
  fetches the latest release; restart the harness afterwards.

## Related skills

- `galaxy-integration` (in `galaxy-skills`) for how to use the MCP tools well.
- `mcp-reference` under `galaxy-integration` for the full tool catalogue.
