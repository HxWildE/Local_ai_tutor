from app.services.rag_service import rag_service

def retrieve_documents(query: str) -> dict:
    """
    Executes similarity search and reranking on vector database for user query.
    """
    try:
        context = rag_service.retrieve_context(query)
        if not context:
            return {
                "tool": "retrieval",
                "status": "success",
                "context": "No matching knowledge base documents found for the query.",
                "has_context": False
            }
        return {
            "tool": "retrieval",
            "status": "success",
            "context": context,
            "has_context": True
        }
    except Exception as e:
        return {
            "tool": "retrieval",
            "status": "error",
            "error": f"Failed to retrieve documents: {str(e)}",
            "context": "",
            "has_context": False
        }