# Blog post reference: https://www.codingforentrepreneurs.com/blog/python-jwt-client-django-rest-framework-simplejwt

from dataclasses import dataclass
import requests
from getpass import getpass
import pathlib
import json
import aiohttp
import asyncio
import aiofiles

headers = {"Content-Type": "application/json"}


@dataclass
class JWTClient:
    """
    Use a dataclass decorator
    to simply the class construction
    """

    access: str = None
    refresh: str = None
    # ensure this matches your simplejwt config
    header_type: str = "Bearer"
    # this assumesy ou have DRF running on localhost:8000
    base_endpoint = "http://localhost:8000/v1"
    # this file path is insecure
    cred_path: pathlib.Path = pathlib.Path("creds.json")

    def __post_init___(self):
        if self.cred_path.exists():
            """
            You have stored creds,
            let's verify them
            and refresh them.
            If that fails,
            restart login process.
            """
            try:
                data = json.loads(self.cred_path.read_text())
            except Exception:
                print("Assuming creds has been tampered with")
                data = None
            if data is None:
                """ 
                Clear stored creds and
                Run login process
                """
                self.clear_tokens()
                self.perform_auth()
            else:
                """
                `creds.json` was not tampered with
                Verify token -> 
                if necessary, Refresh token ->
                if necessary, Run login process
                """
                self.access = data.get("access")
                self.refresh = data.get("refresh")
                token_verified = self.verify_token()
                if not token_verified:
                    """
                    This can mean the token has expired
                    or is invalid. Either way, attempt
                    a refresh.
                    """
                    refreshed = self.perform_refresh()
                    if not refreshed:
                        """
                        This means the token refresh
                        also failed. Run login process
                        """
                        print("invalid data, login again.")
                        self.clear_tokens()
                        self.perform_auth()
        else:
            """
            Run login process
            """
            self.perform_auth()

    async def get_headers(self, header_type=None):
        """Default headers for HTTP requests including the JWT token"""
        _type = header_type or self.header_type
        token = self.access
        if not token:
            return {}
        return {"Authorization": f"{_type} {token}"}

    def perform_auth(self):
        """
        Simple way to perform authentication
        Without exposing password(s) during the
        collection process.
        """
        endpoint = f"{self.base_endpoint}/token/"
        username = input("What is your username?\n")
        password = getpass("What is your password?\n")
        r = requests.post(endpoint, json={"username": username, "password": password})
        if r.status_code != 200:
            raise Exception(f"Access not granted: {r.text}")
        print("access granted")
        self.write_creds(r.json())

    def write_creds(self, data: dict):
        """
        Store credentials as a local file
        and update instance with correct
        data.
        """
        if self.cred_path is not None:
            self.access = data.get("access")
            self.refresh = data.get("refresh")
            if self.access and self.refresh:
                self.cred_path.write_text(json.dumps(data))

    def verify_token(self):
        """
        Simple method for verifying your
        token data. This method only verifies
        your `access` token. A 200 HTTP status
        means success, anything else means failure.
        """
        data = {"token": f"{self.access}"}
        endpoint = f"{self.base_endpoint}/token/verify/"
        r = requests.post(endpoint, json=data)
        return r.status_code == 200

    def clear_tokens(self):
        """
        Remove any/all JWT token data
        from instance as well as stored
        creds file.
        """
        self.access = None
        self.refresh = None
        if self.cred_path.exists():
            self.cred_path.unlink()

    def perform_refresh(self):
        """
        Refresh the access token by using the correct
        auth headers and the refresh token.
        """
        print("Refreshing token.")
        headers = self.get_headers()
        data = {"refresh": f"{self.refresh}"}
        endpoint = f"{self.base_endpoint}/token/refresh/"
        r = requests.post(endpoint, json=data, headers=headers)
        if r.status_code != 200:
            self.clear_tokens()
            return False
        refresh_data = r.json()
        if "access" not in refresh_data:
            self.clear_tokens()
            return False
        stored_data = {"access": refresh_data.get("access"), "refresh": self.refresh}
        self.write_creds(stored_data)
        return True

    async def create(self, data):
        # headers = await self.get_headers()
        endpoint = f"{self.base_endpoint}/course/create"
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=data) as response:
                response.raise_for_status()  # Raise exception for non-2xx status codes
                data = await response.json()
                return data

    async def get(self, course_id):
        # headers = await self.get_headers()
        endpoint = f"{self.base_endpoint}/course/{course_id}/retrieve"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data

    async def update(self, course_id, data):
        # headers = await self.get_headers()
        endpoint = f"{self.base_endpoint}/course/{course_id}/update"
        async with aiohttp.ClientSession() as session:
            async with session.patch(endpoint, headers=headers, json=data) as response:
                response.raise_for_status()
                return response.status

    async def delete(self, course_id):
        # headers = await self.get_headers()
        endpoint = f"{self.base_endpoint}/course/{course_id}/delete"
        async with aiohttp.ClientSession() as session:
            async with session.delete(endpoint, headers=headers) as response:
                response.raise_for_status()
                return response.status

    async def upload_file(self, course_id, file_path, meta_data):
        endpoint = f"{self.base_endpoint}/course/{course_id}/upload"

        async with aiohttp.ClientSession() as session:
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


async def main():
    client = JWTClient()
    import time

    # create course
    st = time.time()
    import random

    data = {
        "name": str(random.randint(1, 1000000000)),
        "description": "still better",
        "instructor_name": "abcdef",
    }
    response = await client.create(data=data)
    print(time.time() - st)
    print(response)
    course_id = response["course_id"]

    # get the course details
    st = time.time()
    response = await client.get(course_id=course_id)
    print(response)
    print(time.time() - st)

    # update the data in course
    update_data = {
        "description": "changed",
        "instructor_name": "abcdef",
    }
    st = time.time()
    response = await client.update(course_id=course_id, data=update_data)
    print(response)
    print(time.time() - st)

    # upload a file for processing
    file_path = "../temp/pdf_loader_test_1.pdf"
    meta_data = {"start_pg_no": "1", "end_pg_no": "6"}
    st = time.time()
    response = await client.upload_file(
        course_id=course_id, file_path=file_path, meta_data=meta_data
    )
    print(response)
    print(time.time() - st)

    # delete the record
    st = time.time()
    response = await client.delete(course_id=course_id)
    print(response)
    print(time.time() - st)


if __name__ == "__main__":
    asyncio.run(main())
