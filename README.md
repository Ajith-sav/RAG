# RAG (Retrieval-Augmented Generation)

A modular Retrieval-Augmented Generation system for document processing, embedding, and semantic search.

## Features

- **Document Ingestion**: Process PDFs and other document formats
- **Chunking**: Intelligent text splitting for optimal retrieval
- **Embeddings**: Vector representations using sentence transformers
- **Vector Database**: Efficient similarity search with persistent storage
- **Hybrid Search**: Combines dense and sparse retrieval
- **API**: RESTful interface for querying the RAG system

## Project Structure

```
RAG/
├── api/                 # REST API endpoints
│   ├── app.py          # FastAPI application
│   └── config.py       # Configuration settings
├── chunking/           # Text chunking strategies
│   └── chunker.py
├── documents/          # Source documents (PDFs)
├── embeddings/         # Embedding generation
│   └── embedder.py
├── ingestion/          # Document ingestion pipeline
│   └── rag.py
├── retrieval/          # Search and retrieval
│   ├── get_data.py
│   └── hybrid_search.py
├── vectordb/           # Vector database operations
│   └── vector_store.py
└── Script.sql          # Database schema
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Ajith-sav/RAG.git
cd RAG

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the API Server

```bash
cd api
python app.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `POST /ingest` - Ingest documents into the vector database
- `POST /query` - Query the RAG system
- `GET /health` - Health check

### Document Ingestion

Place PDF documents in the `documents/` folder and run the ingestion pipeline:

```python
from ingestion.rag import ingest_documents
ingest_documents("documents/")
```

## Configuration

Edit `api/config.py` to configure:
- Embedding model
- Vector database settings
- Chunking parameters
- API host/port

## Requirements

- Python 3.8+
- FastAPI
- Sentence Transformers
- Vector database (ChromaDB/FAISS)
- PyMuPDF (for PDF processing)

## License

MIT License