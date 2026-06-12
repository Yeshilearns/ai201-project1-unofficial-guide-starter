import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "qc_cs"

model = SentenceTransformer(MODEL_NAME)
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(COLLECTION_NAME)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve_chunks(question, top_k=3):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": text,
            "source": metadata["source"],
            "chunk": metadata["chunk"],
            "distance": distance
        })

    return chunks


def ask(question):
    chunks = retrieve_chunks(question)

    context = "\n\n".join(
        f"Source: {chunk['source']} | Chunk: {chunk['chunk']}\n{chunk['text']}"
        for chunk in chunks
    )

    prompt = f"""
Answer the user's question using ONLY the provided context.

If the context does not contain enough information to answer, say:
"I don't have enough information in the provided documents."

Include source filenames in your answer.

Context:
{context}

Question:
{question}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a grounded RAG assistant. Only answer using the retrieved context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    sources = sorted(set(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


if __name__ == "__main__":
    result = ask("What tutoring resources are available for Computer Science students?")
    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print("-", source)