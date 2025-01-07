### 需要把info里面的用户名密码删除掉

import orjson
import aiohttp
import asyncio

# 读取配置文件
with open("./info.json") as f:
    data = orjson.loads(f.read())

# 获取配置信息
remote_bs = data["remote_booksource"].strip()
reader_addr = data["reader_addr"]

# 获取远程书源
async def get_booksource():
    async with aiohttp.ClientSession() as session:
        async with session.get(remote_bs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print("获取书源失败，请检查远程书源URL")

# 更新阅读器书源
async def update_booksource():
    async with aiohttp.ClientSession(base_url=reader_addr) as session:
        headers = {"Content-Type": "application/json"}

        # 删除所有书源
        async with session.request(
            "POST", "/reader3/deleteAllBookSources", headers=headers
        ) as response:
            if "true" in await response.text():
                print("删除所有书源成功")
            else:
                print("删除所有书源失败")

        # 更新书源
        json = await get_booksource()
        async with session.request(
            "POST", "/reader3/saveBookSources", json=json, headers=headers
        ) as response:
            if "true" in await response.text():
                print("更新书源成功")
            else:
                print("更新书源失败")

# 主函数
async def main():
    await update_booksource()

# 运行主函数
asyncio.run(main())
