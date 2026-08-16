from app.services.ollama_service import generate_response

def summarize(text: str) -> dict:
    """
    Summarizes provided text content using the local LLM.
    """
    if not text or not text.strip():
        return {
            "tool": "summarizer",
            "status": "error",
            "error": "No text provided for summarization.",
            "summary": ""
        }

    try:
        response = generate_response(
            message=f"Please provide a concise, high-level summary of the following text:\n\n{text}",
            history=[],
            context="",
            mode="tutor"
        )
        return {
            "tool": "summarizer",
            "status": "success",
            "summary": response
        }
    except Exception as e:
        return {
            "tool": "summarizer",
            "status": "error",
            "error": f"Failed to summarize content: {str(e)}",
            "summary": ""
        }