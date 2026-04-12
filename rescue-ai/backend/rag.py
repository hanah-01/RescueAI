from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import os
import numpy as np
import pickle

INDEX_FILE = "data/faiss_index.bin"
CHUNKS_FILE = "data/chunks.pkl"

class DisasterRAG:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        self.chunks = []
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists(INDEX_FILE) and os.path.exists(CHUNKS_FILE):
            print("Loading cached FAISS index...")
            self.index = faiss.read_index(INDEX_FILE)
            with open(CHUNKS_FILE, "rb") as f:
                self.chunks = pickle.load(f)
        else:
            print("Creating FAISS index...")
            self.build_index()

    def build_index(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
        
        for file in os.listdir("data"):
            if file.endswith(".txt"):
                disaster_type = file.replace(".txt", "")
                with open(os.path.join("data", file), "r", encoding="utf-8") as f:
                    doc_text = f.read()
                    
                split_texts = splitter.split_text(doc_text)
                for chunk_text in split_texts:
                    self.chunks.append({"text": chunk_text, "disaster": disaster_type})

        if not self.chunks:
            self.chunks.append({"text": "Escape danger, seek high ground, call 911.", "disaster": "general"})

        texts = [chunk["text"] for chunk in self.chunks]
        self.embeddings = self.model.encode(texts)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))
        
        faiss.write_index(self.index, INDEX_FILE)
        with open(CHUNKS_FILE, "wb") as f:
            pickle.dump(self.chunks, f)

    def retrieve(self, query, top_k=2, disaster_filter=None):
        q_emb = self.model.encode([query])
        
        search_k = min(top_k * 2, len(self.chunks))
        D, I = self.index.search(np.array(q_emb), k=search_k)
        
        results = []
        for i in range(len(I[0])):
            idx = I[0][i]
            if idx == -1: continue
            chunk = self.chunks[idx]
            dist = D[0][i]
            score = 1.0 / (1.0 + dist)
            
            if disaster_filter and chunk["disaster"] == disaster_filter: score += 0.2
            if disaster_filter and disaster_filter.lower() in chunk["text"].lower(): score += 0.1
            results.append((score, chunk))
            
        results.sort(key=lambda x: x[0], reverse=True)
        
        formatted_context = ""
        for i, (score, chunk) in enumerate(results[:top_k]):
            disaster_id = chunk.get("disaster", "alert").upper()
            formatted_context += "[" + disaster_id + "] " + chunk["text"] + "\n"
            
        return formatted_context[:800]

rag_db = DisasterRAG()

def retrieve(query_text: str, disaster_filter: str = None) -> str:
    return rag_db.retrieve(query_text, top_k=2, disaster_filter=disaster_filter)
