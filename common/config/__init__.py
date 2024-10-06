from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ElasticsearchSettings(BaseSettings):
    hosts: list[str] = ["http://localhost:9200"]
    index_name: str = "security_llm"


class GeminiGenerationConfig(BaseModel):
    temperature: float = 1
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 8192
    response_mime_type: str = "application/json"


class GeminiSettings(BaseSettings):
    google_api_key: str
    gemini_model_name: str = "gemini-1.5-flash-8b"
    generation_config: GeminiGenerationConfig = GeminiGenerationConfig()
