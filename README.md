# Deep Research (mi versión gratis)

Una app web que **investiga cualquier tema por internet y escribe un informe**, usando un equipo de agentes de IA.
Funciona **100% gratis**: usa un modelo local con [Ollama](https://ollama.com) y busca con DuckDuckGo, sin claves de pago.

<!-- ![Captura de la app](docs) -->

![alt text](<front-desing/Captura de pantalla 2026-10-24 a la(s) 7.19.00 p.m..png>)

##  Qué hace

1. Escribes una pregunta (por ejemplo, _"Most popular AI Agent frameworks in 2026"_).
2. Un agente **planifica** qué búsquedas hacer.
3. El código **busca en DuckDuckGo** y otro agente **resume** cada resultado.
4. Un agente **escribe el informe** completo en Markdown.
5. El informe se **guarda** en la carpeta `reports/` y, si quieres, se **envía por email**.

La orquestación se hace **por código** (`research_manager.py`): cada paso es una llamada separada a un agente, con reintentos y planes de respaldo si el modelo falla.

## Tecnologías

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) (conectado a Ollama)
- [Ollama](https://ollama.com) con `llama3.2`
- [Gradio](https://www.gradio.app) para la interfaz web
- [Pydantic](https://docs.pydantic.dev) para las salidas estructuradas
- [ddgs](https://pypi.org/project/ddgs/) para buscar en DuckDuckGo
