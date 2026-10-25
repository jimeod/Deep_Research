# Deep Research (my free version)

A web app that **researches any topic on the internet and writes a report**, using a team of AI agents.
It works **100% free**: it runs a local model with [Ollama](https://ollama.com) and searches with DuckDuckGo, so no paid API keys are needed.

![Screenshot of the Deep Research web app](<front-desing/Captura de pantalla 2026-10-24 a la(s) 7.19.00 p.m..png>)

## What it does

1. You type a question (for example, _"Most popular AI Agent frameworks in 2026"_).
2. An agent **plans** which searches to run.
3. The code **searches DuckDuckGo** and another agent **summarizes** each result.
4. An agent **writes the full report** in Markdown.
5. The report is **saved** in the `reports/` folder and, optionally, **sent by email**.

The orchestration is done **in code** (`research_manager.py`): each step is a separate call to an agent, with retries and fallback plans in case the model fails.

## Tech stack

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) (connected to Ollama)
- [Ollama](https://ollama.com) with `llama3.2`
- [Gradio](https://www.gradio.app) for the web interface
- [Pydantic](https://docs.pydantic.dev) for structured outputs
- [ddgs](https://pypi.org/project/ddgs/) for searching DuckDuckGo
