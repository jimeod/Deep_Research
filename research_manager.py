import asyncio
import re
from datetime import datetime
from pathlib import Path
from agents import Runner, trace
from model_config import USE_EMAIL,HOW_MANY_SEARCHES
from search_agent import search_agent
from search_tool import web_search 
from planner_agent import planner_agent,WebSearchItem,WebSearchPlan
from writer_agent import writer_agent,writer_agent_plain,ReportData
from emailer import send_report_email

REPORTS_DIR=Path("reports")
MAX_TRIES=2

async def run_with_retry(agent,input_message:str,tries:int=MAX_TRIES):
    last_error =None
    for attempt in range(1,tries +1):
        try:
            return await Runner.run(agent,input_message)
        except Exception as e:
            last_error=e
            print(f"[{agent.name}] intento {attempt}/{tries} falló: {e}")
    raise last_error


class ResearchManager:

    async def run(self,query:str):
        if not query or not query.strip():
            yield "Escribe una pregunta para investigar"
            return

        with trace("Research trace"):
            yield "Iniciando investigación (modelo local: puede tardar unos minutos)..."
            search_plan = await self.plan_searches(query)

            yield f"Búsquedas planificadas: {len(search_plan.searches)}. Buscando en DuckDuckGo y resumiendo..."
            search_results= await self.perform_searches(search_plan)

            yield "Búsquedas listas, escribiendo el informe..."
            report = await self.write_report(query,search_results)

            path = self.save_report(query,report)
            status = f"Informe escrito y guardado en {path}."

            if USE_EMAIL:
                yield status + " Enviando email..."
                try:
                    await asyncio.to_thread(send_report_email, query, report.markdown_report)
                    status = "Email enviado"
                except Exception as e:
                    status= f"No se pudo enviar el email ({e}), pero el informe sí se guardó."
                yield status

            yield self.format_final(report, path)

    async def plan_searches(self,query:str)-> WebSearchPlan:
        try:
            result= await run_with_retry(planner_agent,f"Query: {query}")
            plan= result.final_output 
            if plan.searches:
                return WebSearchPlan(searches=plan.searches[:HOW_MANY_SEARCHES])
        except Exception as e:
            print (f"[Planner] falló, uso la pregunta como búsqueda única: {e}")

        return WebSearchPlan(searches=[WebSearchItem(reason="Fallback: search the query directly", query=query)])

    async def perform_searches(self,search_plan:WebSearchPlan)->list[str]:
        tasks=[self.search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)

    async def search(self, item: WebSearchItem)->str:
        raw_results = await web_search(item.query)
        input_message =(
            f"Search term: {item.query}\nReason for searching: {item.reason}\n\n"
            f"Raw search results:\n{raw_results}"
        )
        try:
            result = await run_with_retry(search_agent,input_message)
            return result.final_output
        except Exception as e:
            return f"(No se pudo resumir la búsqueda '{item.query}': {e})"

    async def write_report(self,query:str,search_results:list[str])->ReportData:
        input_message = f"Original query: {query}\nSummarized search results: {search_results}"
        try:
            result = await run_with_retry(writer_agent,input_message)
            return result.final_output
        except Exception as e:
            print(f"[Writer] salida estructurada falló, uso modo texto simple: {e}")
            result = await run_with_retry(writer_agent_plain, input_message)
            return ReportData(
                short_summary="(Informe generado en modo texto simple)",
                markdown_report=result.final_output,
                follow_up_questions=[],
            )

    def save_report(self,query:str, report:ReportData)->Path:
        REPORTS_DIR.mkdir(exist_ok=True)
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", query).strip("-").lower()[:50] or "report"
        path = REPORTS_DIR / f"{datetime.now():%Y%m%d-%H%M%S}-{slug}.md"
        path.write_text(
            f"# {query}\n\n> {report.short_summary}\n\n{report.markdown_report}\n", encoding="utf-8"
        )
        return path

    def format_final(self,report:ReportData,path:Path)->str:
        text = report.markdown_report
        if report.follow_up_questions:
            text += "\n\n## Preguntas para seguir investigando\n\n"
            text += "\n".join(f"- {q}" for q in report.follow_up_questions)
        text += f"\n\n---\n*Informe guardado en `{path}`*"
        return text




