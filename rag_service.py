import os
import re
import json
import math
import numpy as np
from google import genai
from google.genai import types

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "data", "documents")
STORE_FILE = os.path.join(BASE_DIR, "data", "vector_store.json")

# Initialize Gemini Client
# It will automatically pick up GEMINI_API_KEY from environment.
# If missing, it will throw an error when used, which we handle by falling back to TF-IDF.
api_key = os.environ.get("GEMINI_API_KEY")
client = None
if api_key:
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini Client: {e}")
else:
    print("Warning: GEMINI_API_KEY environment variable is not set. Using TF-IDF fallback.")

# Global state for in-memory vector store
chunks_db = []
tf_idf_vectorizer = None

# --- Pure Python TF-IDF Vectorizer for Offline/Fallback Mode ---
class SimpleTFIDF:
    def __init__(self):
        self.vocab = {}
        self.idf = {}
        self.doc_count = 0

    def fit_transform(self, texts):
        self.doc_count = len(texts)
        # Tokenize and build vocabulary
        tokenized_docs = [self._tokenize(t) for t in texts]
        
        # Calculate Term Frequency (TF)
        dfs = {}
        for doc in tokenized_docs:
            unique_tokens = set(doc)
            for token in unique_tokens:
                dfs[token] = dfs.get(token, 0) + 1
        
        # Calculate Inverse Document Frequency (IDF)
        self.vocab = {token: idx for idx, token in enumerate(dfs.keys())}
        self.idf = {token: math.log((1 + self.doc_count) / (1 + df)) + 1 for token, df in dfs.items()}
        
        # Build vectors
        vectors = []
        for doc in tokenized_docs:
            vector = self._vectorize(doc)
            vectors.append(vector)
        return np.array(vectors)

    def transform(self, text):
        tokens = self._tokenize(text)
        return self._vectorize(tokens)

    def _tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def _vectorize(self, tokens):
        vector = np.zeros(len(self.vocab))
        if not tokens:
            return vector
        # Count frequencies
        tf = {}
        for token in tokens:
            if token in self.vocab:
                tf[token] = tf.get(token, 0) + 1
        
        # L2 Normalize
        for token, count in tf.items():
            idx = self.vocab[token]
            vector[idx] = count * self.idf[token]
            
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector

# --- Chunking Helper ---
def chunk_text(text, max_chars=800, overlap=150):
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        # Try to break at a space if we're not at the end
        if end < len(text):
            space_idx = text.rfind(' ', start, end)
            if space_idx > start:
                end = space_idx
        chunks.append(text[start:end].strip())
        start = end - overlap
        if start >= len(text) - overlap:
            break
    return chunks

# --- Loading and Indexing ---
def load_and_index_documents(force_rebuild=False):
    global chunks_db, tf_idf_vectorizer
    
    # If store exists and not force_rebuild, load from file
    if not force_rebuild and os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                chunks_db = data["chunks"]
                # Convert list back to numpy arrays for embeddings
                for chunk in chunks_db:
                    if chunk.get("embedding") is not None:
                        chunk["embedding"] = np.array(chunk["embedding"])
                
                # Fit TF-IDF on loaded chunks
                texts = [c["content"] for c in chunks_db]
                tf_idf_vectorizer = SimpleTFIDF()
                tf_idf_vectorizer.fit_transform(texts)
                print(f"Loaded {len(chunks_db)} chunks from local cache.")
                return
        except Exception as e:
            print(f"Error loading cache: {e}. Reindexing...")

    # Otherwise, read all source files
    print("Indexing documents...")
    chunks_db = []
    if not os.path.exists(DOCS_DIR):
        print(f"Error: Documents directory {DOCS_DIR} does not exist.")
        return

    doc_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    
    for filename in doc_files:
        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
            
        # Parse metadata
        meta_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", file_content, re.DOTALL)
        metadata = {}
        content_body = file_content
        
        if meta_match:
            try:
                metadata = json.loads(meta_match.group(1))
                content_body = file_content[meta_match.end():]
            except Exception as e:
                print(f"Error parsing metadata in {filename}: {e}")
        
        # Chunk the content body
        chunks = chunk_text(content_body)
        for idx, chunk_text_content in enumerate(chunks):
            chunks_db.append({
                "doc_id": metadata.get("id", filename),
                "title": metadata.get("title", filename),
                "category": metadata.get("category", "General"),
                "classification": metadata.get("classification", "Public"),
                "chunk_index": idx,
                "content": chunk_text_content,
                "embedding": None
            })

    # Fit TF-IDF on all text contents
    texts = [c["content"] for c in chunks_db]
    tf_idf_vectorizer = SimpleTFIDF()
    tf_idf_vectorizer.fit_transform(texts)

    # Compute Gemini embeddings if client is active
    gemini_success = False
    if client:
        try:
            print("Generating Gemini embeddings...")
            # Embed in batches to be efficient
            batch_size = 50
            for i in range(0, len(chunks_db), batch_size):
                batch = chunks_db[i:i+batch_size]
                batch_texts = [c["content"] for c in batch]
                
                # Call Gemini embedding API
                response = client.models.embed_content(
                    model="text-embedding-004",
                    contents=batch_texts
                )
                
                for idx, emb_data in enumerate(response.embeddings):
                    batch[idx]["embedding"] = np.array(emb_data.values)
            gemini_success = True
            print("Gemini embeddings generated successfully.")
        except Exception as e:
            print(f"Failed to generate Gemini embeddings: {e}. Falling back to TF-IDF.")
            gemini_success = False

    # Save to store file
    save_data = []
    for chunk in chunks_db:
        emb_list = None
        if chunk["embedding"] is not None:
            emb_list = chunk["embedding"].tolist()
        save_data.append({
            "doc_id": chunk["doc_id"],
            "title": chunk["title"],
            "category": chunk["category"],
            "classification": chunk["classification"],
            "chunk_index": chunk["chunk_index"],
            "content": chunk["content"],
            "embedding": emb_list
        })
        
    os.makedirs(os.path.dirname(STORE_FILE), exist_ok=True)
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump({"chunks": save_data, "uses_gemini_embeddings": gemini_success}, f, indent=2)
    print(f"Indexed {len(chunks_db)} chunks. Vector store saved to {STORE_FILE}.")

