from sentence_transformers import SentenceTransformer

from config import (
    EMBED_MODEL_NAME,
    HF_API_KEY,
)

# Load the embedding model once when the application starts.
# This avoids reloading the model for every request.
if HF_API_KEY:
    embedding_model = SentenceTransformer(
        EMBED_MODEL_NAME,
        token=HF_API_KEY,
    )
else:
    embedding_model = SentenceTransformer(
        EMBED_MODEL_NAME,
    )


def generate_embedding(text: str) -> list:
    """
    Generate an embedding for a single string.

    Returns:
        List[float]
    """

    embedding = embedding_model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple strings.

    Returns:
        List[List[float]]
    """

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()
