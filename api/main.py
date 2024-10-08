import time
import uuid
from datetime import datetime
from typing import Annotated

import google.generativeai as genai
from elasticsearch import Elasticsearch
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from common.config import ElasticsearchSettings, GeminiSettings
from common.elasticsearch.repository import ElasticRepository
from common.response_model import ResponseModel
from database.model import Conversation, Feedback
from database.postgres import get_session
from rag.repositories.generative import GeminiGenenerativeRepository
from rag.repositories.rag import RAGRepository

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


class FeedbackRequest(BaseModel):
    conversation_id: str
    feedback: Annotated[int, Field(ge=-1, le=1)]


class ResponseModelUUID(ResponseModel):
    uuid: str


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


@app.post("/rag", response_model=ResponseModelUUID)
def rag_query(
    request: QueryRequest,
    rag_repository: Annotated[RAGRepository, Depends(get_rag_repository)],
    db_session: Annotated[Session, Depends(get_session)],
):
    gemini_settings = GeminiSettings()  # type: ignore
    start_time = time.time()
    response = rag_repository.run(request.question)
    uuid_str = str(uuid.uuid4())

    db_session.add(
        Conversation(
            id=uuid_str,
            question=request.question,
            answer=str(response),
            model_used=gemini_settings.gemini_model_name,
            response_time=time.time() - start_time,
            timestamp=datetime.utcnow(),
        )
    )

    db_session.commit()

    return ResponseModelUUID(uuid=uuid_str, **response.model_dump())


@app.post("/feedback")
def feedback(
    request: FeedbackRequest,
    db_session: Annotated[Session, Depends(get_session)],
) -> None:
    db_session.add(
        Feedback(
            conversation_id=request.conversation_id,
            feedback=request.feedback,
            timestamp=datetime.utcnow(),
        )
    )

    db_session.commit()

    return
