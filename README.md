# 🤖 Cloud-Native AI Tutor

A Serverless RAG application built with Streamlit, powered by Google Gemini API and Pinecone Vector DB.

## 🌟 Key Features
- **Cloud-Native RAG Pipeline:** Uses Google Gemini API for fast, semantic document embedding and generation.
- **Scalable Vector Database:** Integrated with Pinecone Vector DB for highly efficient cloud-based document retrieval.
- **ChatGPT-like UI:** Flawless, minimalist UI featuring native inline file attachments directly within the chat box.
- **Multiple Learning Modes:** Features Tutor, Quiz, and Interview modes powered by mode-specific prompt engineering.

## 📂 Project Structure
`	ext
local_ai_tuto/
├── app.py                  # Main Streamlit UI application
├── core/                   # Core Backend Logic
│   ├── rag.py              # Retrieval & Prompt injection logic
│   ├── vector_index.py     # Pinecone index building and document parsing
│   ├── tools.py            # Tool Registry 
│   └── modes.py            # System prompts for learning modes
├── documents/              # Stored PDFs/Text files uploaded by user
├── .env                    # Environment variables (API Keys)
├── requirements.txt        # Python dependencies
└── README.md
`

## 🚀 Quick Start

1. **Install Dependencies:**
   `ash
   pip install -r requirements.txt
   `

2. **Configure API Keys:**
   Create a .env file in the root directory and add your keys:
   `env
   GEMINI_API_KEY="your_gemini_api_key"
   PINECONE_API_KEY="your_pinecone_api_key"
   PINECONE_INDEX_NAME="ai-tutor-index"
   `

3. **Start the Frontend:**
   `ash
   streamlit run app.py
   `

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **LLM Engine:** Google Gemini API (gemini-flash-latest)
- **Vector Database:** Pinecone
- **Document Parsing:** PyPDF
