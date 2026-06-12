from sentence_transformers import SentenceTransformer
import chromadb
from ingest import load_documents, chunk_text

MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading model...")
model = SentenceTransformer(MODEL_NAME)
print("Model loaded!")

client = chromadb.PersistentClient(path="chroma_db")

try:
    client.delete_collection("qc_cs")
except:
    pass

collection = client.create_collection("qc_cs")

documents = load_documents()

ids = []
texts = []
metadatas = []

chunk_number = 0

for doc in documents:
    chunks = chunk_text(doc["text"])

    for i, chunk in enumerate(chunks):
        ids.append(f"chunk_{chunk_number}")
        texts.append(chunk)

        metadatas.append({
            "source": doc["source"],
            "chunk": i
        })

        chunk_number += 1

print(f"Embedding {len(texts)} chunks...")

embeddings = model.encode(texts).tolist()

collection.add(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)

def search(query, top_k=3):
    print(f"\nQuery: {query}\n")

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):
        print("=" * 80)
        print(f"Rank: {i + 1}")
        print(f"Source: {metadatas[i]['source']}")
        print(f"Chunk: {metadatas[i]['chunk']}")
        print(f"Distance: {distances[i]:.4f}")
        print()
        print(documents[i])
        print()

print(f"Stored {collection.count()} chunks in ChromaDB!")

search("What tutoring resources are available for Computer Science students?")

search("How can I contact a Computer Science academic advisor?")

search("What opportunities does the AI Skill Foundry 3-Hour Micro-Internship provide?")