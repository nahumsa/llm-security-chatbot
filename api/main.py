from typing import Annotated

import google.generativeai as genai
from elasticsearch import Elasticsearch
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from common.config import ElasticsearchSettings, GeminiSettings
from common.elasticsearch.repository import ElasticRepository
from common.response_model import ResponseModel
from rag.repositories.generative import GeminiGenenerativeRepository
from rag.repositories.rag import RAGRepository

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


def get_rag_repository() -> RAGRepository:
    # environment variables
    gemini_settings = GeminiSettings()  # type: ignore
    genai.configure(api_key=gemini_settings.google_api_key)
    elastic_settings = ElasticsearchSettings()

    # repositories
    client = Elasticsearch(hosts=elastic_settings.hosts)
    elastic_repository = ElasticRepository(
        client=client, index_name=elastic_settings.index_name
    )

    gemini_repo = GeminiGenenerativeRepository(settings=gemini_settings)

    return RAGRepository(
        retrieval_repository=elastic_repository,
        generative_repository=gemini_repo,
        prompt_name="rag_generation_1",
        response_model=ResponseModel,
    )


@app.post("/rag", response_model=ResponseModel)
async def rag_query(
    request: QueryRequest,
    rag_repository: Annotated[RAGRepository, Depends(get_rag_repository)],
):
    try:
        return rag_repository.run(request.question)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
