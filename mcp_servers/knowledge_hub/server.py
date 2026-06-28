#!/usr/bin/env python3
"""Knowledge Hub MCP Server — stdio transport.

Usage:
  python -m mcp_servers.knowledge_hub.server
  python -m mcp_servers.knowledge_hub.server --domains godot
  python -m mcp_servers.knowledge_hub.server --domains davinci_resolve
  KNOWLEDGE_HUB_DOMAINS=godot python -m mcp_servers.knowledge_hub.server

OpenCode config:
  "mcp": {
    "knowledge_hub": {
      "type": "local",
      "command": ["python3", "-m", "mcp_servers.knowledge_hub.server", "--domains", "godot"],
      "enabled": true
    }
  }
"""

import argparse
import json
import os
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import (
    search_knowledge,
    get_domain_status,
    update_domain,
    add_personal_note,
    list_personal_notes,
    list_domains,
    list_scoped_domains,
    set_domain_scope,
)

# ── CLI argument parsing (before MCP server starts) ───────────────────────


def _parse_domains_arg() -> list[str] | None:
    """Parse --domains CLI flag or KNOWLEDGE_HUB_DOMAINS env var.

    Returns None if neither is set (all domains visible).
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--domains", type=str, default=None,
                        help="Comma-separated list of domains to expose")
    args, _ = parser.parse_known_args()

    if args.domains:
        return [d.strip() for d in args.domains.split(",") if d.strip()]

    env = os.environ.get("KNOWLEDGE_HUB_DOMAINS")
    if env:
        return [d.strip() for d in env.split(",") if d.strip()]

    return None


server = Server("knowledge-hub")


@server.list_tools()
async def list_tools_handler() -> list[Tool]:
    return [
        Tool(
            name="search_knowledge",
            description="Search knowledge in a domain (exact=BM25, semantic=ChromaDB, hybrid=both + CrossEncoder rerank). Finds API references, code examples, and personal notes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Domain to search (e.g., 'godot', 'davinci_resolve')"},
                    "query": {"type": "string", "description": "Search query (natural language)"},
                    "mode": {"type": "string", "enum": ["exact", "semantic", "hybrid"], "description": "Search mode: exact=BM25, semantic=ChromaDB, hybrid=both", "default": "hybrid"},
                    "max_results": {"type": "integer", "description": "Maximum number of results", "default": 10},
                    "source_filter": {"type": "array", "items": {"type": "string", "enum": ["repo", "personal"]}, "description": "Filter by source type (repo and/or personal)"},
                },
                "required": ["domain", "query"],
            },
        ),
        Tool(
            name="get_domain_status",
            description="Get status of one or all knowledge domains (sources, personal notes, index state).",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Specific domain (omitted = all scoped domains)"},
                },
            },
        ),
        Tool(
            name="update_domain",
            description="Update a domain's knowledge: refresh repo sources (via repomix) and rebuild ChromaDB + BM25 index.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Domain to update"},
                    "rebuild_index": {"type": "boolean", "description": "Rebuild ChromaDB index after update", "default": True},
                },
                "required": ["domain"],
            },
        ),
        Tool(
            name="add_personal_note",
            description="Add a personal note (gotcha, tip, FAQ) to a domain's knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Domain to add to"},
                    "topic": {"type": "string", "description": "Short topic title"},
                    "content": {"type": "string", "description": "Note content (markdown)"},
                    "category": {"type": "string", "enum": ["gotchas", "tips", "best-practices", "faq"], "description": "Category of note", "default": "gotchas"},
                },
                "required": ["domain", "topic", "content"],
            },
        ),
        Tool(
            name="list_personal_notes",
            description="List personal notes for a domain.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Domain to list notes for"},
                    "category": {"type": "string", "description": "Filter by category (gotchas, tips, best-practices, faq)"},
                },
                "required": ["domain"],
            },
        ),
        Tool(
            name="list_domains",
            description="List all available knowledge domains (scoped to this server).",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool_handler(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "search_knowledge":
            result = search_knowledge(
                domain=arguments["domain"],
                query=arguments["query"],
                mode=arguments.get("mode", "hybrid"),
                max_results=arguments.get("max_results", 10),
                source_filter=arguments.get("source_filter"),
            )
        elif name == "get_domain_status":
            result = get_domain_status(domain=arguments.get("domain"))
        elif name == "update_domain":
            result = update_domain(
                domain=arguments["domain"],
                rebuild_index=arguments.get("rebuild_index", True),
            )
        elif name == "add_personal_note":
            result = add_personal_note(
                domain=arguments["domain"],
                topic=arguments["topic"],
                content=arguments["content"],
                category=arguments.get("category", "gotchas"),
            )
        elif name == "list_personal_notes":
            result = list_personal_notes(
                domain=arguments["domain"],
                category=arguments.get("category"),
            )
        elif name == "list_domains":
            domains = list_scoped_domains()
            result = {"domains": domains, "count": len(domains)}
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def main():
    # Parse and apply domain scoping before starting MCP loop
    domains = _parse_domains_arg()
    if domains:
        print(f"[INFO]  Domain scope: {domains}", file=sys.stderr)
        set_domain_scope(domains)
    else:
        print(f"[INFO]  Domain scope: ALL (no --domains flag)", file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
