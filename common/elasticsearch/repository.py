import logging
from typing import Optional, get_type_hints
from elasticsearch import BadRequestError, Elasticsearch
from elasticsearch.helpers import streaming_bulk
from pydantic import BaseModel, TypeAdapter

from common.elasticsearch.data_model import (
    ElasticDocument,
    IndexSettings,
    Mappings,
    Settings,
)

ES_MAPPING = {
    str: "text",
    int: "long",
    Optional[str]: "text",
}

logger = logging.getLogger(__name__)


class ElasticRepository:

    def __init__(self, client: Elasticsearch, index_name: str) -> None:
        self._client = client
        self._index_name = index_name

    def convert_base_model_to_mapping(
        self, data_model: type[BaseModel]
    ) -> IndexSettings:
        model_fields = get_type_hints(data_model)

        properties = {}

        for field_name, field_type in model_fields.items():
            es_field_name = field_name

            try:
                es_type = ES_MAPPING[field_type]

            except IndexError as _:
                raise NotImplementedError(
                    f"the mapping for {str(field_type)} is not implemented"
                )

            properties[es_field_name] = {"type": es_type}

        return IndexSettings(
            settings=Settings(number_of_shards=1, number_of_replicas=1),
            mappings=Mappings(properties=properties),
        )

    def create_index(self, data_model: type[BaseModel]) -> None:
        try:
            self._client.indices.create(
                index=self._index_name,
                body=self.convert_base_model_to_mapping(data_model).model_dump(),
            )
            logger.info(f"created index {self._index_name}")

        except BadRequestError as _:
            logger.info(f"index {self._index_name} already created")

    def add(self, documents: list[ElasticDocument]) -> None:
        successes: int = 0

        for ok, _ in streaming_bulk(
            client=self._client,
            index=self._index_name,
            actions=[doc.model_dump() for doc in documents],
        ):
            successes += ok

        logger.info(f"Indexed {successes}/{len(documents)} documents")

    def retrieval(self, term: str, num_results: int = 3) -> list[ElasticDocument]:
        retrieval_docs: list[ElasticDocument] = []

        query = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": term,
                            "fields": [
                                "title^10",
                                "description^3",
                                "example_vulnerabilities^1",
                                "mitigation^1",
                                "example_attacks^1",
                            ],
                            "type": "best_fields",
                        }
                    }
                }
            }
        }

        response = self._client.search(
            index=self._index_name, body=query, size=num_results
        )

        for hit in response["hits"]["hits"]:
            retrieval_docs.append(ElasticDocument(**hit["_source"]))

        return retrieval_docs
