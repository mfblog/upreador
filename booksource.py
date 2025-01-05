import orjson
import aiohttp
import asyncio


with open("./info.json") as f:
    data = orjson.loads(f.read())

username = data["username"]
password = data["password"]
remote_bs = data["remote_booksource"].strip()  # 去掉多余空格
reader_addr = data["reader_addr"]

login_data = {"username": username, "password": password, "isLogin": True}


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
        async with session.request(
            "POST", "/reader3/login", json=login_data, headers=headers
        ) as response:
            if response.status == 200:
                print("Login success")
            else:
                print("Login failed, Please check your username and password")

    async with aiohttp.ClientSession(base_url=reader_addr) as session:
        headers = {"Content-Type": "application/json"}
        async with session.request(
            "POST", "/reader3/deleteAllBookSources", headers=headers
        ) as response:
            assert response.status == 200
            print("Delete all booksources success")

        json = await get_booksource()
        async with session.request(
            "POST", "/reader3/saveBookSources", json=json, headers=headers
        ) as response:
            assert response.status == 200
            print("Update booksources success")


async def main():
    await update_booksource()


asyncio.run(main())
