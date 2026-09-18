declared_tools = {
    "check_disk_space": {
        "description": "Check how much space is left on the disk",
        "parameters": {},
    },
    "check_current_user": {
        "description": "Check the current logged in user",
        "parameters": {},
    },
    "check_internet": {
        "description": "check if the internet is working",
        "parameters": {},
    },
    "list_files": {
        "description": "list files in the directory requested by the user",
        "parameters": {},
    },
    "check_cpu_usage": {
        "description": "check the CPU usage",
        "parameters": {},
    },
}


class CLITool:
    def __init__(self, name: str) -> None:
        self.name = name
        self.description = ""
        self.params: dict = []
        self.args: list[str] = []

    def as_spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.params,
            },
        }

    def __str__(self) -> str:
        return f"tool: {self.name}\nargs: {self.args}"


def available_tools() -> list[dict]:
    tools = []
    for name in declared_tools:
        tool = CLITool(name)
        tool.description = declared_tools[name]["description"]
        tool.params = declared_tools[name]["parameters"]
        tools.append(tool)

    return [tool.as_spec() for tool in tools]
