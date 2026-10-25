import asyncio

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS 

def web_search_sync(query:str,max_results:int =5)->str:
    try:
        results= DDGS().text(query,max_results=max_results)
    except Exception as e:
        return f"Search failed: {e}"
    if not results:
        return "No results found."
    return "\n\n".join(
        f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}" for r in results
    )


async def web_search(query:str)->str:
    return await asyncio.to_thread(web_search_sync,query)
