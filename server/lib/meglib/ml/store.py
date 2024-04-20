import uuid
import asyncio
import random
import json

from qdrant_client import AsyncQdrantClient, grpc
from typing import Dict, List, Any, Optional
from grpc import RpcError
from google.protobuf.json_format import MessageToJson

__all__ = ["VectorDB"]


class VectorDB:
    def __init__(self, config: Dict):
        """Qdrant Vector DB __init__

        Parameters
        ----------
        config : Dict
            config dict directly passed to the QdrantClient
        """
        self.client = AsyncQdrantClient(**config)

    def _get_distance_metric(self, metric: str) -> Any:
        if metric == "cosine":
            return grpc.Distance.Cosine
        elif metric == "dot":
            return grpc.Distance.Dot
        elif metric == "euclid":
            return grpc.Distance.Euclid
        elif metric == "manhattan":
            return grpc.Distance.Manhattan

    def _generate_uuid(self):
        """generates uuid4"""
        return str(uuid.uuid4())

    def _get_cast_value(self, value):
        """Convert the payload's python type to qdrant's grpc type"""
        if isinstance(value, str):
            return grpc.Value(string_value=value)
        elif isinstance(value, int):
            return grpc.Value(integer_value=value)
        elif isinstance(value, float):
            return grpc.Value(double_value=value)
        elif isinstance(value, bool):
            return grpc.Value(bool_value=value)
        elif isinstance(value, list):
            return grpc.Value(
                list_value=grpc.ListValue(
                    values=[self._get_cast_value(val) for val in value]
                )
            )
        elif isinstance(value, dict):
            return grpc.Value(
                struct_value=grpc.Struct(
                    fields={k: self._get_cast_value(v) for k, v in value.items()}
                )
            )
        else:
            return grpc.Value(null_value=value)

    def proto_to_dict(self, message):
        """convert protobuf to Json format

        Parameters
        ----------
        message : google.protobuf.message.Message
            proto formatted object to be converted to dict

        Returns
        -------
        Dict
            Json dict
        """
        json_obj = MessageToJson(message)
        return json.loads(json_obj)

    async def delete(self, collection_name: str, timeout: Optional[int] = 10):
        """Delete Collection specified by name

        Parameters
        ----------
        collection_name : str
            name of the collection
        timeout : Optional[int], optional
            timeout limit, by default 10

        Returns
        -------
        response : response of delete query
        """
        response = await self.client.grpc_collections.Delete(
            grpc.DeleteCollection(collection_name=collection_name, timeout=timeout)
        )

        return response

    async def create(
        self,
        collection_name: str,
        dim: int,
        distance: str,
        timeout: Optional[int] = 10,
        quantization_config: Optional[Dict] = None,
        hnsw_config: Optional[Dict] = None,
    ):
        """Create collection specified by name

        Parameters
        ----------
        collection_name : str
            name of the collection
        dim : int
            vector dimension space
        distance : str
            distance metric used, any one of ['cosine', 'dot', 'euclid', manhattan]
        timeout : Optional[int], optional
            timeout in seconds, by default 10
        quantization_config : Optional[Dict], optional
            config dict of quantization, by default None
        hnsw_config : Optional[Dict], optional
            config dict of hnsw, by default None

        Returns
        -------
        response
            response of create query
        """
        # quadrant collection : env variable
        params = {
            "collection_name": collection_name,
            "vectors_config": grpc.VectorsConfig(
                params=grpc.VectorParams(
                    size=dim,
                    distance=self._get_distance_metric(distance),
                )
            ),
            "timeout": timeout,
        }

        if quantization_config:
            params.update(
                {
                    "quantization_config": grpc.QuantizationConfig(
                        scalar=grpc.ScalarQuantization(
                            type=grpc.QuantizationType.Int8, **quantization_config
                        )
                    )
                }
            )

        if hnsw_config:
            params.update({"hnsw_config": grpc.HnswConfigDiff(**hnsw_config)})

        response = await self.client.grpc_collections.Create(
            grpc.CreateCollection(**params)
        )

        return response

    async def verify(self, collection_name: str):
        """verify if collection is present

        Parameters
        ----------
        collection_name : str
            name of the collection

        Returns
        -------
        response
            returns None if not found | error, else the response of the query
        """
        try:
            response = await self.client.grpc_collections.Get(
                grpc.GetCollectionInfoRequest(collection_name=collection_name)
            )
        except RpcError:
            return None

        return response

    async def insert(self, collection_name: str, data: List[Dict], wait: bool = False):
        """Insert List of points to the collection

        Parameters
        ----------
        collection_name : str
            name of the collection, for insert operation
        data : List[Dict]
            data points in the format
            List[
                Dict{
                    "vector": List
                    "payload": Dict
                }
            ]
        wait : bool, optional
            should the query wait until changes have been applied,
            by default False

        Returns
        -------
        response
            response of the query
        """

        points = []
        for data_point in data:
            payload = {}
            for key, value in data_point["payload"].items():
                payload[key] = self._get_cast_value(value)

            points.append(
                grpc.PointStruct(
                    id=grpc.PointId(uuid=self._generate_uuid()),
                    payload=payload,
                    vectors=grpc.Vectors(vector=grpc.Vector(data=data_point["vector"])),
                )
            )

        response = await self.client.grpc_points.Upsert(
            grpc.UpsertPoints(
                collection_name=collection_name,
                points=points,
                wait=wait,
            )
        )

        return response

    async def search(
        self,
        collection_name: str,
        vector: List[float],
        limit: Optional[int] = 5,
        filters: Optional[Dict] = None,
    ) -> Dict:
        """Searches the specified collection for similar points to the provided vector.

        Parameters
        ----------
        collection_name : str
            The name of the collection to search within.
        vector : List[float]
            The vector representing the query point.
        limit : Optional[int], optional
           The maximum number of results to return, by default 5
        filters : Optional[Dict], optional
            A dictionary of key-value pairs to filter search results.
            - Keys must be field names within the collection.
            - Values can be integers or strings, depending on the field type.
            Note: Currently, only filters on string and integer fields are supported.

        Returns
        -------
        JsonResponse : Dict
            response from the query
        """
        filter_obj = None
        if filters:
            conditions = [
                grpc.Condition(
                    field=grpc.FieldCondition(
                        key=k,
                        match=(
                            grpc.Match(integer=v)
                            if isinstance(v, int)
                            else grpc.Match(keyword=str(v))
                        ),
                    )
                )
                for k, v in filters.items()
            ]
            filter_obj = grpc.Filter(must=conditions)

        search_points_dict = {
            "collection_name": collection_name,
            "limit": limit,
            "vector": vector,
            "with_payload": grpc.WithPayloadSelector(enable=True),
            "filter": filter_obj,
        }

        response = await self.client.grpc_points.Search(
            grpc.SearchPoints(**search_points_dict)
        )

        return response

    async def create_payload_index(
        self, collection_name: str, field_name: str, field_schema: str
    ):
        """RestApi function to create a payload index on a specified collection.

        Parameters
        ----------
        collection_name : str
            The name of the collection to create the index in.
        field_name : str
            The name of the field to index.
        field_schema : str
            The response from the RestAPI server.

        Returns
        -------
        response
            response for the query
        """
        response = await self.client.create_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            field_schema=eval(field_schema),
        )

        return response


