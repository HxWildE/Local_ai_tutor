import os
from dotenv import load_dotenv
import google.generativeai as genai
from pinecone import Pinecone

# Load Environment Variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "ai-tutor-index")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

pc = None
index = None

if PINECONE_API_KEY:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    try:
        index = pc.Index(INDEX_NAME)
    except Exception as e:
        pass

def get_query_embedding(text):
    """Generate embedding for the search query."""
    if not GEMINI_API_KEY:
        return None
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_query",
        )
        return result['embedding']
    except:
        return None

def retrieve_context(question, top_k=3):
    """Search Pinecone for the most relevant document chunks."""
    if not index or not GEMINI_API_KEY:
        return None

    query_embedding = get_query_embedding(question)
    if not query_embedding:
        return None

    # Search Pinecone
    try:
        response = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Extract text from metadata of matching chunks
        chunks = []
        for match in response['matches']:
            if 'metadata' in match and 'text' in match['metadata']:
                chunks.append(match['metadata']['text'])
                
        if not chunks:
            return None
            
        return "\n\n---\n\n".join(chunks)
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return None
