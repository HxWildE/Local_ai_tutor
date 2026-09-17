import os
import time
from pypdf import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai
from pinecone import Pinecone

# Load Environment Variables
load_dotenv()

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "ai-tutor-index")

pc = None
index = None

if PINECONE_API_KEY:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    # Get the index
    try:
        index = pc.Index(INDEX_NAME)
    except Exception as e:
        print(f"Warning: Could not connect to Pinecone index: {e}")

def get_embedding(text):
    """Generate embedding using Google Gemini's embedding model."""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key is not set.")
    
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document",
        title="Document chunk"
    )
    return result['embedding']

def extract_text(file_path):
    """Extract text from PDF or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    return text

def add_document(file_path):
    """Extracts text, creates embeddings, and uploads to Pinecone."""
    if not index:
        raise ValueError("Pinecone index is not initialized. Check API keys.")

    print(f"Indexing document: {file_path}")
    text = extract_text(file_path)
    
    if not text.strip():
        print("Document is empty.")
        return

    # Semantic Chunking (split by double newline, keeping meaningful paragraphs)
    raw_chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip() and len(chunk.strip()) > 50]
    
    vectors_to_upsert = []
    
    for i, chunk in enumerate(raw_chunks):
        try:
            embedding = get_embedding(chunk)
            # Pinecone requires unique IDs for each vector
            vector_id = f"{os.path.basename(file_path)}-chunk-{i}-{int(time.time())}"
            
            # We store the raw text as metadata so we can retrieve it later
            vectors_to_upsert.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {"text": chunk, "source": os.path.basename(file_path)}
            })
            
            # Batch upsert every 50 chunks to avoid limits
            if len(vectors_to_upsert) >= 50:
                index.upsert(vectors=vectors_to_upsert)
                vectors_to_upsert = []
                time.sleep(1) # Rate limit protection
                
        except Exception as e:
            print(f"Error processing chunk {i}: {e}")
            
    # Upsert remaining chunks
    if vectors_to_upsert:
        index.upsert(vectors=vectors_to_upsert)
        
    print(f"Successfully uploaded {len(raw_chunks)} chunks to Pinecone!")
