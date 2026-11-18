# Galaxy in Orbit

## Step 1 · Get your Galaxy key and a model key

- **Galaxy API key:** On [usegalaxy.org](https://usegalaxy.org) *(or [usegalaxy.eu](https://usegalaxy.eu) / [usegalaxy.org.au](https://usegalaxy.org.au))*, open **User › Preferences › Manage API Key** → **Create a new key**.
- **Custom tools on UseGalaxy.org *(optional)*:** Request [User-Defined Tools beta access](https://udt-signup.galaxyproject.org/) (~30s). Standard tools work immediately while we approve.
- **Model provider:** Grab an API key from [Anthropic](https://console.anthropic.com/) (`claude-sonnet-4-6` recommended), [OpenAI](https://platform.openai.com/), [Google Gemini](https://aistudio.google.com/), or [DeepSeek](https://platform.deepseek.com/) — or sign in with an existing **ChatGPT Plus / Pro** subscription inside Orbit.

## Step 2 · Download Orbit and enter your keys

**[Orbit](https://galaxyproject.org/agents/orbit/)** is Galaxy's standalone desktop app — **`galaxy-mcp` and `galaxy-skills` are already built in** (no terminal required):

1. Download the installer for macOS (`.dmg`), Linux (`.deb` / `.rpm` / `.zip`), or Windows (`.zip`) from **[Orbit Releases](https://github.com/galaxyproject/orbit/releases/latest)** and open **Orbit**.
2. Press **`Cmd+,`** (`Ctrl+,` on Linux/Windows) to open **Preferences**:
   - **Provider:** paste your model key *(or choose **OpenAI Codex** → **Sign in with ChatGPT**)* and pick a default model.
   - **Galaxy:** enter `https://usegalaxy.org` (no `/api`) and paste your Galaxy API key → **Save** *(footer indicator turns green)*.

## Step 3 · Verify and run

Start a session and ask:

```
Connect to Galaxy and tell me who I am.
```

Orbit confirms your Galaxy account and attaches to a history. Describe your analysis — Orbit drafts a plan for your approval, executes on Galaxy (including custom containerized UDTs), and records every decision in your notebook. Full tour & model guide: **[galaxyproject.org/agents/orbit/](https://galaxyproject.org/agents/orbit/)**.

<details>
<summary>Model switching, Windows WSL2 & troubleshooting</summary>

- **Switch models mid-session:** plan on a frontier model, then switch to a cheaper model for execution via the footer selector, `Cmd/Ctrl+,`, or `/model <exact-id>` (e.g. `/model claude-sonnet-4-6`).
- **Windows local shell (WSL2):** native `Orbit.exe` runs all steps remotely on Galaxy; for local shell execution on Windows 11 (WSLg), install `orbit_<version>_amd64.deb` inside Ubuntu WSL2 (`chmod 600 ~/.loom/config.json`).
- **Troubleshooting & feedback:** if the footer Galaxy dot stays grey/red, check **Preferences › Galaxy** (omit `/api`; match key to server). Report issues via Orbit's **Feedback** button or **[GitHub Discussions (`Agents & UDTs`)](https://github.com/galaxyproject/galaxy/discussions/categories/agents-udts)**.

</details>
