#!/usr/bin/env python3
"""Print the "Add to Cursor" deeplink for the galaxy MCP server.

Cursor's install deeplink carries the server config as base64-encoded JSON:
  cursor://anysphere.cursor-deeplink/mcp/install?name=<name>&config=<base64>
The config here references shell variables, so no secret is embedded.
"""
import base64
import json
import sys
import urllib.parse

CONFIG = {
    "command": "uvx",
    "args": ["galaxy-mcp"],
    "env": {
        "GALAXY_URL": "${env:GALAXY_URL}",
        "GALAXY_API_KEY": "${env:GALAXY_API_KEY}",
    },
}


def deeplink(name: str = "galaxy", config: dict = CONFIG) -> str:
    encoded = base64.b64encode(json.dumps(config, separators=(",", ":")).encode()).decode()
    return f"cursor://anysphere.cursor-deeplink/mcp/install?name={name}&config={urllib.parse.quote(encoded, safe='')}"


if __name__ == "__main__":
    link = deeplink()
    if "--check" in sys.argv:
        # round-trip: the docs must contain exactly this link
        import pathlib
        doc = pathlib.Path(__file__).resolve().parent.parent / "docs" / "cursor.md"
        if link not in doc.read_text():
            sys.exit(f"docs/cursor.md does not contain the current deeplink:\n{link}")
        print("deeplink in docs/cursor.md is current")
    else:
        print(link)
