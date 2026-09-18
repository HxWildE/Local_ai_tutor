import os

file_path = 'app.py'

new_code = '''import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from core.rag import retrieve_context
from core.vector_index import add_document

# Load Keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Cloud-Native AI Tutor", page_icon="🤖", layout="centered")
st.title("🤖 Cloud-Native AI Tutor")
st.markdown("A Serverless, Privacy-First RAG application powered by **Gemini Pro** and **Pinecone**.")

if not GEMINI_API_KEY:
    st.error("🔑 Gemini API Key not found! Please check your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

SYSTEM_PROMPT = \"\"\"
YOU ARE A CONVERSATIONAL AI TUTOR.
Explain concepts clearly. Use examples.
Keep explanations structured.
If the student seems confused, simplify further.
ALWAYS base your answers on the provided context if available.
\"\"\"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def ask_llm_stream(prompt):
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\\n\\n**Error connecting to Gemini API:** {str(e)}"

if prompt := st.chat_input("Ask me anything or attach a PDF to index...", accept_file="multiple", file_type=["pdf", "txt"]):
    
    # Handle file uploads if any are attached
    if prompt.get("files"):
        with st.spinner("Indexing documents to cloud..."):
            os.makedirs("documents", exist_ok=True)
            for uploaded_file in prompt["files"]:
                temp_path = os.path.join("documents", uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    add_document(temp_path)
                    st.success(f"✅ {uploaded_file.name} indexed successfully!")
                except Exception as e:
                    st.error(f"❌ Error indexing {uploaded_file.name}: {e}")

    # Handle chat text if any is provided
    if prompt.text:
        user_input = prompt.text
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Searching Knowledge Base..."):
            context = retrieve_context(user_input)
        
        if context:
            full_prompt = f"{SYSTEM_PROMPT}\\n\\nUse the context below to answer.\\n\\nContext:\\n{context}\\n\\nUser:\\n{user_input}\\n\\nTutor:"
        else:
            full_prompt = f"{SYSTEM_PROMPT}\\n\\nUser:\\n{user_input}\\n\\nTutor:"

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in ask_llm_stream(full_prompt):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
'''

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_code)
print('UI Updated with integrated chat input')
