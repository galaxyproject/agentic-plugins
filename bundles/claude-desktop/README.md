# Claude Desktop bundle (`.mcpb`)

One-click installer for the galaxy-mcp server in Claude Desktop. Uses the
`uv` server type, so Claude Desktop provisions Python and installs
`galaxy-mcp` from PyPI itself; the bundle contains no code beyond a
three-line entry point.

Build:

```bash
npx @anthropic-ai/mcpb validate bundles/claude-desktop/manifest.json
npx @anthropic-ai/mcpb pack bundles/claude-desktop dist/galaxy-mcp.mcpb
```

Releases attach the packed file; see [docs/claude-desktop.md](../../docs/claude-desktop.md).