# --- Search & Retrieval ---
def retrieve_similar_chunks(query, k=4):
    global chunks_db, tf_idf_vectorizer
    if not chunks_db:
        load_and_index_documents()
        
    if not chunks_db:
        return []

    # Check if we should use Gemini embeddings or TF-IDF
    has_gemini_embeddings = all(c.get("embedding") is not None for c in chunks_db)
    
    query_vector = None
    if has_gemini_embeddings and client:
        try:
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=query
            )
            query_vector = np.array(response.embeddings[0].values)
        except Exception as e:
            print(f"Error computing query embedding with Gemini: {e}. Using TF-IDF.")
            query_vector = None

    if query_vector is not None:
        # Cosine Similarity using Gemini embeddings
        similarities = []
        for chunk in chunks_db:
            dot_prod = np.dot(query_vector, chunk["embedding"])
            norm_q = np.linalg.norm(query_vector)
            norm_c = np.linalg.norm(chunk["embedding"])
            sim = dot_prod / (norm_q * norm_c) if (norm_q * norm_c) > 0 else 0
            similarities.append((chunk, float(sim)))
    else:
        # Fallback: Cosine Similarity using TF-IDF
        query_vector = tf_idf_vectorizer.transform(query)
        similarities = []
        for chunk in chunks_db:
            chunk_vector = tf_idf_vectorizer.transform(chunk["content"])
            dot_prod = np.dot(query_vector, chunk_vector)
            norm_q = np.linalg.norm(query_vector)
            norm_c = np.linalg.norm(chunk_vector)
            sim = dot_prod / (norm_q * norm_c) if (norm_q * norm_c) > 0 else 0
            similarities.append((chunk, float(sim)))

    # Sort by similarity descending
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:k]

# --- RAG Synthesis ---
def generate_rag_answer(query, history=None):
    global client
    # 1. Retrieve top context
    similar_chunks = retrieve_similar_chunks(query, k=4)
    
    # 2. Build prompt context
    context_str = ""
    for idx, (chunk, score) in enumerate(similar_chunks):
        context_str += f"[{idx + 1}] Source: {chunk['title']} | Category: {chunk['category']} | Classification: {chunk['classification']} (Score: {score:.3f})\n"
        context_str += f"Content: {chunk['content']}\n\n"
        
    # 3. Construct System Prompt
    system_prompt = (
        "You are the Galactic Archive Chatbot, a highly intelligent virtual archivist for the Galactic Federation.\n"
        "Your task is to answer user queries using ONLY the retrieved context fragments provided below. "
        "Strictly adhere to the following rules:\n"
        "1. Answer the question accurately based on the context.\n"
        "2. If the context does not contain the answer, say exactly: 'I cannot find the answer to this question in the Galactic Archive.' Do not invent information.\n"
        "3. Provide clear citations. Format your answer in markdown and end with a 'Sources Cited' section lists the documents you retrieved (with their category and classification)."
    )

    # Convert conversation history if present
    messages = []
    if history:
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            messages.append(types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            ))
            
    # Add current prompt
    current_prompt = f"Context:\n{context_str}\n\nUser Question: {query}\n\nAnswer:"
    messages.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=current_prompt)]
    ))

    # Synthesize answer using Gemini
    answer_text = ""
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2
                )
            )
            answer_text = response.text
        except Exception as e:
            answer_text = f"Error generating answer with Gemini API: {e}\n\nFalling back to context summary."
    else:
        # Standalone simple offline synthesis if no Gemini API key
        answer_text = "### Galactic Archive Fallback Response (Offline Mode)\n\n"
        answer_text += "It appears I am running in offline mode. Here are the relevant passages from the archives:\n\n"
        for idx, (chunk, score) in enumerate(similar_chunks):
            answer_text += f"* **From {chunk['title']}** (Score: {score:.2f}):\n  _{chunk['content']}_\n\n"
            
    return {
        "answer": answer_text,
        "sources": [
            {
                "doc_id": c["doc_id"],
                "title": c["title"],
                "category": c["category"],
                "classification": c["classification"],
                "score": score,
                "content": c["content"]
            }
            for c, score in similar_chunks
        ]
    }

if __name__ == "__main__":
    # Test indexing
    load_and_index_documents(force_rebuild=True)
    
    # Test search
    test_query = "What is the Void Whisper signal?"
    print(f"\nTesting Retrieval for: '{test_query}'")
    results = retrieve_similar_chunks(test_query, k=2)
    for c, score in results:
        print(f"- {c['title']} (Score: {score:.2f}): {c['content'][:100]}...")
        
    print("\nTesting RAG synthesis...")
    ans = generate_rag_answer(test_query)
    print(ans["answer"])
