from elasticsearch import Elasticsearch
from ingestion.elasticsearch.data_model import ElasticDocument
from ingestion.elasticsearch.repository import ElasticRepository
from ingestion.files import FilesExtractor


if __name__ == "__main__":
    documents_to_ingest: list[ElasticDocument] = []
    for file in FilesExtractor().extract():
        content_dict = {section.name: section.content for section in file.sections}
        documents_to_ingest.append(ElasticDocument(title=file.name, **content_dict))

    # TODO: creat a pydantic settings class for every env variable
    client = Elasticsearch(hosts=["http://localhost:9200"])
    INDEX_NAME = "security_llm"
    repository = ElasticRepository(client=client, index_name=INDEX_NAME)

    repository.create_index(ElasticDocument)
    repository.add(documents=documents_to_ingest)
