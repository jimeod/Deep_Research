from agents import Agent 
from model_config import MODEL

INSTRUCTIONS= """
You are a research assistant. You are given a search term an the raw web search results for it.
Produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""

search_agent = Agent(name="Search Agent",instructions=INSTRUCTIONS,model=MODEL)