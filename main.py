import aiohttp
import asyncio
import yaml
import re
import json
import os
from typing import Union
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware


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


async def getProxies(attr: int):
    url = "https://api.stentvessel.top/sub?target=clash&new_name=true&emoji=true&clash.doh=true&filename=YToo_SS&udp=true&config=https%3A%2F%2Fsubweb.s3.fr-par.scw.cloud%2FRemoteConfig%2Fcustomized%2Fytoo.ini&url=https%3A%2F%2Fapi.ytoo.xyz%2Fosubscribe.php%3Fsid%3D37854%26token%3Di9S5KxiwJZgx%26sip002%3D1"
    res = await httpGet(url)
    data = yaml.safe_load(res)

    rstr = ['日用.*香港', '日用.*美国', '日用.*日本', '标准.*香港', '标准.*美国',
            '标准.*日本', '标准.*台湾', '标准.*日本', '标准.*韩国', '阿根廷'][attr]
    res = list()
    for v in data['proxies']:
        if re.search(rstr, v['name']) != None:
            v["skip-cert-verify"] = True
            res.append(v)

    yamls = yaml.dump({"proxies": res}, allow_unicode=True)
    return yamls


async def getRules(attr: int, qx=False):
    fn = ['globalDirect', 'pselect', 'ms', 'apple', 'openai',
          'game', 'globalmedia', 'cnmeida', 'cqu'][attr]
    rule = file_get(f"./rule/{fn}.list")
    if qx:
        rule = rule.replace("IP-CIDR6,","IP6-CIDR,")
        rule = rule.replace("DOMAIN,","HOST,")
        rule = rule.replace("DOMAIN-SUFFIX,","HOST-SUFFIX,")
        rule = rule.replace("DOMAIN-KEYWORD,","HOST-KEYWORD,")
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


@app.get("/qrule")
async def read_root(attr: int):
    return PlainTextResponse(content=await getRules(attr, True))
