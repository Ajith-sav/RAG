

def split_text_into_chunks(text:str, chunk_size:int=500, overlap:int=100)-> list[str]:
    """
        Splits text into fixed-size chunks with a specified character overlap.
    """
    words = text.split()
    chunks = []
    start = 0

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        if end > len(words):
            break
        start = end - overlap

    return chunks
