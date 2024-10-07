from common.elasticsearch.repository import ElasticRepository
from prompts import PromptManager
from pydantic import BaseModel

from rag.repositories.generative import GenerativeRepository


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
            for entry in self.retrieval_repository.retrieval(
                term=question, num_results=1
            )
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
            response_json_schema=self.response_model.model_json_schema(),
        )

        return self.__generate_model_response(prompt)
