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
    generation_config: GeminiGenerationConfig = GeminiGenerationConfig()
