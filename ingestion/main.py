from elasticsearch import Elasticsearch

from common.config import ElasticsearchSettings
from common.elasticsearch.data_model import ElasticDocument
from common.elasticsearch.repository import ElasticRepository
from ingestion.files import FilesExtractor

if __name__ == "__main__":
    documents_to_ingest: list[ElasticDocument] = []

    for file in FilesExtractor().extract():
        content_dict = {section.name: section.content for section in file.sections}
        documents_to_ingest.append(ElasticDocument(title=file.name, **content_dict))

    elastic_settings = ElasticsearchSettings()

    client = Elasticsearch(hosts=elastic_settings.hosts)
    repository = ElasticRepository(
        client=client, index_name=elastic_settings.index_name
    )

    repository.create_index(ElasticDocument)
    repository.add(documents=documents_to_ingest)
