# Galaxy for Cursor

Connects [Cursor](https://cursor.com) to Galaxy with the `galaxy-mcp` server (48
Galaxy tools) and curated `galaxy-skills`.

## Step A · Get your Galaxy API key, request UDT access, and export credentials

1. **API key:** Log in to [usegalaxy.org](https://usegalaxy.org) (or
   [usegalaxy.eu](https://usegalaxy.eu), [usegalaxy.org.au](https://usegalaxy.org.au),
   or your institution's server) → **User › Preferences › Manage API Key** →
   **Create a new key** → copy it.
2. **User-Defined Tools beta (UseGalaxy.org):** Submit the 30-second form at
   **[udt-signup.galaxyproject.org](https://udt-signup.galaxyproject.org/)**
   with your UseGalaxy.org email *(optional ORCID sign-in speeds review)*. Basic
   tools and workflows work immediately while we approve UDT access.
3. **Export credentials:** Add both variables to `~/.zshrc` or `~/.bashrc` and
   launch Cursor from a terminal (or place them in a project `.env` file, which
   works even when Cursor is launched from a GUI icon):

   ```bash
   export GALAXY_URL="https://usegalaxy.org"
   export GALAXY_API_KEY="paste-your-key-here"
   ```

## Step B · Install in Cursor

**Needs:** Cursor with plugin support and [uv](https://docs.astral.sh/uv/) on
your `PATH` (`uv --version`).

1. Open **Customize** in the Cursor sidebar → **From GitHub Repository** → enter
   `galaxyproject/agentic-plugins`.
2. Install **`galaxy-mcp`** and **`galaxy-skills`** *(add `galaxy-dev-skills` or
   `foundry-skills` only if you build XML wrappers or Foundry workflows)*.
3. Run **Developer: Reload Window**.

*(Only want the MCP connection? Click [Add Galaxy to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=galaxy&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJnYWxheHktbWNwIl0sImVudiI6eyJHQUxBWFlfVVJMIjoiJHtlbnY6R0FMQVhZX1VSTH0iLCJHQUxBWFlfQVBJX0tFWSI6IiR7ZW52OkdBTEFYWV9BUElfS0VZfSJ9fQ%3D%3D) to register `galaxy-mcp` in one click using your environment variables.)*

## Step C · Verify and run

1. Check **Customize › MCP** (`galaxy` enabled), then ask in Agent chat:

   ```
   Connect to Galaxy and tell me who I am.
   ```

   *(If anything fails, run `/galaxy-connect`.)*
2. Ask in plain language — upload FASTQs, run IWC workflows, write in-Galaxy
   JupyterLite (`gxy`) notebooks, rebuild scratch histories (`/reproduciblify`),
   or author containerized UDTs (`/udt-authoring`).

<details>
<summary>Manual setup and troubleshooting</summary>

### Manual `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "galaxy": {
      "command": "uvx",
      "args": ["galaxy-mcp"],
      "env": {
        "GALAXY_URL": "${env:GALAXY_URL}",
        "GALAXY_API_KEY": "${env:GALAXY_API_KEY}"
      }
    }
  }
}
```

### Troubleshooting

- **No `galaxy` server under Customize › MCP**: reload the window and verify `uv --version`.
- **"Missing Galaxy URL and API key"**: GUI launches often skip `~/.zshrc`; put `GALAXY_URL` and `GALAXY_API_KEY` in a project `.env` file.
- **Server fails to start**: run `uvx galaxy-mcp` in a terminal to inspect the error.
- **"Provided API key is not valid"**: key belongs to a different Galaxy server or was revoked.

</details>

## For maintainers: marketplace listing

Importing the repository from **Customize** works today. Listing in the public
[Cursor Marketplace](https://cursor.com/marketplace) is a manual submission at
[cursor.com/marketplace/publish](https://cursor.com/marketplace/publish):

- valid `.cursor-plugin/plugin.json` in each plugin, unique kebab-case names: yes
- `description` on every plugin: yes
- components with valid frontmatter: yes
- logo committed and referenced by relative path: `assets/logo.svg`
- `README.md` documents usage and configuration: this file and the root README
- multi-plugin repo with `.cursor-plugin/marketplace.json` at the root: yes
- tested locally in `~/.cursor/plugins/local/`: **not yet**; do this before submitting
