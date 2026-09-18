from json import loads

from requests import post
from requests.exceptions import RequestException

from .parser import map_to_command
from .tool_executor import CLITool, available_tools


class LLMClient:
    def __init__(self, url: str, model_name: str) -> None:
        self.model_name = model_name
        self.temperature = 0.3
        self.url = url

    def call_model(self, query: str) -> CLITool:
        messages = [{"role": "user", "content": query}]
        body = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "stream": False,
            "tools": available_tools(),
        }

        try:
            response = post(self.url, json=body)
            content = response.json()["choices"][0]["message"]["content"]
            tool_call = loads(content)
            tool = CLITool(tool_call["name"])
            tool.args = tool_call["arguments"]
            return tool
        except (RequestException, KeyError) as e:
            print(f"LLM request failed because of {e}")
            print("Using manual mapping rules")
            return map_to_command(query)

    def __str__(self) -> str:
        return self.model_name
