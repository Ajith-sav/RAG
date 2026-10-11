lazy import psycopg2
from pypdf import PdfReader
from chunking.chunker import split_text_into_chunks
from api.config import DB_CONFIG
from embeddings.embedder import get_embedding

def ingest_pdf(pdf_path:str):
    """
    Read Document and split into chunks then covert into embeddings then store in Vector DB
    """
    reader = PdfReader(pdf_path)
    text = "\n".join(
        page.extract_text() or "" for page in reader.pages
    )
    chunks = split_text_into_chunks(text=text)

    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn:
            with conn.cursor() as cur:
                for chunk in chunks:
                    vector = get_embedding(chunk)
                    query = """
                            INSERT INTO document_chunks (document_name, chunk_text, embedding)
                            VALUES (%s,%s,%s::vector)
                            """
                    params = (pdf_path,chunk,str(vector))
                    cur.execute(query,params,)
    except Exception as e:
        print("Error:",str(e))
    finally:
        conn.close()    
    print(f"Indexed {len(chunks)} chunks.")


def hybrid_ingest_pdf(pdf_path:str):
    """
    Read Document and split into chunks then covert into embeddings then store in Vector DB
    """
    reader = PdfReader(pdf_path)
    conn = psycopg2.connect(**DB_CONFIG)
    total_chunks = 0
    try:
        with conn:
            with conn.cursor() as cur:
                for page_number, page in enumerate(reader.pages, start=1):
                    text = page.extract_text() or ""
                    if not text.strip():
                        continue  # Skip empty pages
                    chunks = split_text_into_chunks(text=text)
                    if not chunks: 
                        print(f"No chunks found for page {page_number} in {pdf_path}.")
                    for chunk_index, chunk in enumerate(chunks, start=1):
                        vector = get_embedding(chunk)
                        query = """
                                INSERT INTO document_chunks (
                                    document_name,
                                    page_number,
                                    chunk_index,
                                    chunk_text,
                                    embedding
                                )
                                VALUES (%s, %s, %s, %s, %s::vector)
                                """
                        params = (pdf_path,page_number,chunk_index,chunk,str(vector),)
                        cur.execute(query,params)
                        total_chunks += 1
    except Exception as e:
        print(f"Error ingesting PDF: {e}")
    finally:
        conn.close()

    print(f"Successfully ingested {total_chunks} chunks from {pdf_path}.")


if __name__== "__main__":
    pdf_path = "documents/Leave-and-Holiday-Policy.pdf"
    # ingest_pdf(pdf_path)  
    hybrid_ingest_pdf(pdf_path)