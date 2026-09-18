# 🔑 API Keys Setup Guide (Gemini & Pinecone)

Bhai, is naye architecture ke liye tumhe 2 free API keys chahiye hongi. Inko fetch karne mein mushkil se 2 minute lagenge. Jab keys mil jayein, toh bas apni `.env` file mein daal dena.

---

## 1. Google Gemini API Key Kaise Layein? (Free)

1. **Google AI Studio** par jao: [https://aistudio.google.com/](https://aistudio.google.com/)
2. Apne Google Account se login karo.
3. Left sidebar mein **"Get API Key"** par click karo.
4. **"Create API Key"** button dabao. Ek lamba sa alphanumeric code generate hoga.
5. Us key ko copy kar lo. 

---

## 2. Pinecone API Key Kaise Layein? (Free Vector DB)

1. **Pinecone** par jao: [https://www.pinecone.io/](https://www.pinecone.io/)
2. Sign up karo (Google se direct ho jayega).
3. Dashboard mein left sidebar se **"API Keys"** par click karo.
4. Wahan default key already bani hogi, use copy kar lo.

### 2.1 Pinecone mein Index (Database) Banana:
Key lane ke baad, humein ek khali database bhi banana hoga jisme vectors save honge.
1. Pinecone Dashboard pe **"Indexes"** pe jao.
2. **"Create Index"** pe click karo.
3. **Index Name:** `ai-tutor-index` rakh do.
4. **Dimensions:** `768` (Google Gemini Embeddings ki dimension 768 hoti hai, yeh bohot zaroori hai!).
5. **Metric:** `cosine` select rehne do.
6. **Create Index** dabao.

---

## 3. Keys ko `.env` mein save karna

Apne project ke root folder (`MYwebDEvprojects/local_ai_tuto/`) mein ek nayi file banao jiska naam strictly `.env` ho (aur kuch nahi, sirf `.env`).

Us file mein yeh likho:

```env
GEMINI_API_KEY="tumhari_gemini_api_key_yahan_daalo"
PINECONE_API_KEY="tumhari_pinecone_api_key_yahan_daalo"
PINECONE_INDEX_NAME="ai-tutor-index"
```

Bas! Ab hum backend code update karenge jo in keys ko automatically fetch karke use karega.
