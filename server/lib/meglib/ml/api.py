import json
import asyncio
import httpx
import sys

from typing import Dict, AsyncGenerator
from abc import ABC, abstractmethod
from errors import APIError


class API(ABC):
    def __init__(self, host: str, port: int, endpoint: str):
        self.endpoint_url = f"http://{host}:{port}{endpoint}"

    @abstractmethod
    async def query(self, payload) -> Dict:
        """Abstract method to query the API."""
        pass

    async def check_health(self) -> int:
        """Checks the health of the server by sending a GET request to the "/health" endpoint.
        Returns
        -------
        int
            The HTTP status code of the response. A status code of 200 indicates that the server is healthy.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url=self.endpoint_url + "/health")
            return response.status_code


class Llm(API):
    async def query(self, payload) -> AsyncGenerator:
        """This method streams results from a POST request to the '/generate' endpoint.

        Parameters
        ----------
        payload : dict
            The payload for the query. It should contain the necessary information for the request.

        Yields
        ------
        str
            The output from the response, parsed from a JSON to `output` string.

        Raises
        ------
        HTTPStatusError
            If the response status code is not 200, an exception is raised.
        """
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            async with client.stream(
                method="POST",
                url=self.endpoint_url + "/generate",
                json=payload,
                headers=headers,
                timeout=30,
            ) as response:
                if response.status_code == 200:
                    async for line in response.aiter_lines():
                        line_dict = json.loads(line)
                        res = line_dict["output"]
                        yield res
                else:
                    response.raise_for_status()

    async def query_no_stream(self, payload) -> Dict:
        """This method returns a single result from a POST request to the '/generate' endpoint.

        Parameters
        ----------
        payload : dict
            The payload for the query. It should contain the necessary information for the request.

        Returns
        -------
        dict
            The result from the response, parsed from a JSON string to a dictionary.

        Raises
        ------
        HTTPStatusError
            If the response status code is not 200, an exception is raised.
        """
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint_url + "/generate",
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            return result


class Embedding(API):
    async def query(self, payload) -> Dict:
        """This method returns a single result from a POST request to the '/embed' endpoint.

        Parameters
        ----------
        payload : dict
            The payload for the query. It should contain the necessary information for the request.

        Returns
        -------
        dict
            The result from the response, parsed from a JSON string to a dictionary.

        Raises
        ------
        HTTPStatusError
            If the response status code is not 200, an exception is raised.
        """
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=self.endpoint_url + "/embed",
                params=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()

            embeddings = response.json()
            return embeddings


async def _test_workflow(llm: Llm, emb: Embedding):
    string = "Tell me something about AI"

    emb_payload = {
        "data": [string, string + "hello", string + "he"],
        "type": "QUERY_EMBED",
    }

    emb_res = await emb.query(payload=emb_payload)
    print(len(emb_res.items()))
    print(len(emb_res["embedding"]), type(emb_res["embedding"]))

    # vector search (skipping) -> get relevant text
    text = "Artificial Intelligence (AI) is a field of research in computer science"

    llm_string = (
        f"content: {text} \nuser:{string}. \nAnswer the user's question from content"
    )
    llm_payload = {
        "messages": [{"role": "user", "content": llm_string}],
        "stream": True,
        "max_tokens": "1024",
        "temperature": 0.3,
    }
    if llm_payload["stream"]:
        async for lines in llm.query(payload=llm_payload):
            sys.stdout.write(lines)
            sys.stdout.flush()

    else:
        res = await llm.query_no_stream(payload=llm_payload)
        print(res)


if __name__ == "__main__":
    llm = Llm(
        host="172.16.0.57",
        port=9999,
        endpoint="/api/v1/llm",
    )
    emb = Embedding(
        host="172.16.0.57",
        port=9999,
        endpoint="/api/v1/embedder",
    )

    # typical workflow
    asyncio.run(_test_workflow(llm, emb))
