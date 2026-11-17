# Getting a Galaxy API key

Every Galaxy server issues its own API keys. An API key grants full access to
your account on that server — treat it like a password and never paste it into
chat.

1. Log in to your Galaxy server (for example
   [usegalaxy.org](https://usegalaxy.org),
   [usegalaxy.eu](https://usegalaxy.eu),
   [usegalaxy.org.au](https://usegalaxy.org.au), or your institution's server).
2. Open **User › Preferences** in the top navigation bar.
3. Click **Manage API Key**.
4. Click **Create a new key** (if you do not already have one) and copy it.

Keep these two values ready for your agent setup:

| Value | Example | Notes |
|-------|---------|-------|
| **Galaxy URL** | `https://usegalaxy.org` | Base server URL only — omit `/api` |
| **Galaxy API key** | `1a2b3c4d...` | Unique to this server; creating a new key revokes the old one |

How you store these two values depends on your harness in **Step B** below:
**Claude Code** and **Claude Desktop** prompt for them at install time and save
the key in your system keychain; **Codex CLI**, **Antigravity**, and **Pi** read
`GALAXY_URL` and `GALAXY_API_KEY` from your shell environment or a project
`.env` file (keep `.env` out of git).
