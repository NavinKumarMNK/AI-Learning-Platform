import asyncio

import aiohttp


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
        ) as response:  # Expect plain text
            if response.status == 200:
                async for word in response.content:  # Stream words
                    print(word.decode("utf-8").strip())  # Decode and print
            else:
                # Handle non-200 status codes
                raise Exception(f"Request failed with status code: {response.status}")


async def main():
    url = "http://localhost:8000/api/v1/chat/"
    await fetch_data(url)


if __name__ == "__main__":
    asyncio.run(main())
