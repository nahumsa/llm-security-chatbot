import csv
from typing import Counter

import google.generativeai as genai
from elasticsearch import Elasticsearch
from pydantic import BaseModel

from common.config import ElasticsearchSettings, GeminiSettings
from common.elasticsearch.repository import ElasticRepository
from common.response_model import ResponseModel
from prompts import PromptManager
from rag.repositories.generative import (
    GeminiGenenerativeRepository,
    GenerativeRepository,
)
from rag.repositories.rag import RAGRepository


class EvaluationModel(BaseModel):
    relevance: str
    explanation: str


def eval_rag(
    rag_repository: RAGRepository, generative_repository: GenerativeRepository
) -> list[BaseModel]:
    with open("data/rag_eval.csv", mode="r") as file:
        csv_reader = csv.reader(file)
        relevance_total = []
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue

            question, *_ = row

            rag_result = rag_repository.run(question=question)

            eval_prompt = PromptManager.get_prompt(
                "rag_evaluation",
                question=question,
                answer_llm=rag_result,
            )

            result = generative_repository.generate_response(
                prompt=eval_prompt, response_model=EvaluationModel
            )

            relevance_total.append(result)

    print(Counter([entry.relevance for entry in relevance_total]))


if __name__ == "__main__":
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

    prompts_to_evaluate: list[str] = ["rag_generation_1", "rag_generation_2"]

    for prompt_name in prompts_to_evaluate:
        rag_repository = RAGRepository(
            retrieval_repository=elastic_repository,
            generative_repository=gemini_repo,
            prompt_name=prompt_name,
            response_model=ResponseModel,
        )

        print(f"Evaluating: {prompt_name}.j2")
        eval_rag(rag_repository, gemini_repo)
