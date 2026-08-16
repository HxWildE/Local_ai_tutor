from app.services.ollama_service import generate_response


def summarize(text: str):

    response = generate_response(
        message=f"Summarize this:\n{text}",
        history=[],
        context="",
        mode="tutor"
    )

    return {
        "tool": "summarizer",
        "summary": response
    }