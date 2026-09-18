from system_agent.core.tool_executor import CLITool


def map_to_command(query: str) -> CLITool:
    if "disk space" in query:
        return CLITool("check_disk_space")
    elif "show me the current user" == query:
        return CLITool("check_current_user")
    elif "check internet connection" == query:
        return CLITool("check_internet")
    elif "list files" in query:
        return CLITool("list_files")
    elif "CPU usage" in query:
        return CLITool("check_cpu_usage")
    else:
        return CLITool("unknown")
