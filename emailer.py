import html
from messenger import send_email


def markdown_to_html(md_text:str)->str:
    try:
        import markdown
        body = markdown.markdown(md_text,extensions=["tables","fenced_code"])
    except ImportError:
        body = f"<pre>{html.escape(md_text)}</pre>"
    return(
        "<html><body style=\"font-family: Arial, sans-serif; max-width: 800px; margin: auto; line-height: 1.6;\">"
        f"{body}</body></html>"
    )

def send_report_email(title:str,markdown_report:str)->None:
    send_email(f"Deep Research: {title}", markdown_report, markdown_to_html(markdown_report))