import asyncio
import json
import logging
import os
import sys
from typing import Dict, List

import click
import httpx

logger = logging.getLogger()


async def generate_text(endpoint_url: str, payload: Dict) -> List[str]:
    result = []
    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint_url,
            json=payload,
        )
        if response.status_code == 200:
            data = response.json()
            if payload["stream"]:
                for token in data["tokens"]:
                    sys.stdout.write(token)
                    sys.stdout.flush()
            else:
                result.append(data["tokens"])
        else:
            logger.error(f"HTTP status code: {response.status_code}")
            logger.error(response.text)
            response.raise_for_status()

    return result


@click.command()
@click.option("--host", default="localhost", help="Host")
@click.option("--port", default=8000, help="Port")
@click.option("--stream", is_flag=True, help="Stream")
@click.option("--max-tokens", default=512, help="Max tokens")
@click.option("--temperature", default=0.7, help="Temperature")
def main(
    host: str,
    port: int,
    stream: bool,
    max_tokens: int,
    temperature: float,
):
    logging.basicConfig(level=logging.INFO)

    url = f"http://{host}:{port}/llm/generate"
    user_message = input("User(q) : ")

    payload = {
        "messages": [
            {"role": "user", "content": user_message},
        ],
        "stream": stream,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    if stream:
        asyncio.run(generate_text(url, payload))
    else:
        result = asyncio.run(generate_text(url, user_message))
        print(result)


if __name__ == "__main__":
    main()
