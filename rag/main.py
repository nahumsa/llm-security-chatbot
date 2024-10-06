from abc import abstractmethod
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


class GenerativeRepository:
    @abstractmethod
    def generate_response(
        self, prompt: str, response_model: type[BaseModel]
    ) -> BaseModel:
        pass


class GeminiGenenerativeRepository(GenerativeRepository):
    def __init__(self, settings: GeminiSettings) -> None:
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model_name,
            generation_config=settings.generation_config.model_dump(),  # type: ignore
        )

    def generate_response(
        self, prompt: str, response_model: type[BaseModel]
    ) -> BaseModel:
        chat_session = self.model.start_chat()
        response = chat_session.send_message(prompt)
        return response_model.model_validate_json(response.text)


class RAGRepository:
    def __init__(
        self,
        retrieval_repository: ElasticRepository,
        generative_repository: GenerativeRepository,
        prompt_name: str,
        response_model: type[BaseModel],
    ) -> None:
        self.retrieval_repository = retrieval_repository
        self.prompt_name = prompt_name
        self.response_model = response_model
        self.generative_repository = generative_repository

    def __generate_context(self, question: str) -> list[str]:
        return [
            entry.model_dump_json()
            for entry in elastic_repository.retrieval(term=question, num_results=1)
        ]

    def __generate_model_response(self, prompt: str) -> BaseModel:
        return self.generative_repository.generate_response(
            prompt, response_model=self.response_model
        )

    def run(self, question: str) -> BaseModel:
        context = self.__generate_context(question)

        prompt = PromptManager.get_prompt(
            self.prompt_name,
            question=question,
            context=context,
            response_json_schema=ResponseModel.model_json_schema(),
        )

        return self.__generate_model_response(prompt)


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

    rag_repository = RAGRepository(
        retrieval_repository=elastic_repository,
        generative_repository=gemini_repo,
        prompt_name="rag_generation_1",
        response_model=ResponseModel,
    )

    question = "What is 'jailbreaking' in the context of Direct Prompt Injections?"
    print(rag_repository.run(question))
