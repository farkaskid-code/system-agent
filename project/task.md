# Task 1: LLM Client with Fallback Strategies

## Concept Recap
This task introduces the core pattern of mapping natural language to structured commands, with fallback strategies for when LLMs are unavailable. It establishes the modular architecture that will be extended in later tasks.

## Goal
Implement a basic LLM client that:
1. Accepts natural language queries
2. Maps them to structured commands
3. Provides fallback strategies when LLM is unavailable

## Inputs / Outputs
- Input: Natural language query (e.g., "Show me the disk usage")
- Output: Structured command representation (e.g., {"tool": "df", "args": ["-h"]})

## Constraints
- Must handle both API-based and local model interactions (using Ollama)
- Must implement at least two fallback strategies
- Should be testable with local LLM integration

## Acceptance Criteria
1. [TESTABLE] The client returns a structured command object for valid inputs [TESTABLE]
2. [TESTABLE] Fallback strategies are triggered when LLM is unavailable [TESTABLE]
3. [QUALITATIVE] The code demonstrates clear separation of concerns between LLM interaction and command mapping [QUALITATIVE]
4. [TESTABLE] The client handles at least three different types of natural language queries [TESTABLE]

## Explicitly Out of Scope
- Complex command validation
- Persistent state management