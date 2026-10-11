-- level 1
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_name TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL
);

-- level 2

ALTER TABLE document_chunks
ADD COLUMN IF NOT EXISTS page_number INTEGER;

ALTER TABLE document_chunks
ADD COLUMN IF NOT EXISTS chunk_index INTEGER;

ALTER TABLE document_chunks
ADD COLUMN IF NOT EXISTS search_vector TSVECTOR
GENERATED ALWAYS AS (
    to_tsvector('english', chunk_text)
) STORED;

CREATE INDEX IF NOT EXISTS idx_chunks_search_vector
ON document_chunks USING GIN (search_vector);
