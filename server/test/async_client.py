import asyncio
import sys
import aiohttp
import json


async def fetch_create_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 201:
                async for word in response.content:
                    return json.loads(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")


async def fetch_get_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async for word in response.content:
                    return word.decode("utf-8").strip()
            else:
                raise Exception(f"Request failed with status code: {response.status}")


async def fetch_list_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async for word in response.content:
                    return json.loads((word.decode("utf-8").strip()))
            else:
                raise Exception(f"Request failed with status code: {response.status}")


async def fetch_delete_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            if response.status == 204:
                async for word in response.content:
                    print(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")


async def fetch_completion_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                if data["stream"]:
                    async for line in response.content.iter_any():
                        yield line.decode("utf-8").strip()
                else:
                    text = await response.text()
                    yield text
            else:
                raise Exception(f"Request failed with status code: {response.status}")


async def fetch_patch_data(url, feedback):
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, params={"feedback": feedback}) as response:
            if response.status == 200:
                async for word in response.content:
                    print(word.decode("utf-8").strip())
            else:
                raise Exception(f"Request failed with status code: {response.status}")


async def main():
    import time

    user_id = "550e8400-e29b-41d4-a716-446655440000"

    # create req looks like
    st = time.time()
    url = "http://localhost:8000/v1/chat/create"  # create
    data = {
        "user_id": user_id,  # Example UUID
    }
    res = await fetch_create_data(url, data)
    chat_id = res["chat_id"]
    print(chat_id)
    print(time.time() - st)

    # chat completion
    st = time.time()
    url = f"http://localhost:8000/v1/chat/{chat_id}"  # post for chat completion
    data = data = {
        "messages": [
            {"role": "user", "content": "How are you?"},
        ],
        "stream": True,
        "course": "general",
    }

    if data["stream"]:
        async for lines in fetch_completion_data(url, data):
            sys.stdout.write(lines + " ")
            sys.stdout.flush()
        print("")
    else:
        async for res in fetch_completion_data(url, data):
            print(res + "\n")

    print(time.time() - st)

    st = time.time()
    url = f"http://localhost:8000/v1/chat/{chat_id}"  # post for chat completion
    data = data = {
        "messages": [
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "Anything you wish"},
            {"role": "user", "content": "This is X"},
        ],
        "stream": False,
        "course": "general",
    }

    if data["stream"]:
        async for lines in fetch_completion_data(url, data):
            sys.stdout.write(lines + " ")
            sys.stdout.flush()
        print("")
    else:
        async for res in fetch_completion_data(url, data):
            print(res)

    print(time.time() - st)

    # get list (user_id -> chat_id) mapping
    st = time.time()
    url = f"http://localhost:8000/v1/chat/user/{user_id}"  # list
    res = await fetch_list_data(url)
    print(res)
    print(time.time() - st)

    # get_particular chat
    st = time.time()
    url = f"http://localhost:8000/v1/chat/{chat_id}/retrieve"  # get (use valid, else will get 404 page not found)
    await fetch_get_data(url)
    print(time.time() - st)

    # feedback chat
    st = time.time()
    feedback = 3  # replace with your feedback value
    url = f"http://localhost:8000/v1/chat/{chat_id}/"
    await fetch_patch_data(url, feedback)
    print(time.time() - st)

    # delete the chat
    st = time.time()
    url = f"http://localhost:8000/v1/chat/{chat_id}/delete"  # delete (use valid, else will get 404 page not found)
    await fetch_delete_data(url)
    print(time.time() - st)


if __name__ == "__main__":
    asyncio.run(main())
