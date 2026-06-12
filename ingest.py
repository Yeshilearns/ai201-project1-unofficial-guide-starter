from pathlib import Path
import re

DOCUMENTS_DIR = Path("documents")
CHUNK_SIZE = 400
OVERLAP = 80


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    return text.strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_documents():
    documents = []

    for path in DOCUMENTS_DIR.glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        cleaned = clean_text(text)

        documents.append({
            "source": path.name,
            "text": cleaned
        })

    return documents


def main():
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    print(f"Loaded documents: {len(documents)}")
    print(f"Total chunks: {len(all_chunks)}")

    print("\nSample chunks:\n")
    for chunk in all_chunks[:5]:
        print("=" * 80)
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"])


if __name__ == "__main__":
    main()