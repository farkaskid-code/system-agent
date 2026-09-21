import logging
import os
import subprocess
from resource import RLIMIT_AS, RLIMIT_CPU, setrlimit
from typing import NamedTuple

from system_agent.core.parser import ParsedResult, parse

logger = logging.getLogger(__name__)


class Tool(NamedTuple):
    name: str
    command: str
    args: list[str]


class ToolResult(NamedTuple):
    tool: Tool
    status: bool
    stdout: ParsedResult
    stderr: ParsedResult


def check_permissions(tool: Tool, permissions: dict) -> dict:
    """
    Check if the current user has permission to run the specified tool.
    """
    current_user = os.getlogin()

    if current_user not in permissions:
        raise RuntimeError(f"{current_user} is not authorized")

    current_user_permissions = permissions.get(current_user)
    if tool.name not in current_user_permissions.get("allowed_tools"):
        raise RuntimeError(f"{current_user} is not authorized to run: {tool.name}")

    return current_user_permissions


def execute(tool: Tool, permissions: dict) -> ToolResult:
    """
    Execute the specified tool in a sandboxed environment with resource limits.
    """
    try:
        current_user_permissions = check_permissions(tool, permissions)
    except RuntimeError as e:
        logger.error(f"Permission check failed: {e}")
        return ToolResult(
            tool=tool,
            status=False,
            stdout=ParsedResult(type="text", raw="", parsed={}),
            stderr=ParsedResult(type="text", raw=str(e), parsed={}),
        )

    if "resource_limits" in current_user_permissions:
        cpu = current_user_permissions.get("resource_limits").get("cpu")
        cpu_limit = cpu * os.cpu_count()

        memory = current_user_permissions.get("resource_limits").get("memory")
        memory_limit = memory * 1024 * 1024

        logger.debug(f"applying resource limits with cpu: {cpu}%, memory: {memory}M")
        setrlimit(RLIMIT_AS, (memory_limit, memory_limit))
        setrlimit(RLIMIT_CPU, (cpu_limit, cpu_limit))

    logger.debug(f"executing tool: {tool}")
    try:
        process = subprocess.run(
            args=[*tool.command.split(), *tool.args],
            check=True,
            capture_output=True,
            text=True,  # Capture output as text
        )
        logger.debug(f"command execution success: {process.returncode == 0}")
        logger.debug("parsing: stdout")
        stdout = parse(process.stdout)
        logger.debug("parsing: stderr")
        stderr = parse(process.stderr)
        return ToolResult(
            tool=tool,
            status=process.returncode == 0,
            stdout=stdout,
            stderr=stderr,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"failed to execute command: {e}")
        logger.debug("parsing: stdout")
        stdout = parse(e.stdout)
        logger.debug("parsing: stderr")
        stderr = parse(e.stderr)
        return ToolResult(
            tool=tool,
            status=False,
            stdout=stdout,
            stderr=stderr,
        )
    except PermissionError as e:
        logger.error(f"Permission error: {e}")
        return ToolResult(
            tool=tool,
            status=False,
            stdout=ParsedResult(type="text", raw="", parsed={}),
            stderr=ParsedResult(type="text", raw=str(e), parsed={}),
        )
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return ToolResult(
            tool=tool,
            status=False,
            stdout=ParsedResult(type="text", raw="", parsed={}),
            stderr=ParsedResult(type="text", raw=str(e), parsed={}),
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return ToolResult(
            tool=tool,
            status=False,
            stdout=ParsedResult(type="text", raw="", parsed={}),
            stderr=ParsedResult(type="text", raw=str(e), parsed={}),
        )
