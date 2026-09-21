import logging
import sys
from os import getenv
from pathlib import Path

from system_agent.core.llm_client import LLMClient
from system_agent.core.tool_executor import execute

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_tools_and_permissions(path: Path) -> tuple[list[dict], dict]:
    try:
        logger.debug(f"loading tools and permissions from: {path}")
        from yaml import safe_load

        data = safe_load(path.read_text())
        return data["tools"], data["permissions"]
    except (FileNotFoundError, KeyError) as e:
        raise RuntimeError(f"Failed in loading tools and permissions because: {e}")


def main() -> None:
    OLLAMA_API_BASE = getenv("OLLAMA_API_BASE")
    url = f"{OLLAMA_API_BASE}/v1/chat/completions"
    model_name = "qwen2.5-coder:14b"

    TOOL_DECLARATIONS = Path("src/system_agent/config/tools.yaml")

    declared_tools, permissions = load_tools_and_permissions(TOOL_DECLARATIONS)
    client = LLMClient(url=url, model_name=model_name, tools=declared_tools)

    tool = client.get_tool(sys.argv[1])
    result = execute(tool=tool, permissions=permissions)

    if result.status:
        logger.info(result.stdout.raw)
    else:
        logger.info(result.stderr.raw)
