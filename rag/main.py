import google.generativeai as genai
from elasticsearch import Elasticsearch

from common.config import ElasticsearchSettings, GeminiSettings
from common.elasticsearch.repository import ElasticRepository
from common.response_model import ResponseModel
from rag.repositories.generative import GeminiGenenerativeRepository
from rag.repositories.rag import RAGRepository

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
