import asyncio
import json
import logging
import sys
from typing import Dict, List
import traceback
import click
import httpx

from rich.console import Console

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)
logger = logging.getLogger()


async def generate_text(endpoint_url: str, payload: Dict) -> List[str]:
    result = []
    headers = {"Content-Type": "application/json"}

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
                        res = line_dict["output"]
                        sys.stdout.write(res)
                        sys.stdout.flush()
                        result.append(res)
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
@click.option("--max-tokens", default=4096, help="Max tokens")
@click.option("--temperature", default=0.3, help="Temperature")
@click.option(
    "--is-prompt",
    default=False,
    help="Format of input, if prompt then \
              set True. Default is False ",
)
def main(
    host: str,
    port: int,
    stream: bool,
    max_tokens: int,
    temperature: float,
    is_prompt: bool,
):
    logging.basicConfig(level=logging.INFO)

    console = Console()
    url = f"http://{host}:{port}/api/v1/llm/generate"
    print("""Hi, This is MegAcad, your AI Educational Tutor
You can type the prompts (or) messages.
Please be polite. Remember AI can make mistake.""")

    messages = []
    i = 0
    # console.begin_capture()
    while i <= 30:
        try:
            user_message = console.input(">>> ")
            if user_message == "\\q":
                print("Session Exited")
                break
            if user_message == "\\n":
                print("New Session")
                messages = []
                continue

            if is_prompt:
                payload = {
                    "prompt": user_message,
                    "stream": stream,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
            else:
                messages.append({"role": "user", "content": user_message})
                payload = {
                    "messages": messages,
                    "stream": stream,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }

            if stream:
                assistant_message = asyncio.run(generate_text(url, payload))
                assistant_message = "".join(assistant_message)
                print("\n")
            else:
                result = asyncio.run(generate_text(url, payload))
                assistant_message = result["output"]
                sys.stdout.write(assistant_message + "\n")

            messages.append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            print("\n")
            logger.error(e)
            traceback.print_exc()

        i += 1

if __name__ == "__main__":
    main()
