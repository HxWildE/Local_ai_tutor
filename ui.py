import gradio as gr
from rag import retrieve_context
from app import ask_llm, SYSTEM_PROMPT

def chat(user_message, history):

    context = retrieve_context(user_message)

    if context is None:
        prompt = f"""
        {SYSTEM_PROMPT}

        User:
        {user_message}

        Tutor:
        """

    else:
        prompt = f"""
        You are a strict syllabus-bound AI tutor.

        Context:
        {context}

        User:
        {user_message}

        Tutor:
        """

    reply = ask_llm(prompt)

    return reply


demo = gr.ChatInterface(
    chat,
    title="Local AI Tutor",
    description="RAG powered tutor using Ollama + FAISS"
)

demo.launch()