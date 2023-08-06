import aiohttp
import asyncio

api_uri = "https://api.ferris.chat/api/v0/"

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get(api_uri) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
