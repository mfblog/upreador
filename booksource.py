import aiohttp
import asyncio
import orjson
import urllib.parse

# Load the data from the JSON file
with open("./info.json") as f:
    data = orjson.loads(f.read())

username = data["username"]
password = data["password"]
remote_bs = data["remote_booksource"]
reader_addr = data["reader_addr"]


# 登录到reader3
async def login(session):
    login_url = "/reader3/login"
    url = urllib.parse.urljoin(reader_addr, login_url)
    data = {"username": username, "password": password, "isLogin": True}
    headers = {"Content-Type": "application/json"}

    async with session.post(url, json=data, headers=headers) as response:
        result = await response.json()
        print(result)
        print("\n")


# 删除reader3本地书源
async def deleteBookSource(session):
    deleteBookSource_url = "/reader3/deleteAllBookSources"
    url = urllib.parse.urljoin(reader_addr, deleteBookSource_url)

    async with session.post(url) as response:
        result = await response.json()
        print(result)


# 获取远程书源
async def get_remotebs(session):
    for i in remote_bs:
        async with session.get(i) as response:
            return await response.json()


# 推送书源到reader3
async def send_bs(session):
    remote_booksource = "/reader3/saveBookSources"
    url = urllib.parse.urljoin(reader_addr, remote_booksource)
    headers = {"Content-Type": "application/json"}

    payload = await get_remotebs(session)
    async with session.post(url, json=payload, headers=headers) as response:
        result = await response.json()
        print(result)


# Main function to run all tasks
async def main():
    async with aiohttp.ClientSession() as session:
        await login(session)
        await deleteBookSource(session)
        await send_bs(session)


# Run the main function
asyncio.run(main())
