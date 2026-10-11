lazy import requests

from api.config import EMBEDDING_MODEL, OLLAMA_URL


def get_embedding(text:str) -> list[float]:
    """
    Get the embedding for a given text using the OLLAMA API.

    Args:
        text (str): The input text to be embedded."""
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBEDDING_MODEL, "prompt":text},
        timeout=120
    )
    response.raise_for_status()
    return response.json()["embedding"]
