from elasticsearch import Elasticsearch
from common.config import ElasticsearchSettings
from common.elasticsearch.repository import ElasticRepository
import csv

from retrieval.metrics import hit_rate, mrr


if __name__ == "__main__":

    elastic_settings = ElasticsearchSettings()

    client = Elasticsearch(hosts=elastic_settings.hosts)
    repository = ElasticRepository(
        client=client, index_name=elastic_settings.index_name
    )

    with open("data/ground_truth_retrieval.csv", mode="r") as file:
        csv_reader = csv.reader(file)
        relevance_total = []
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue

            title, question = row
            result_list = repository.retrieval(term=question, num_results=3)
            relevance = [title == result.title for result in result_list]
            relevance_total.append(relevance)

        print(
            {
                "hit_rate": hit_rate(relevance_total),
                "mrr": mrr(relevance_total),
            }
        )
