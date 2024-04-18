import asyncio
from uvicorn import Server, Config


class MyServer(Server):
    async def run(self, sockets=None):
        self.config.setup_event_loop()
        return await self.serve(sockets=sockets)


async def run():
    apps = []

    # For the FastAPI server
    config1 = Config("server:app", host="0.0.0.0", port=8000, reload=True)
    server1 = MyServer(config=config1)
    apps.append(server1.run())

    # For the Chainlit server
    cmd = [
        "chainlit",
        "run",
        "chat/chainlit.py",
        "--host",
        "0.0.0.0",
        "--port",
        "8001",
        "-h",
    ]
    proc = await asyncio.create_subprocess_exec(*cmd)
    apps.append(proc.wait())

    return await asyncio.gather(*apps)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
