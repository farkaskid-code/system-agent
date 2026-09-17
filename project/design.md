# Project: Miniature OpenClaw for LLM Tooling Learning

## Overview
A simplified, educational LLM tooling framework focused on Linux system interaction. This project teaches core patterns for building LLM-powered task runners while providing practical value through system diagnostics, automation, and security auditing capabilities.

## Core Concepts
1. **LLM Harness Architecture**
   - Modular design for LLM interaction (CLI, API, local models)
   - Natural language → structured command mapping
   - Fallback strategies for LLM unavailability

2. **Persistent State Management**
   - File-based storage for:
     - Historical system metrics
     - Tool execution logs
     - User preferences
   - Trade-offs between memory persistence and performance

3. **Tool Integration**
   - Secure execution of Linux CLI tools (rsync, nmap, docker)
   - Parsing structured output (text, JSON, tables)
   - Command validation and sandboxing

4. **Model-Agnostic Design**
   - Configurable LLM backends (OpenAI, local Llama)
   - Configuration management for tool permissions and arguments
   - Secure logging and sensitive data handling

## Architecture
```
project-root/
├── core/
│   ├── llm_client.py        # LLM interaction with fallback strategies
│   ├── tool_executor.py     # CLI/tool execution with sandboxing
│   ├── memory.py            # File-based state retention (JSON, logs)
│   └── parser.py            # Natural language → structured command mapping
├── tools/
│   ├── system_monitor.py    # System diagnostics (top, iostat)
│   ├── security_auditor.py  # Security tools (nmap, lynis)
│   └── dev_tools.py         # Development automation (black, rsync)
├── config/
│   ├── llm_providers.yaml   # LLM API keys and configurations
│   └── tool_permissions.yaml# Tool execution rules and restrictions
├── examples/
│   ├── system_diagnostic.md # Example: "What is using excessive CPU?"
│   ├── task_automation.md   # Example: "Back up /home/user/data"
│   └── security_scan.md     # Example: "Scan for open ports"
└── tests/
    ├── test_tool_executor.py
    └── test_parser.py
```

## Key Decisions
- **Scope Focus**: Linux-only CLI tool integration (no cross-platform support)
- **Security Model**: Tool execution sandboxed via `subprocess` with strict permissions
- **State Management**: Simple file-based storage for historical metrics and logs
- **Model-Agnostic Design**: Configurable LLM backends with fallback to rule-based logic

## Known Trade-offs / Deferred Items
- [ ] Cross-platform support (currently Linux-only)
- [ ] Advanced security features (basic implementation first)
- [ ] Complex workflow pipelines (simplified version first)
- [ ] Mobile device support (deferred to later stages)