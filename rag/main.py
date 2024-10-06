import json
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from common.config import ElasticsearchSettings, GeminiSettings
import google.generativeai as genai

from common.elasticsearch.repository import ElasticRepository
from prompts import PromptManager


class ResponseModel(BaseModel):
    answer: str
    example_vulnerability: str
    example_attack: str
    prevention: str


def generate_context(question: str) -> list[str]:
    elastic_settings = ElasticsearchSettings()
    client = Elasticsearch(hosts=elastic_settings.hosts)

    elastic_repository = ElasticRepository(
        client=client, index_name=elastic_settings.index_name
    )

    return [
        entry.model_dump_json()
        for entry in elastic_repository.retrieval(term=question, num_results=3)
    ]


def generate_response(prompt: str, response_model: type[BaseModel]) -> BaseModel:
    gemini_settings = GeminiSettings()  # type: ignore
    genai.configure(api_key=gemini_settings.google_api_key)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=gemini_settings.generation_config.model_dump(),  # type: ignore
    )

    chat_session = model.start_chat()
    response = chat_session.send_message(prompt)
    return response_model.model_validate_json(response.text)


if __name__ == "__main__":
    question = "What is 'jailbreaking' in the context of Direct Prompt Injections?"

    context = generate_context(question)

    prompt = PromptManager.get_prompt(
        "rag_generation",
        question=question,
        context=context,
        response_json_schema=ResponseModel.model_json_schema(),
    )

    print(generate_response(prompt, response_model=ResponseModel))
