"""Claude Desktop (MCPB) entry point: run the galaxy-mcp server over stdio.

Credentials arrive as GALAXY_URL / GALAXY_API_KEY in the environment, set by
Claude Desktop from the bundle's user_config.
"""

from galaxy_mcp.__main__ import run

if __name__ == "__main__":
    run()
