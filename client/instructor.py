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
        endpoint = f"{self.base_endpoint}/course/create"
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=data) as response:
                response.raise_for_status()
                data = await response.json()
                return data

    async def upload_file(self, course_id, file_path, meta_data):
        endpoint = f"{self.base_endpoint}/course/{course_id}/upload"

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=1800)
        ) as session:
            data = aiohttp.FormData()
            data.add_field(
                name="file",
                value=open(file_path, "rb"),
                filename="file.pdf",
                content_type="application/pdf",
            )
            for key, value in meta_data.items():
                data.add_field(key, value)
            async with session.post(endpoint, data=data) as response:
                return await response.json()


@click.command()
@click.option("--host", default="localhost", help="Host")
@click.option("--port", default=8000, help="Port")
@click.option("--create-course", default=None, help="Create new course")
@click.option("--upload", default=None, help="Upload new course content")
@coro
async def main(
    host: str,
    port: int,
    create_course: str,
    upload: str,
):
    logging.basicConfig(level=logging.INFO)

    client = JWTClient(f"http://{host}:{port}/v1")

    if create_course:
        course_description = click.prompt("? Like to give a description : ", type=str)
        instructor_name = click.prompt("? Enter author's name : ", type=str)

        course_data = {
            "name": create_course,
            "description": course_description,
            "instructor_name": instructor_name,
        }
        response = await client.create(data=course_data)
        print(response["course_id"])

    elif upload:
        course_id = click.prompt("? Enter course id", type=str)
        start_pgno = click.prompt("? Enter the starting pg no of the content: ")
        end_pgno = click.prompt("? Enter the ending pg no of the content: ")
        meta_data = {"start_pg_no": str(start_pgno), "end_pg_no": str(end_pgno)}

        response = await client.upload_file(
            course_id=course_id, file_path=upload, meta_data=meta_data
        )
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
