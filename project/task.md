# Task 2: Tool Executor with Secure Execution

## Concept Recap
This task builds on the LLM client's structured command output to implement secure execution of Linux CLI tools. It establishes the foundation for actual system interaction while maintaining security constraints.

## Goal
Implement a secure CLI tool executor that:
1. Runs commands in a sandboxed environment
2. Parses structured output (text, JSON, tables)
3. Validates commands against configured permissions

## Inputs / Outputs
- Input: Structured command from LLM client (e.g., {"tool": "df", "args": ["-h"]})
- Output: Parsed execution result (e.g., {"status": "success", "output": "..."})

## Constraints
- Must implement process sandboxing (resource limits, chroot)
- Must validate commands against tool_permissions.yaml
- Must handle output parsing for common formats

## Acceptance Criteria
1. [TESTABLE] Executor runs valid commands with proper permissions [TESTABLE]
2. [TESTABLE] Sandbox limits prevent resource exhaustion [TESTABLE]
3. [TESTABLE] Output parser handles text, JSON, and table formats [TESTABLE]
4. [QUALITATIVE] Code demonstrates clear separation between execution and parsing concerns [QUALITATIVE]
5. [TESTABLE] Executor correctly rejects unauthorized commands [TESTABLE]

## Explicitly Out of Scope
- Advanced security features (basic sandboxing only)
- Complex error handling for edge cases