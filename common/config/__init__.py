from pydantic_settings import BaseSettings


class ElasticsearchSettings(BaseSettings):
    hosts: list[str] = ["http://localhost:9200"]
    index_name: str = "security_llm"
