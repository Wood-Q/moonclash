import json
import aiohttp
import asyncio
import os


def readMap(name) -> dict:
    fs = open(f"./maps/{name}.map", "r")
    res = json.loads(fs.read())
    fs.close()
    return res


def file_get(path):
    if(not os.path.exists(path)):
        print(f"{path} does not exist")
        return ""
    fs = open(path, "r")
    res = fs.read()
    fs.close()
    return res


async def httpGet(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:  # Check if the response status is OK
                data = await resp.text()  # Parse JSON from the response
                return data
            else:
                return None

async def globalDirect():
    resList = list()
    resStr = ""
    mainland = readMap("mainland")
    cnmedia = readMap("mainlandmedia").keys()
    other = readMap("other")
    game = readMap("game")
    resList.append(game["SteamCN"])
    for key in other.keys():
        if key == "本地局域网地址" or key.find("云计算") != -1:
            resList.append(other[key])

    for key in mainland.keys():
        if key not in cnmedia:
            resList.append(mainland[key])

    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"

    resStr = resStr.replace("DOMAIN-SUFFIX,10.in-addr.arpa\n", "")
    resStr = resStr.replace("IP-CIDR,10.0.0.0/8,no-resolve\n", "")
    resStr = resStr.replace("IP-CIDR,172.16.0.0/12,no-resolve\n", "")
    fs = open("./rule/globalDirect.list", "w")
    fs.write(resStr)
    fs.close()

async def pselect():
    resList = list()
    resStr = ""
    gb = readMap("global")
    gb.pop("OpenAI")

    exclued = list(readMap("globalmedia").keys())
    exclued = exclued + list(readMap("apple").keys())
    exclued = exclued + list(readMap("Microsoft").keys())
    other = readMap("other")
    resList.append("./files/autodesk.list")
    for key in other.keys():
        if key != "本地局域网地址" and key.find("云计算") == -1:
            resList.append(other[key])

    for key in gb.keys():
        if key not in exclued:
            resList.append(gb[key])

    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"

    fs = open("./rule/pselect.list", "w")
    fs.write(resStr)
    fs.close()

async def cnmedia():
    resList = list()
    resStr = ""
    cnmedia = readMap("mainlandmedia")
    for key in cnmedia.keys():
            resList.append(cnmedia[key])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"
    fs = open("./rule/cnmedia.list", "w")
    fs.write(resStr)
    fs.close()

async def media():
    resList = list()
    resStr = ""
    globalmedia = readMap("globalmedia")
    for key in globalmedia.keys():
            resList.append(globalmedia[key])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"
    fs = open("./rule/globalmedia.list", "w")
    fs.write(resStr)
    fs.close()

async def apple():
    resList = list()
    resStr = ""
    apple = readMap("apple")
    for key in apple.keys():
            resList.append(apple[key])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"
    fs = open("./rule/apple.list", "w")
    fs.write(resStr)
    fs.close()

async def game():
    resList = list()
    resStr = ""
    game = readMap("game")
    game.pop("SteamCN")
    for key in game.keys():
            resList.append(game[key])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"
    fs = open("./rule/game.list", "w")
    fs.write(resStr)
    fs.close()

async def ms():
    resList = list()
    resStr = ""
    ms = readMap("Microsoft")
    for key in ms.keys():
            resList.append(ms[key])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"
    fs = open("./rule/ms.list", "w")
    fs.write(resStr)
    fs.close()

async def ai():
    resList = list()
    resStr = ""
    gb = readMap("global")
    resList.append(gb['OpenAI'])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"
    fs = open("./rule/openai.list", "w")
    fs.write(resStr)
    fs.close()

async def cqu():
    resList = list()
    resStr = ""
    resList.append("./files/cqu.list")
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += line+"\n"
    fs = open("./rule/cqu.list", "w")
    fs.write(resStr)
    fs.close()

async def main():
    await globalDirect()
    await pselect()
    await ms()
    await ai()
    await game()
    await apple()
    await media()
    await cnmedia()
    await cqu()

asyncio.run(main())
