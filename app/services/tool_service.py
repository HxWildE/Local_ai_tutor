"""
Tool Service - Implements a Formal Tool Registry Pattern for Local AI Tutor.

The Tool Registry manages tool discovery, routing, argument extraction,
and safe execution, simulating tool-calling agent frameworks.
"""
from typing import Dict, Any, Callable, Tuple, Optional
from app.tools.calculator_tool import calculate
from app.tools.retrieval_tool import retrieve_documents
from app.tools.summarizer_tool import summarize

# Tool Registry map associating tool names with metadata and callable functions
TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "calculator": {
        "name": "calculator",
        "description": "Evaluates mathematical and arithmetic expressions safely.",
        "handler": calculate,
    },
    "retrieval": {
        "name": "retrieval",
        "description": "Searches and retrieves relevant document chunks from the FAISS vector store.",
        "handler": retrieve_documents,
    },
    "summarizer": {
        "name": "summarizer",
        "description": "Generates a concise summary of text input.",
        "handler": summarize,
    }
}

def register_tool(name: str, description: str, handler: Callable):
    """
    Dynamically registers a new tool in the Tool Registry.
    """
    TOOL_REGISTRY[name] = {
        "name": name,
        "description": description,
        "handler": handler
    }

def detect_tool(message: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Detects if the user query requires tool execution, and extracts parameters.
    Implements rule-based intent parsing for tool routing.
    """
    message_lower = message.lower().strip()

    # Rule 1: Calculator detection
    if "calculate" in message_lower or message_lower.startswith("math:") or message_lower.startswith("compute:"):
        expression = (
            message_lower
            .replace("calculate", "")
            .replace("math:", "")
            .replace("compute:", "")
            .strip()
        )
        return "calculator", expression

    # Rule 2: Summarizer detection
    if "summarize" in message_lower or message_lower.startswith("summary:"):
        text_to_summarize = (
            message
            .replace("summarize", "")
            .replace("Summarize", "")
            .replace("summary:", "")
            .replace("Summary:", "")
            .strip()
        )
        return "summarizer", text_to_summarize if text_to_summarize else message

    # Rule 3: Document retrieval explicit query
    if any(keyword in message_lower for keyword in ["document", "notes", "chapter", "search syllabus", "search vector"]):
        return "retrieval", message

    return None, None

def execute_tool(tool_name: str, input_data: str) -> Dict[str, Any]:
    """
    Routes execution to the registered tool handler and returns a standardized response payload.
    """
    if tool_name not in TOOL_REGISTRY:
        return {
            "status": "error",
            "tool": tool_name,
            "error": f"Tool '{tool_name}' is not registered in the Tool Registry.",
            "result": None
        }

    try:
        handler = TOOL_REGISTRY[tool_name]["handler"]
        result = handler(input_data)
        return {
            "status": "success",
            "tool": tool_name,
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "tool": tool_name,
            "error": f"Error executing tool '{tool_name}': {str(e)}",
            "result": None
        }