import logging
from json import loads

from requests import post
from requests.exceptions import RequestException

from system_agent.core.tool_executor import Tool

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, url: str, model_name: str, tools: list[dict]) -> None:
        self.model_name = model_name
        self.temperature = 0.3
        self.url = url
        self.tools = tools

    def get_tool(self, query: str) -> Tool:
        messages = [{"role": "user", "content": query}]

        def _as_spec(tool_declaration: dict) -> dict:
            params = {}
            if len(tool_declaration.get("parameters")):
                properties = {}
                for param in tool_declaration.get("parameters"):
                    properties[param["name"]] = {
                        "type": param["type"],
                        "description": param["description"],
                    }
                params = {"type": "object", "properties": properties}
            return {
                "type": "function",
                "function": {
                    "name": tool_declaration.get("name"),
                    "description": tool_declaration.get("description"),
                    "parameters": params,
                },
            }

        try:
            body = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "stream": False,
                "tools": list(map(_as_spec, self.tools)),
            }
            logger.debug(
                f"calling LLM with query: '{query}' with tools: {[tool['name'] for tool in self.tools]}"
            )
            response = post(self.url, json=body)
            content = response.json()["choices"][0]["message"]["content"]
            logger.debug(f"LLM response: {content}")
            tool_call = loads(content)

            for tool in self.tools:
                if tool["name"] == tool_call["name"]:
                    return Tool(
                        name=tool["name"],
                        command=tool["command"],
                        args=list(tool_call["arguments"].values()),
                    )
            return Tool(
                name="echo", command="echo", args=["couldn't detect the command"]
            )
        except (RequestException, KeyError) as e:
            logger.error(f"LLM request failed: {e}")
            return Tool(
                name="echo", command="echo", args=["couldn't detect the command"]
            )
