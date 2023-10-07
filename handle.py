﻿import json
import aiohttp
import asyncio
import os


def readMap(name) -> dict:
    fs = open(f"./maps/{name}.map", "r")
    res = json.loads(fs.read())
    fs.close()
    return res


def file_get(path):
    if (not os.path.exists(path)):
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


async def lan():
    resList = list()
    resStr = "payload:\n"
    other = readMap("other")
    resList.append(other["本地局域网地址"])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += f"  - {line}\n"
    resStr = resStr.replace("  - DOMAIN-SUFFIX,10.in-addr.arpa\n", "")
    resStr = resStr.replace("  - IP-CIDR,10.0.0.0/8,no-resolve\n", "")
    resStr = resStr.replace("  - IP-CIDR,172.16.0.0/12,no-resolve\n", "")
    fs = open("./rule/lan.list", "w")
    fs.write(resStr)
    fs.close()


async def globalDirect():
    resList = list()
    resStr = "payload:\n"
    mainland = readMap("mainland")
    cnmedia = readMap("mainlandmedia").keys()
    other = readMap("other")
    game = readMap("game")
    resList.append(game["SteamCN"])
    resList.append(game["GameDownloadCN"])
    resList.append(game["米哈游HoYoverse"])
    resList.append(game["腾讯英雄联盟手游"])
    for key in other.keys():
        if key.find("云计算") != -1:
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
            resStr += f"  - {line}\n"

    resStr = resStr.replace("  - DOMAIN-SUFFIX,10.in-addr.arpa\n", "")
    resStr = resStr.replace("  - IP-CIDR,10.0.0.0/8,no-resolve\n", "")
    resStr = resStr.replace("  - IP-CIDR,172.16.0.0/12,no-resolve\n", "")
    fs = open("./rule/globalDirect.list", "w")
    fs.write(resStr)
    fs.close()


async def pselect():
    resList = list()
    resStr = "payload:\n"
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
            resStr += f"  - {line}\n"

    fs = open("./rule/pselect.list", "w")
    fs.write(resStr)
    fs.close()


async def cnmedia():
    resList = list()
    resStr = "payload:\n"
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
            resStr += f"  - {line}\n"
    fs = open("./rule/cnmedia.list", "w")
    fs.write(resStr)
    fs.close()


async def media():
    resList = list()
    resStr = "payload:\n"
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
            resStr += f"  - {line}\n"
    fs = open("./rule/globalmedia.list", "w")
    fs.write(resStr)
    fs.close()


async def apple():
    resList = list()
    resStr = "payload:\n"
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
            resStr += f"  - {line}\n"
    fs = open("./rule/apple.list", "w")
    fs.write(resStr)
    fs.close()


async def game():
    resList = list()
    resStr = "payload:\n"
    game = readMap("game")
    game.pop("SteamCN")
    game.pop("GameDownloadCN")
    game.pop("米哈游HoYoverse")
    game.pop("腾讯英雄联盟手游")
    for key in game.keys():
        resList.append(game[key])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += f"  - {line}\n"
    fs = open("./rule/game.list", "w")
    fs.write(resStr)
    fs.close()


async def ms():
    resList = list()
    resStr = "payload:\n"
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
            resStr += f"  - {line}\n"
    fs = open("./rule/ms.list", "w")
    fs.write(resStr)
    fs.close()


async def ai():
    resList = list()
    resStr = "payload:\n"
    gb = readMap("global")
    resList.append(gb['OpenAI'])
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += f"  - {line}\n"
    fs = open("./rule/openai.list", "w")
    fs.write(resStr)
    fs.close()

async def cqu():
    resList = list()
    resStr = "payload:\n"
    resList.append("./files/cqu.list")
    for url in resList:
        data = file_get(url)
        for line in data.split("\n"):
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            resStr += f"  - {line}\n"
    fs = open("./rule/cqu.list", "w")
    fs.write(resStr)
    fs.close()

async def qhandle():
    fns = ['globalDirect', 'pselect', 'ms', 'apple', 'openai',
          'game', 'globalmedia', 'cnmedia', 'cqu', 'lan']
    tags = ['🎯 全球直连','🚀 节点选择','Ⓜ️ 微软服务',' 苹果服务','💬 OpenAI','🎮 游戏平台','🌍 国外媒体','📺 国内媒体','🕋 重大服务','Direct']
    
    for i in range(0,len(fns)):
        tag = tags[i]
        fn = fns[i]
        resStr = ""
        rule = file_get(f"./rule/{fn}.list")
        rule = rule.replace("payload:\n","")
        rule = rule.replace("  - ","")
        rule = rule.replace("IP-CIDR6,","IP6-CIDR,")
        rule = rule.replace("DOMAIN,","HOST,")
        rule = rule.replace("DOMAIN-SUFFIX,","HOST-SUFFIX,")
        rule = rule.replace("DOMAIN-KEYWORD,","HOST-KEYWORD,")
        for line in rule.split("\n"):
            if line == "":
                continue
            params = line.split(",")
            if(params[0] == 'PROCESS-NAME'):
                continue
            if(len(params) == 3):
                resStr += f"{params[0]},{params[1]},{tag},no-resolve\n"
            else:
                resStr += f"{line},{tag}\n"
        fs = open(f"./qrule/{fn}.list","w")
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
    await lan()
    await qhandle()

asyncio.run(main())
