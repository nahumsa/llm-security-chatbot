from elasticsearch import Elasticsearch
from common.config import ElasticsearchSettings
from common.elasticsearch.repository import ElasticRepository


if __name__ == "__main__":

    elastic_settings = ElasticsearchSettings()

    client = Elasticsearch(hosts=elastic_settings.hosts)
    repository = ElasticRepository(
        client=client, index_name=elastic_settings.index_name
    )

    print(repository.retrieval(term="output handling"))
