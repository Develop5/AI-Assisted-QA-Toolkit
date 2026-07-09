"""
AI-Assisted QA Documentation RAG Module
---------------------------------------

This module implements a Retrieval-Augmented Generation (RAG) system
for QA documentation. It allows the AI-Assisted-QA-Toolkit to retrieve
relevant information from internal QA documents and combine it with
LLM reasoning to produce accurate, context-aware answers.

It is designed to support:
- Test case generation
- Script generation
- Log analysis
- Regression optimization
- QA best practices
- Internal standards and policies

Extended Description
--------------------
This module performs the following functions:

- Loads QA documentation files from a local directory.
- Splits documents into chunks for efficient retrieval.
- Generates embeddings for each chunk.
- Stores embeddings in an in-memory vector store.
- Retrieves the most relevant chunks based on user queries.
- Builds a context-aware prompt combining retrieved text + user question.
- Sends the prompt to an LLM backend (OpenAI).
- Returns an answer grounded in your QA documentation.
- Includes an executable example.
- Fully functional: requires OPENAI_API_KEY.

Author: AI-Assisted QA Lead (in transition)
"""

import os
import glob
import json
from typing import List, Tuple
from dataclasses import dataclass

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Install with: pip install openai")

# -----------------------------
# Data Models
# -----------------------------

@dataclass
class DocumentChunk:
    text: str
    embedding: List[float]


# -----------------------------
# LLM Client Wrapper
# -----------------------------

class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Environment variable OPENAI_API_KEY is missing.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content


# -----------------------------
# RAG Engine
# -----------------------------

class QARAGEngine:
    """
    Loads QA documentation, builds embeddings, retrieves relevant chunks,
    and generates answers grounded in the documentation.
    """

    def __init__(self, docs_path: str = "docs/qa/"):
        self.llm = LLMClient()
        self.docs_path = docs_path
        self.chunks: List[DocumentChunk] = []
        self._load_and_index_docs()

    # -------------------------
    # Document Loading
    # -------------------------

    def _load_and_index_docs(self):
        files = glob.glob(os.path.join(self.docs_path, "*.md"))
        if not files:
            print(f"No documentation found in {self.docs_path}")
            return

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
                for chunk in self._split_into_chunks(text):
                    embedding = self.llm.embed(chunk)
                    self.chunks.append(DocumentChunk(text=chunk, embedding=embedding))

        print(f"Indexed {len(self.chunks)} documentation chunks.")

    def _split_into_chunks(self, text: str, size: int = 500) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), size):
            chunk = " ".join(words[i:i+size])
            chunks.append(chunk)
        return chunks

    # -------------------------
    # Retrieval
    # -------------------------

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        import numpy as np
        a = np.array(a)
        b = np.array(b)
        return float(a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        query_embedding = self.llm.embed(query)
        scored = []

        for chunk in self.chunks:
            score = self._cosine_similarity(query_embedding, chunk.embedding)
            scored.append((score, chunk.text))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [text for _, text in scored[:top_k]]

    # -------------------------
    # Generation
    # -------------------------

    def answer(self, query: str) -> str:
        retrieved_chunks = self.retrieve(query)
        context = "\n\n--- Retrieved QA Documentation ---\n\n" + "\n\n".join(retrieved_chunks)

        prompt = f"""
You are an expert QA engineer. Answer the user's question using ONLY the following QA documentation:

{context}

User question:
{query}

Provide a clear, concise, documentation-grounded answer.
"""

        return self.llm.generate(prompt)


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    rag = QARAGEngine(docs_path="docs/qa/")

    query = "What are the mandatory fields for a test case according to our QA standards?"

    answer = rag.answer(query)

    print("\nRAG Answer:\n")
    print(answer)
