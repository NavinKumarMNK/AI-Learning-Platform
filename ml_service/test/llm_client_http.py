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
    headers = {"Content-Type": "application/json"}
    print(payload)

    async with httpx.AsyncClient() as client:
        if payload["stream"]:
            async with client.stream(
                method="POST",
                url=endpoint_url,
                json=payload,
                headers=headers,
                timeout=30,
            ) as response:
                if response.status_code == 200:
                    async for line in response.aiter_lines():
                        # Parse the line from a JSON string to a dictionary
                        line_dict = json.loads(line)
                        # Process each line here
                        sys.stdout.write(line_dict['output'])
                        sys.stdout.flush()
                else:
                    logger.error(f"HTTP status code: {response.status_code}")
                    logger.error(response.text)
                    response.raise_for_status()
        else:
            response = await client.post(
                endpoint_url, json=payload, headers=headers, timeout=30
            )
            response.raise_for_status()
            result = response.json()

    return result


@click.command()
@click.option("--host", default="localhost", help="Host")
@click.option("--port", default=8000, help="Port")
@click.option("--stream", default=True, help="Stream")
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

    url = f"http://{host}:{port}/api/v1/llm/generate"
    user_message = input("User(q) : ")

    payload = {
        "messages": [
            {"role": "user", "content": user_message},
        ],
        "prompt": user_message,
        "stream": stream,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    if stream:
        asyncio.run(generate_text(url, payload))
        print("\n")
    else:
        result = asyncio.run(generate_text(url, payload))
        print(json.loads(result)['output'])


if __name__ == "__main__":
    main()
