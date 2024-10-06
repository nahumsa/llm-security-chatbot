from elasticsearch import Elasticsearch
from common.config import ElasticsearchSettings
from common.elasticsearch.repository import ElasticRepository
import csv

from retrieval.metrics import hit_rate, mrr


def eval(data_store_repository: ElasticRepository):
    with open("data/ground_truth_retrieval.csv", mode="r") as file:
        csv_reader = csv.reader(file)
        relevance_total = []
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue

            title, question = row
            result_list = data_store_repository.retrieval(term=question, num_results=3)
            relevance = [title == result.title for result in result_list]
            relevance_total.append(relevance)

        print(
            {
                "hit_rate": hit_rate(relevance_total),
                "mrr": mrr(relevance_total),
            }
        )


if __name__ == "__main__":

    elastic_settings = ElasticsearchSettings()

    client = Elasticsearch(hosts=elastic_settings.hosts)
    elastic_repository = ElasticRepository(
        client=client, index_name=elastic_settings.index_name
    )

    print("Evaluating Elasticsearch")
    eval(elastic_repository)
