conversations = {}


def get_history(conversation_id: str):
    return conversations.get(conversation_id, [])


def add_message(conversation_id: str, role: str, content: str):
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    conversations[conversation_id].append({
        "role": role,
        "content": content
    })