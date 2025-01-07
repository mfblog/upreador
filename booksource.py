import orjson
import aiohttp
import asyncio


with open("./data/info.json") as f:
    data = orjson.loads(f.read())

username = data["username"]
password = data["password"]
remote_bs = data["remote_booksource"].strip()
reader_addr = data["reader_addr"]


# Get remote booksource
async def get_booksource():
    async with aiohttp.ClientSession() as session:
        async with session.get(remote_bs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print("Get booksource failed, Please check your remote booksource url")


# Update reader booksources
async def update_booksource():
    async with aiohttp.ClientSession(base_url=reader_addr) as session:
        headers = {"Content-Type": "application/json"}
        login_data = {"username": username, "password": password, "isLogin": True}
        # login reader
        async with session.request(
            "POST", "/reader3/login", json=login_data, headers=headers
        ) as response:
            if "true" in await response.text():
                print("Login success")
            else:
                print("Login failed")

        # delete All BookSources
        async with session.request(
            "POST", "/reader3/deleteAllBookSources", headers=headers
        ) as response:
            if "true" in await response.text():
                print("Delete all booksources success")
            else:
                print("Delete all booksources failed")
        # Update booksources wi  reader
        json = await get_booksource()
        async with session.request(
            "POST", "/reader3/saveBookSources", json=json, headers=headers
        ) as response:
            if "true" in await response.text():
                print("Update booksources success")
            else:
                print("Update booksources failed")


async def main():
    await update_booksource()


asyncio.run(main())
