import asyncio

import aiohttp
import requests


async def fetch_create_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, json=data
        ) as response:
            if response.status == 201:
                async for word in response.content:
                    print(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")

async def fetch_get_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url
        ) as response:
            if response.status == 200:
                async for word in response.content:
                    print(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")
            
async def fetch_list_data(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, headers=headers
        ) as response:
            if response.status == 200:
                async for word in response.content:
                    print(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")

async def fetch_delete_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            url
        ) as response:
            if response.status == 204:
                async for word in response.content:
                    print(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")

async def fetch_update_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.patch(
            url, json=data
        ) as response:
            if response.status == 200:
                async for word in response.content:
                    print(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")

            

async def main():
    auth_url = "http://localhost:8000/api/v1/auth"
    auth_response = requests.post(auth_url, json={
        "username" : "",
        "password" : ""})
    print(auth_response.json())

    if auth_response.status_code == 200:

        # url = "http://localhost:8000/api/v1/user/" # create
        # url = "http://localhost:8000/api/v1/user/c1b3bb6e-9d3a-484d-8026-0929004c03a4" # get (use valid, else will get 404 page not found)
        url = "http://localhost:8000/api/v1/user/users" # list
        # url = "http://localhost:8000/api/v1/user/c1b3bb6e-9d3a-484d-8026-0929004c03a4/delete" # delete (use valid, else will get 404 page not found)
        # url = "http://localhost:8000/api/v1/user/b3459df8-2785-450c-bcb9-13e529f82041/update" # update (use valid, else will get 404 page not found)


        data = {
            # "email": "example3@gmail.com",
            # "password": "12345678",
            # "role" : "instructor"
        }

        token = auth_response.json()["token"]
        headers = {
            "Authorization": f"Token {token}"
        }


        # await fetch_create_data(url, data)
        # await fetch_get_data(url)
        await fetch_list_data(url, headers)
        # await fetch_delete_data(url)
        # await fetch_update_data(url, data)


if __name__ == "__main__":
    asyncio.run(main())
