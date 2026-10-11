lazy import psycopg2
from api.config import DB_CONFIG
from embeddings.embedder import get_embedding


def retrieve_chunks(query:str, top_k:int=5) -> list[str]:
    """
    Retrieve the most relevant chunks from the database based on a query.

    Args:
        query (str): The input query to search for relevant chunks.
        top_k (int): The number of top relevant chunks to retrieve.

    Returns:
        list[str]: A list of the most relevant chunk texts.
    """
    query_embedding = get_embedding(query)
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            query = """
                    SELECT chunk_text
                    FROM document_chunks
                    ORDER BY embedding <-> %s::vector
                    LIMIT %s
                    """
            params = (str(query_embedding), top_k)
            cur.execute(query,params)
            results = cur.fetchall()
            return [row[0] for row in results]
    except Exception as e:
        print("Error:-", str(e))
        return []
    finally:
        conn.close()



def hybrid_search(query:str, candidate_k:int=10 , top_k:int=5)-> list[dict]:
    """
    Perform a hybrid search using embeddings and text similarity.

    Args:
        query (str): The input query to search for relevant chunks.
        candidate_k (int): The number of candidate chunks to retrieve based on embedding similarity.
        top_k (int): The number of top chunks to return based on text similarity.
    Returns:
        list[dict]: A list of dictionaries containing the most relevant chunk texts and their corresponding similarity scores.
    """
    query_vector = get_embedding(query)
    conn = psycopg2.connect(**DB_CONFIG)
    sql = """WITH vector_candidates AS (
            SELECT id,
                ROW_NUMBER() OVER (
                    ORDER BY embedding <=> %s::vector
                ) AS rank
            FROM document_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        ),
        text_candidates AS (
            SELECT id,
                ROW_NUMBER() OVER (
                    ORDER BY ts_rank_cd(
                        search_vector,
                        plainto_tsquery('english', %s)
                    ) DESC
                ) AS rank
            FROM document_chunks
            WHERE search_vector @@
                plainto_tsquery('english', %s)
            ORDER BY ts_rank_cd(
                search_vector,
                plainto_tsquery('english', %s)
            ) DESC
            LIMIT %s
        ),
        combined AS (
            SELECT id, 1.0 / (60 + rank) AS score
            FROM vector_candidates

            UNION ALL

            SELECT id, 1.0 / (60 + rank) AS score
            FROM text_candidates
        ),
        fused AS (
            SELECT id, SUM(score) AS score
            FROM combined
            GROUP BY id
        )
        SELECT d.document_name,
            d.page_number,
            d.chunk_index,
            d.chunk_text,
            f.score
        FROM fused f
        JOIN document_chunks d ON d.id = f.id
        ORDER BY f.score DESC
        LIMIT %s"""
    try:
        with conn.cursor() as cur:
            vector = str(query_vector)
            cur.execute(sql,(vector,vector,candidate_k,query,query,query,candidate_k,top_k,))  
            rows = cur.fetchall()
            results = [
                {
                    "document_name": row[0],
                    "page_number": row[1],
                    "chunk_index": row[2],
                    "chunk_text": row[3],
                    "score": float(row[4])
                }
                for row in rows
            ]
            return results
    except Exception as e:
        print(f"Error during hybrid search: {e}")
        results = []
        return results
    finally:
        conn.close()