def generate_random_numbers(n):
    return [random.uniform(-3, 3) for _ in range(n)]


async def _test_create(collection_name: str):
    ret = await obj.create(
        collection_name=collection_name,
        dim=1024,
        distance="cosine",
        timeout=5,
        hnsw_config={"m": 10, "ef_construct": 10},
        quantization_config={
            "quantile": 0.99,
        },
    )
    print(ret)


async def _test_verify(collection_name: str):
    ret = await obj.verify(collection_name=collection_name)
    print(ret)


async def _test_insert(collection_name: str):
    ret = await obj.insert(
        collection_name=collection_name,
        data=[
            {
                "vector": generate_random_numbers(1024),
                "payload": {
                    "text": "lorem ipsum :)",
                    "int": 123,
                    "float": 0.0123,
                    "list": [1, 2, "abc"],
                    "dict": {"a": 2, "b": "c"},
                    "bool": True,
                    "null": None,
                },
            },
            {
                "vector": generate_random_numbers(1024),
                "payload": {
                    "text": "dup lorem ipsum :)",
                    "int": 1230,
                    "float": 0.123,
                    "list": [1, 2, "abc"],
                    "dict": {"a": [1, 2], "2": "c"},
                    "bool": False,
                    "null": None,
                },
            },
        ],
        wait=False,
    )

    print(ret)


async def _test_search(collection_name: str):
    ret = await obj.search(
        collection_name=collection_name,
        vector=generate_random_numbers(1024),
        limit=1,
        filters={"text": "lorem ipsum :)"},
    )
    print(ret)

    ret = await obj.search(
        collection_name=collection_name,
        vector=generate_random_numbers(1024),
        limit=1,
        filters={"int": 123},
    )
    print(ret)


async def _test_create_payload_index(collection_name: str):
    ret = await obj.create_payload_index(
        collection_name=collection_name, field_schema="grpc.Integer", field_name="int"
    )
    print(ret)


async def _test_delete(collection_name: str):
    ret = await obj.delete(collection_name=collection_name)
    print(ret)


async def _main(collection_name: str):
    await _test_create(collection_name=collection_name)
    await _test_verify(collection_name=collection_name)
    await _test_create_payload_index(collection_name=collection_name)
    await _test_insert(collection_name=collection_name)
    await _test_search(collection_name=collection_name)
    await _test_delete(collection_name=collection_name)


if __name__ == "__main__":
    obj = VectorDB(
        config={"url": "localhost", "port": "6333", "prefer_grpc": True, "timeout": 5}
    )

    # perform test
    collection_name = "example_collection"
    asyncio.run(_main(collection_name=collection_name), debug=True)
