# 🧠 2. Deep Dive Concepts (Interview Core)

Is document mein hum RAG ke andar ke concepts ko deeply break down karenge kyunki Accenture aise hi fundamental sawal poochta hai.

## 1. What are Embeddings?
Embeddings ek tarah ka mathematical representation hain. Computers English language nahi samajhte, wo sirf numbers samajhte hain. Embedding models (jaise Google ka `embedding-001`) kisi bhi sentence ko ek lambi number line (array) mein convert kar dete hain. 
*Example:* Agar array 768 length ka hai, toh usme har number sentence ki ek khasiyat (feature) batata hai (jaise tone, topic, grammar). 
Jo sentences meaning mein similar hote hain (e.g. "Puppy" and "Dog"), unke vectors space mein ek dusre ke bohot kareeb hote hain.

## 2. Why Pinecone (Vector Database) instead of SQL/MongoDB?
Normal databases (MySQL, MongoDB) **Keyword Search** (Exact Match) par kaam karte hain. Agar user ne search kiya "Newton", toh DB wahi line return karega jisme strictly "Newton" likha ho. 
Lekin Vector databases **Semantic Search (Meaning Search)** par kaam karte hain. 
Pinecone mathematical distance calculate karta hai. Agar user puche "Gravity laws", toh Vector DB "Newton's second law" wala paragraph utha layega kyunki unka *meaning* close hai, bhale hi unme exact words match na ho rahe hon. Isliye RAG ke liye Vector DBs compulsory hain.

## 3. What is Cosine Similarity?
Jab hum Vector DB se search karte hain, toh DB internally do vectors ke beech ka angle check karta hai. 
Agar do vectors ek hi direction mein point kar rahe hain (angle 0 degree), toh unki cosine similarity 1 hoti hai (Matlab 100% same meaning). Agar angle 90 degree hai, toh similarity 0 hoti hai (Totally unrelated). Vector DB humesha top Cosine Similarity wale chunks return karta hai.

## 4. Chunking strategies and limitations
**Chunking kya hai?** Kisi badi PDF ko chote parts mein todna. 
Agar humne chunk size bohot bada rakha, toh LLM confuse ho jayega ki itne bade paragraph mein se answer kahan hai, aur token cost bohot ayegi. 
Agar chunk size bohot chota rakha (e.g., 2 words), toh sentence ka meaning loose ho jayega (Loss of context).
*Best Practice:* Hum 500-1000 characters ka chunk size use karte hain with "Overlap". Overlap matlab agar pehla chunk "A to B" hai, toh dusra chunk "B se C" hoga. Aisa isliye taaki koi important baat do chunks ke beech mein kat na jaye.

## 5. RAG vs Fine-Tuning
Interviewer pakka puchega: *"Apne private documents ke liye tumne model ko Fine-Tune kyu nahi kiya, RAG kyu use kiya?"*
**Your Answer:** "Fine-tuning is extremely expensive, time-consuming, and hard to update. Agar kal ko PDF mein ek line change ho gayi, toh mujhe pura model dobara fine-tune karna padega. 
Lekin RAG mein, main simply purana PDF delete karke naya PDF Pinecone mein daal dunga, instantly knowledge update ho jayegi bina kisi training ke. Plus, RAG hallucinations (lying) ko prevent karta hai kyunki LLM ko specifically source documents se padh ke answer dene ko kaha jata hai."
