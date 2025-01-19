# upreador

此脚本用于给[假装大佬的reader3项目](https://github.com/hectorqin/reader)做书源推送
支持python3.9以上版本，python3.6请自行测试
此脚本可以部署在非reader服务器上

## 安装与使用

### 本地执行

拉取代码到本地目录

```bash
git clone https://github.com/akiooo45/upreador.git
```
创建虚拟环境
```bash
python3 -m venv venv
```

激活虚拟环境
```bash
source venv/bin/activate
```

安装依赖

```bash
pip install -r requirements.txt
```

根据需求修改info.json文件

```bash
vim info.json
```

执行脚本

```bash
python booksource.py
```

### 使用docker

拉取镜像

```bash
docker pull meifly/usersu-preador
```

修改info.json文件

执行容器(此命令在脚本执行完成后会自行删除容器)

```bash
docker run -it --rm  --name upderor -v data:/root/data meifly/usersu-preador
```

## 感谢

本项目感谢以下贡献者：

- **[mfblog]**：打包了docker镜像并上传
