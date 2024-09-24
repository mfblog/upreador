import requests
import orjson
import urllib.parse

with open("./info.json") as f:
    data = orjson.loads(f.read())

username = data["username"]
password = data["password"]
remote_bs = data["remote_booksource"].strip()  # 去掉多余空格
reader_addr = data["reader_addr"]
session = requests.session()


def login():
    login_url = "/reader3/login"
    url = urllib.parse.urljoin(reader_addr, login_url)
    # print(url)
    data = {"username": username, "password": password, "isLogin": True}
    headers = {
        "Content-Type": "application/json",
    }
    result = session.post(url, json=data, headers=headers).json()
    if str(result["isSuccess"]).lower() == "true":
        print("登陆成功")
    else:
        print(result)


def deleteBookSource():
    deleteBookSource_url = "/reader3/deleteAllBookSources"
    url = urllib.parse.urljoin(reader_addr, deleteBookSource_url)
    result = session.post(url).json()
    if str(result["isSuccess"]).lower() == "true":
        print("书源删除成功")
    else:
        print(result)


def get_remotebs():
    return requests.get(remote_bs).json()


def send_bs():
    remote_booksource = "/reader3/saveBookSources"
    url = urllib.parse.urljoin(reader_addr, remote_booksource)
    headers = {
        "Content-Type": "application/json",
    }
    data = get_remotebs()
    result = session.post(url, json=data, headers=headers).json()
    if str(result["isSuccess"]).lower() == "true":
        print("新增书源成功")
    else:
        print(result)


login()
deleteBookSource()
send_bs()
