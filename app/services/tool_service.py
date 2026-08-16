from app.tools.calculator_tool import calculate
from app.tools.retrieval_tool import retrieve_documents
from app.tools.summarizer_tool import summarize

def execute_tool(
    tool_name: str,
    input_data: str
):

    if tool_name == "calculator":
        return calculate(input_data)


    elif tool_name == "retrieval":
        return retrieve_documents(input_data)
    elif tool_name == "summarizer":
        return summarize(input_data)

    else:
        return {
            "error": "Unknown tool"
        }

def detect_tool(message: str):

    message = message.lower()


    if "calculate" in message:

        expression = (
            message
            .replace("calculate","")
            .strip()
        )

        return (
            "calculator",
            expression
        )


    if (
        "summarize" in message
        or "summary" in message
    ):

        return (
            "summarizer",
            message
        )


    if (
        "document" in message
        or "notes" in message
        or "chapter" in message
    ):

        return (
            "retrieval",
            message
        )


    return None, None