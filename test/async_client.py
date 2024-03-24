import asyncio

import aiohttp


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
            
async def fetch_list_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url
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
                # updated_data = await response.json()  # Read the response JSON data
                # print("Resource updated successfully. Updated data:", updated_data)
                async for word in response.content:
                    print(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")


async def main():
    # url = "http://localhost:8000/api/v1/chat/" # create
    # url = "http://localhost:8000/api/v1/chat/user/550e8400-e29b-41d4-a716-446655440000" # list
    # url = "http://localhost:8000/api/v1/chat/8436218b-7324-4f27-836a-525a691cef54" # get (use valid, else will get 404 page not found)
    # url = "http://localhost:8000/api/v1/chat/8436218b-7324-4f27-836a-525a691cef54/delete" # delete (use valid, else will get 404 page not found)
    url = "http://localhost:8000/api/v1/chat/86f7e57c-ae58-4474-9c2a-b83383d6b4d3/update" # update (use valid, else will get 404 page not found)


    data = {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",  # Example UUID
        "messages": [{"role": "user", "content": "say dude what apple color"}],  # Example message data
        "title": "Apple color dono"  # Example title
    }


    # await fetch_create_data(url, data)
    # await fetch_get_data(url)
    # await fetch_list_data(url)
    # await fetch_delete_data(url)
    await fetch_update_data(url, data)


if __name__ == "__main__":
    asyncio.run(main())
