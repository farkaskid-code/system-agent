import logging
import sys
from os import getenv
from pathlib import Path

from system_agent.core.llm_client import LLMClient
from system_agent.core.tool_executor import execute

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_declared_tools(path: Path) -> list[dict]:
    try:
        logger.debug(f"loading tools from: {path}")
        from yaml import safe_load

        return safe_load(path.read_text())["tools"]
    except (FileNotFoundError, KeyError) as e:
        raise RuntimeError(f"Failed in loading tools because: {e}")


def main() -> None:
    OLLAMA_API_BASE = getenv("OLLAMA_API_BASE")
    url = f"{OLLAMA_API_BASE}/v1/chat/completions"
    model_name = "qwen2.5-coder:14b"

    TOOL_DECLARATIONS = Path("src/system_agent/config/tool_declarations.yaml")

    declared_tools = get_declared_tools(TOOL_DECLARATIONS)
    client = LLMClient(url=url, model_name=model_name, tools=declared_tools)

    tool = client.get_tool(sys.argv[1])
    result = execute(tool=tool)

    if result.status:
        logger.info(result.stdout.raw)
    else:
        logger.info(result.stderr.raw)
