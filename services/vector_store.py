import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "chroma_db"

client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = client.get_or_create_collection(
    name="summaries"
)

model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)


def add_summary_to_vector_db(title: str, content: str, file_name: str):
    embedding = model.encode(content).tolist()

    collection.add(
        documents=[content],
        embeddings=[embedding],
        metadatas=[{"title": title}],
        ids=[file_name]
    )


def semantic_search(query: str, n_results: int = 5):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results
