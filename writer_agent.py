from pydantic import BaseModel,Field
from agents import Agent
from model_config import MODEL, REPORT_LANGUAGE

INSTRUCTIONS = f"""
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some research.
Generate a detailed report based on the research and the query.
The final output should be in markdown format. Aim for at least 500 words.
Write the report in {REPORT_LANGUAGE}.
"""

class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")

writer_agent = Agent(name="Writer Agent", instructions=INSTRUCTIONS, model=MODEL, output_type=ReportData)


writer_agent_plain = Agent(
    name="Writer Agent (plain)",
    instructions=INSTRUCTIONS + "\nReply only with the markdown report.",
    model=MODEL,
)
