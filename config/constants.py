APP_NAME = "FieldSyncAI"
DEFAULT_API_PREFIX = "/api/v1"

DEFAULT_OLLAMA_MODEL = "llama3.2:1b"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_QDRANT_COLLECTION = "fieldsyncai_docs"

DEFAULT_VECTOR_TOP_K = 5
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100

ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".txt"}
ALLOWED_DOCUMENT_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}