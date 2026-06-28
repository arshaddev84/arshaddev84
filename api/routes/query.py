from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    question: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=10)


class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)


@router.post("/", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def ask_question(payload: QueryRequest) -> QueryResponse:
    # TODO: Implement retrieval, reranking, prompt construction, and generation.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="RAG query pipeline is not implemented yet.",
    )