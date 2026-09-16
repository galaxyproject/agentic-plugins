#!/usr/bin/env python3
"""Smoke-test a stdio MCP command for galaxy-mcp without a Galaxy server.

Spawns the command with placeholder credentials, performs the MCP initialize
handshake, lists tools and checks the core Galaxy tools are present.

Usage:
  scripts/mcp_smoke.py                          # uvx galaxy-mcp
  scripts/mcp_smoke.py uv run --directory bundles/claude-desktop src/server.py

With GALAXY_URL and GALAXY_API_KEY set to real values and --live, also calls
get_user and prints the username (integration check).
"""
from __future__ import annotations

import json
import os
import select
import subprocess
import sys
import time

REQUIRED = {"connect", "get_user", "get_server_info", "get_histories", "search_tools_by_name", "run_tool", "invoke_workflow"}


def main() -> int:
    args = sys.argv[1:]
    live = "--live" in args
    cmd = [a for a in args if a != "--live"] or ["uvx", "galaxy-mcp"]
    env = dict(os.environ)
    if not live:
        env.update(GALAXY_URL="https://example.invalid", GALAXY_API_KEY="smoke")
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True)

    def send(obj: dict) -> None:
        assert p.stdin
        p.stdin.write(json.dumps(obj) + "\n")
        p.stdin.flush()

    def recv(timeout: float = 300) -> dict:
        end = time.time() + timeout
        while time.time() < end:
            ready, _, _ = select.select([p.stdout], [], [], 1)
            if ready:
                line = p.stdout.readline()  # type: ignore[union-attr]
                if not line:
                    break
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        p.kill()
        sys.exit("timeout waiting for MCP response; stderr tail:\n" + (p.stderr.read()[-1500:] if p.stderr else ""))

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "agentic-plugins-smoke", "version": "0"}}})
        info = recv()["result"]["serverInfo"]
        print(f"server: {info.get('name')} {info.get('version')}")
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = sorted(t["name"] for t in recv()["result"]["tools"])
        print(f"{len(names)} tools")
        missing = REQUIRED - set(names)
        if missing:
            sys.exit(f"missing required tools: {sorted(missing)}")
        if live:
            send({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_user", "arguments": {}}})
            res = recv()["result"]
            text = "".join(c.get("text", "") for c in res.get("content", []))
            if res.get("isError"):
                sys.exit(f"get_user failed: {text[:500]}")
            print(f"get_user: {text[:300]}")
        print("smoke OK")
        return 0
    finally:
        p.terminate()


if __name__ == "__main__":
    sys.exit(main())
