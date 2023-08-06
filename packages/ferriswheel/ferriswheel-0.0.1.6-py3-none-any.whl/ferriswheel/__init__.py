import aiohttp
import asyncio

api_uri = "https://api.ferris.chat/api/v0/"

async def run_client(token: str):
    auth_headers = {"Authorization": token}

    async with aiohttp.ClientSession(headers=auth_headers) as session:
        async with session.get(api_uri) as response:

            print("Status:", response.status)
            html = await response.text()
            print("Body:", html[:15], "...")


def run(token: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_client(token))
