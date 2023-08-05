import asyncio
from elasticsearch import Elasticsearch


class IndexDriver(object):
    """ Driver for elasticsearch index """

    def __init__(self, host, port, user, pwd, index_prefix):
        self._client = Elasticsearch(
            {host: host},
            port=port,
            http_auth=(user, pwd)
        )
        self._prefix = index_prefix

    async def get_nodes(self, index_type: str, object_ids: [str] = None, reversed_link=None):
        """ Get nodes and their properties corresponding to index_type
            If object_ids is set, returns only documents matching ids
            If reversed_link is not None, search for document having property matching ids in argument
        """
        if reversed_link:
            terms = {}
            terms[reversed_link] = object_ids
            query = {"terms": terms}
        elif object_ids:
            query = {
                "ids": {
                    "values": object_ids
                }
            }
        else:
            query = {
                "match_all": {}
            }

        results = self._client.search(
            index=self._build_index(index_type),
            body={
                "query": query
            },
            size=20
        )
        hits = results['hits']['hits']
        return [{**hit['_source'], "id": hit["_id"]} for hit in hits]

    async def get_node(self, index_type: str, object_id: str):
        """Get node properties matching object_id in parameter"""
        result = self._client.get(
            index=self._build_index(index_type),
            id=object_id
        )
        return {**result['_source'], "id": result["_id"]}

    def _build_index(self, index_type):
        return f'{self._prefix}-{index_type}'
