# Project Overview

This project is about learning how to build an AI agent, following a course from [boot.dev](https://www.boot.dev).

## Progress So Far

1. Set up API calling to the LLM using OpenRouter and the Python OpenAI SDK.
2. Wrote tools as plain Python functions — listing directory contents, reading a file, writing to a file, and running a Python file.
3. Generated metadata (JSON schemas) for these functions and passed them to the LLM as tools it can choose to call.
4. Handled the LLM's tool call by dispatching to the matching function and returning the result.
