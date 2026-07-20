import chromadb

from config import (
    CHROMA_DB_HOST,
    CHROMA_DB_PORT,
)

# Connect to the Chroma server
client = chromadb.HttpClient(
    host=CHROMA_DB_HOST,
    port=CHROMA_DB_PORT,
)

# Create (or retrieve) a collection
collection = client.get_or_create_collection(
    name="rag_documents",
    metadata={"description": "RAG document collection"},
)


def add_documents(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
):
    """
    Insert or update documents in ChromaDB.
    """

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search_documents(
    query_embedding: list[float],
    top_k: int = 5,
):
    """
    Perform semantic search.
    """

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )


def count_documents():
    """
    Returns the number of indexed chunks.
    """

    return collection.count()
