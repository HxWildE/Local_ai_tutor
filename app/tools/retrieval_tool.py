from app.services.rag_service import rag_service

def retrieve_documents(query: str):

    context = rag_service.retrieve_context(query)

    return {
        "tool": "retrieval",
        "context": context
    }