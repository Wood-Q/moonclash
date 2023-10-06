import aiohttp
import asyncio
import yaml
import re
import json
from typing import Union
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware


async def httpGet(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:  # Check if the response status is OK
                data = await resp.text()  # Parse JSON from the response
                return data
            else:
                return None


async def getProxies(attr: int):
    url = "https://api.stentvessel.top/sub?target=clash&new_name=true&emoji=true&clash.doh=true&filename=YToo_SS&udp=true&config=https%3A%2F%2Fsubweb.s3.fr-par.scw.cloud%2FRemoteConfig%2Fcustomized%2Fytoo.ini&url=https%3A%2F%2Fapi.ytoo.xyz%2Fosubscribe.php%3Fsid%3D37854%26token%3Di9S5KxiwJZgx%26sip002%3D1"
    res = await httpGet(url)
    data = yaml.safe_load(res)

    rstr = ['日用.*香港', '日用.*美国', '日用.*日本', '标准.*香港', '标准.*美国', '标准.*日本','标准.*台湾','标准.*日本','标准.*韩国','阿根廷'][attr]
    res = list()
    for v in data['proxies']:
        if re.search(rstr, v['name']) != None:
            v["skip-cert-verify"]=True
            res.append(v)

    yamls = yaml.dump({"proxies": res}, allow_unicode=True)
    return yamls


async def getRules(attr: int):
    fs = open("./rules.json", "r")
    data = json.loads(fs.read())
    fs.close()
    rule = ""
    for url in data[attr]['urls']:
        resp = await httpGet(url)
        resp = resp.replace("IP6-CIDR","IP-CIDR6")
        for line in resp.split("\n"):
            params = line.split(",")

            # 一些例外需要调整的情况
            if (len(params) < 2):
                continue
            if (params[0] == "USER-AGENT"):
                continue
            if (params[1] == "10.0.0.0/8"):
                continue
            if (params[1] == "172.16.0.0/12"):
                continue
            # 例外结束
            if (len(params) == 4):
                rule += f"{params[0]},{params[1]},{params[3]}\n"
            else:
                rule += f"{params[0]},{params[1]}\n"
    return rule

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/ps")
async def read_root(attr: int):
    return PlainTextResponse(content=await getProxies(attr))


@app.get("/rule")
async def read_root(attr: int):
    return PlainTextResponse(content=await getRules(attr))
