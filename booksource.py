import aiohttp
import asyncio
import orjson
import urllib.parse

# Load the data from the JSON file
with open("./info.json") as f:
    data = orjson.loads(f.read())

username = data["username"]
password = data["password"]
remote_bs = data["remote_booksource"].strip()  # 去掉多余空格
reader_addr = data["reader_addr"]


# 登录到reader3
async def login(session):
    login_url = "/reader3/login"
    url = urllib.parse.urljoin(reader_addr, login_url)
    data = {"username": username, "password": password, "isLogin": True}
    headers = {"Content-Type": "application/json"}

    async with session.post(url, json=data, headers=headers) as response:
        result = await response.json()
        # print("登录结果:", result)

        # 判断是否登录成功
        if result.get("isSuccess"):
            print("登录成功", result)
            return True  # 这里可以返回 True 或者直接返回 None
        else:
            print("登录失败:", result.get("errorMsg", "未知错误"))
            return False  # 返回 False 表示登录失败


# 删除reader3本地书源
async def deleteBookSource(session):
    deleteBookSource_url = "/reader3/deleteAllBookSources"
    url = urllib.parse.urljoin(reader_addr, deleteBookSource_url)

    async with session.post(url) as response:
        result = await response.json()
        print("删除书源结果:", result)


# 获取单个远程书源
async def get_remotebs(session):
    print("获取的远程书源地址:", remote_bs)  # 确认地址
    if not isinstance(remote_bs, str) or not remote_bs:
        raise ValueError("remote_bs 必须是一个有效的字符串 URL")

    async with session.get(remote_bs) as response:
        return await response.json()


# 推送书源到reader3
async def send_bs(session, payload):
    remote_booksource = "/reader3/saveBookSources"
    url = urllib.parse.urljoin(reader_addr, remote_booksource)
    headers = {"Content-Type": "application/json"}

    async with session.post(url, json=payload, headers=headers) as response:
        result = await response.json()
        print("推送书源结果:", result)


# Main function to run all tasks
async def main():
    async with aiohttp.ClientSession() as session:
        # 首先进行登录操作
        login_success = await login(session)

        if login_success:
            # 登录成功后并发执行删除本地书源和获取远程书源的任务
            delete_task = deleteBookSource(session)
            fetch_task = get_remotebs(session)

            # 并发执行删除本地书源和获取远程书源
            _, remote_book_sources = await asyncio.gather(delete_task, fetch_task)

            # 然后推送书源
            await send_bs(session, remote_book_sources)
        else:
            print("登录失败，无法继续执行后续操作。")


# Run the main function
asyncio.run(main())
