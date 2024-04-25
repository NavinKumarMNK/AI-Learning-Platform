from functools import wraps
import asyncio
import json
import logging
import sys
from typing import Dict, List
import traceback
import click
import httpx
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

from dataclasses import dataclass
import requests
from getpass import getpass
import pathlib
import json
import aiohttp


httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)
logger = logging.getLogger()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@dataclass
class JWTClient:
    def __init__(self, endpoint):
        self.base_endpoint = endpoint

    async def create(self, data):
        endpoint = f"{self.base_endpoint}/chat/create"

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=data) as response:
                if response.status == 201:
                    async for word in response.content:
                        return json.loads(word.decode("utf-8").strip())
                else:
                    raise Exception(
                        f"Request failed with status code: {response.status}"
                    )

    async def patch(self, chat_id, feedback):
        endpoint = f"{self.base_endpoint}/chat/{chat_id}/"

        async with aiohttp.ClientSession() as session:
            async with session.patch(
                endpoint, params={"feedback": feedback}
            ) as response:
                if response.status == 200:
                    async for word in response.content:
                        print(word.decode("utf-8").strip())
                else:
                    raise Exception(
                        f"Request failed with status code: {response.status}"
                    )

    async def generate_text(self, chat_id: str, payload: Dict) -> List[str]:
        endpoint_url = f"{self.base_endpoint}/chat/{chat_id}"
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
                    follow_redirects=True,
                ) as response:
                    if response.status_code == 200:
                        async for line in response.aiter_lines():
                            # Parse the line from a JSON string to a dictionary
                            res = line
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


async def create_chat(client: JWTClient, user_id: str):
    data = {
        "user_id": user_id,
    }
    res = await client.create(data)
    chat_id = res["chat_id"]
    return chat_id


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

    client = JWTClient(f"http://{host}:{port}/v1")

    welcome_message = Text("""Hello, this is MegAcad, your AI Educational Tutor 
You can type the prompts or messages 
Please be polite towards me & Remember, I can make mistakes too """)
    welcome_message = Panel(welcome_message, title="MegAcad AI")
    console.print(welcome_message)
    messages = []
    session = PromptSession(history=FileHistory(".history"))

    # user_id = 8d1c082a-95eb-4a8d-ab1b-1cfa0a63e21a
    user_id = click.prompt("? Enter user id to login", type=str)
    chat_id = asyncio.run(create_chat(client, user_id))
    print(chat_id)
    i = 0
    while i <= 30:
        try:
            user_message = session.prompt(">>> ")
            if user_message == "\\q":
                print("Session Exited")
                break
            elif user_message == "\\n":
                messages = []
                console.clear()
                console.print("New Session")
                console.print(welcome_message)

                chat_id = asyncio.run(create_chat(client, user_id))

                continue
            elif user_message.strip() == "":
                continue
            elif user_message == "\\c":
                console.clear()
                continue
            elif user_message[:2] == "\\f":
                for num in user_message:
                    if num in ["1", "2", "3", "4", "5"]:
                        feedback = int(num)
                        break
                asyncio.run(client.patch(chat_id, feedback))
                print("Feedback received", feedback)
                continue

            course_id = "8159e979-c87f-47ba-b482-9948854a52b7"
            if is_prompt:
                payload = {
                    "prompt": user_message,
                    "stream": stream,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "course_id": course_id,
                }
            else:
                messages.append({"role": "user", "content": user_message})
                payload = {
                    "messages": messages,
                    "stream": stream,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "course_id": course_id,
                }

            if stream:
                assistant_message = asyncio.run(client.generate_text(chat_id, payload))
                assistant_message = " ".join(assistant_message)
                sys.stdout.write(assistant_message + "\n")
            else:
                print("entered")
                result = asyncio.run(client.generate_text(chat_id, payload))
                assistant_message = " ".join(assistant_message)
                sys.stdout.write(assistant_message + "\n")

            messages.append({"role": "assistant", "content": assistant_message})

        except Exception as e:
            print("\n")
            logger.error(e)
            traceback.print_exc()

        i += 1


if __name__ == "__main__":
    main()
