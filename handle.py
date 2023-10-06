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
    fs = open(path,"r")
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


async def main():
    await globalDirect()

asyncio.run(main())
