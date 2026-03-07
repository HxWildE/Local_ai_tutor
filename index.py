import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from pypdf import PdfReader
from tkinter import Tk,filedialog

def build_index():
    os.makedirs("vector_store", exist_ok=True)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load syllabus
    with open("documents/data.txt", "r", encoding="utf-8") as f:
            text = f.read()

    chunks = text.split("\n\n")

    # Create embeddings
    embeddings = model.encode(chunks)
    embeddings = embeddings / np.linalg.norm(embeddings,axis = 1, keepdims=True)

    index = faiss.IndexFlatIP(384)
    # It stores Cosines actually (manualll ypassed 384 dimensions).
    index.add(embeddings)

    # Save index
    faiss.write_index(index, "vector_store/index.faiss")

    # Save chunks separately
    with open("vector_store/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

def add_document(file_path):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    if not os.path.exists(file_path):
        print("File not found")
        return

    print(f"Indexing: {file_path}")

        # read file
    ext = os.path.splitext(file_path)[1]

    if ext == ".pdf":  #check fr PDF extension
        text = read_pdf(file_path)

    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    chunks = text.split("\n\n")

    embeddings = model.encode(chunks)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # load existing index
    index = faiss.read_index("vector_store/index.faiss")

    # load existing chunks
    with open("vector_store/chunks.pkl", "rb") as f:
        old_chunks = pickle.load(f)

    index.add(embeddings)

    old_chunks.extend(chunks)

    # save updated index
    faiss.write_index(index, "vector_store/index.faiss")

    with open("vector_store/chunks.pkl", "wb") as f:
        pickle.dump(old_chunks, f)

    print(f"Added {len(chunks)} chunks")

def browse_and_add():
    root = Tk()
    root.withdraw()

# withdraw()    → hides the blank window
# If we didn’t hide it, you'd see an ugly empty tkinter window behind the file picker.
    
    file_path = filedialog.askopenfilename(
        title="Select files to Upload",
        filetypes = [("Text files","*.txt"),("All files","*.*")]
    )

    if file_path:
        add_document(file_path)
    else:
        print("No file selected")
    
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        #fetch each page from pdf , extraxt its text part 
        # No image handling inside  
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text    

if __name__ == "__main__":
    build_index()
    
