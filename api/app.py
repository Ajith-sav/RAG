from fastapi import FastAPI
from pydantic import BaseModel
from retrieval.get_data import get_answers

app = FastAPI(title="RAG API", description="API for retrieving answers from a knowledge base using RAG.", version="1.0.0")


class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(request: QueryRequest)-> dict:
    """
    Get answers from the most relevant chunks based on a query.

    Args:
        query (str): The input query to search for relevant chunks.
    Returns:
        str: A string containing the most relevant chunk texts concatenated together.
    """
    answers = get_answers(request.query)

    return {"data": {"query":request.query,"answer":answers}, "message": "Success", "status":200}

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify that the API is running.

    Returns:
        dict: A dictionary indicating the health status of the API.
    """
    return {"status": "healthy"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, log_level="info")