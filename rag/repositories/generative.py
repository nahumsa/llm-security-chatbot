from abc import abstractmethod
import google.generativeai as genai
from pydantic import BaseModel

from common.config import GeminiSettings


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
