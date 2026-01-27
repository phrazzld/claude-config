"""MCP server for spawning Kimi K2.5 agents.

Mirrors codex-as-mcp pattern: provides spawn_agent and spawn_agents_parallel
tools for delegating implementation tasks to Kimi's Agent Swarm.
"""

import asyncio
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

server = Server("kimi-as-mcp")


def _run_kimi(prompt: str, thinking: bool = False, cwd: str | None = None) -> str:
    """Execute kimi CLI in non-interactive mode.

    Args:
        prompt: The task/instruction for the agent
        thinking: Enable extended reasoning mode
        cwd: Working directory (defaults to current)

    Returns:
        Agent output (stdout)
    """
    cmd = ["kimi", "--print"]
    if thinking:
        cmd.append("--thinking")
    cmd.extend(["--prompt", prompt])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or os.getcwd(),
        timeout=600,  # 10 minute timeout
    )

    output = result.stdout
    if result.returncode != 0 and result.stderr:
        output += f"\n\nSTDERR:\n{result.stderr}"

    return output


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="spawn_agent",
            description=(
                "Spawn a Kimi K2.5 agent to work in the current directory. "
                "Kimi excels at frontend development, visual coding, and "
                "can coordinate up to 100 sub-agents via Agent Swarm. "
                "Very cost-effective (~$0.15/M input, $2.50/M output)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Instructions for the agent (task, context, constraints)",
                    },
                    "thinking": {
                        "type": "boolean",
                        "description": "Enable extended reasoning mode for complex tasks",
                        "default": False,
                    },
                },
                "required": ["prompt"],
            },
        ),
        Tool(
            name="spawn_agents_parallel",
            description=(
                "Spawn multiple Kimi K2.5 agents in parallel. "
                "Leverages Agent Swarm for 4.5x faster execution than sequential. "
                "Each agent runs independently in the current working directory."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agents": {
                        "type": "array",
                        "description": "List of agent specs with 'prompt' and optional 'thinking' keys",
                        "items": {
                            "type": "object",
                            "properties": {
                                "prompt": {"type": "string"},
                                "thinking": {"type": "boolean", "default": False},
                            },
                            "required": ["prompt"],
                        },
                    },
                },
                "required": ["agents"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    cwd = os.getcwd()

    if name == "spawn_agent":
        prompt = arguments["prompt"]
        thinking = arguments.get("thinking", False)

        output = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _run_kimi(prompt, thinking, cwd)
        )

        return [TextContent(type="text", text=output)]

    elif name == "spawn_agents_parallel":
        agents = arguments["agents"]

        def run_agent(spec: dict) -> dict:
            idx = spec.get("_index", 0)
            try:
                output = _run_kimi(
                    spec["prompt"],
                    spec.get("thinking", False),
                    cwd,
                )
                return {"index": idx, "output": output}
            except Exception as e:
                return {"index": idx, "output": "", "error": str(e)}

        # Add indices for tracking
        for i, agent in enumerate(agents):
            agent["_index"] = i

        # Run in parallel with thread pool
        with ThreadPoolExecutor(max_workers=min(len(agents), 10)) as executor:
            results = list(executor.map(run_agent, agents))

        # Sort by index
        results.sort(key=lambda x: x["index"])

        # Format output
        output_parts = []
        for r in results:
            header = f"=== Agent {r['index']} ==="
            if "error" in r:
                output_parts.append(f"{header}\nERROR: {r['error']}")
            else:
                output_parts.append(f"{header}\n{r['output']}")

        return [TextContent(type="text", text="\n\n".join(output_parts))]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def run():
    """Run the MCP server with stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main():
    """Entry point."""
    import asyncio

    asyncio.run(run())


if __name__ == "__main__":
    main()
