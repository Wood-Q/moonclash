import aiohttp
import asyncio
import yaml
import re
import json
import base64
import re
import os
from typing import Union
from fastapi import FastAPI, Request, Response, status
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


async def httpGet(url, head={}, type=0):
    async with aiohttp.ClientSession(headers=head) as session:
        async with session.get(url) as resp:
            if resp.status == 200:  # Check if the response status is OK
                data = await resp.text()  # Parse JSON from the response
                if type == 1:
                    return {"data": data, "header": dict(resp.headers)}
                return data
            else:
                return None


async def getProxies(attr: int, forcerefrush=False):
    if not forcerefrush:
        return file_get(f"./ps/{attr}.yaml")
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


async def getWarp():
    return file_get(f"./ps/warp.yaml")


async def getRawProxies(attr: int, forcerefrush=False):
    if not forcerefrush:
        return file_get(f"./ps/my{attr}.yaml")
    url = "https://api.stentvessel.top/sub?target=clash&new_name=true&emoji=true&clash.doh=true&filename=YToo_SS&udp=true&config=https%3A%2F%2Fsubweb.s3.fr-par.scw.cloud%2FRemoteConfig%2Fcustomized%2Fytoo.ini&url=https%3A%2F%2Fapi.ytoo.xyz%2Fosubscribe.php%3Fsid%3D37854%26token%3Di9S5KxiwJZgx%26sip002%3D1"
    res = await httpGet(url)
    data = yaml.safe_load(res)
    rstr = ['.*', '香港', '美国', '台湾', '日本'][attr]

    res = list()
    for v in data['proxies']:
        if re.search(rstr, v['name']) != None:
            v["skip-cert-verify"] = True
            res.append(v)

    yamls = yaml.dump({"proxies": res}, allow_unicode=True)
    return yamls


async def getRules(attr: int, qx=False):
    fn = ['globalDirect', 'pselect', 'ms', 'apple', 'openai',
          'game', 'globalmedia', 'cnmedia', 'cqu', 'lan'][attr]
    if qx:
        rule = file_get(f"./qrule/{fn}.list")
    else:
        rule = file_get(f"./rule/{fn}.list")
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
async def read_root(attr: int, forcerefrush: bool = False):
    return PlainTextResponse(content=await getProxies(attr, forcerefrush))


@app.get("/warp")
async def read_warp():
    return PlainTextResponse(content=await getWarp())


@app.get("/rule")
async def read_root(attr: int):
    return PlainTextResponse(content=await getRules(attr))


@app.get("/rawps")
async def read_root(attr: int, forcerefrush: bool = False):
    return PlainTextResponse(content=await getRawProxies(attr))


@app.get("/qrule")
async def read_root(attr: int):
    return PlainTextResponse(content=await getRules(attr, True))


@app.head("/api/v1/client/subscribe")
async def read_root(token: str):
    url = f"https://board6.cquluna.top/api/v1/client/subscribe?token={token}"
    rawinfo = await httpGet(url, {"user-agent": "Stash/2.4.6 Clash/1.9.0"}, 1)
    rawhead = rawinfo['header']
    resp = Response()
    resp.headers['subscription-userinfo'] = rawhead['subscription-userinfo']
    resp.headers['Content-Disposition'] = rawhead['Content-Disposition']
    return resp


@app.get("/api/v1/client/subscribe")
async def read_root(token: str):
    url = f"https://board6.cquluna.top/api/v1/client/subscribe?token={token}"
    rawinfo = await httpGet(url, {"user-agent": "Stash/2.4.6 Clash/1.9.0"}, 1)
    rawhead = rawinfo['header']
    data: dict = yaml.safe_load(rawinfo['data'])
    if len(data['proxies']) == 0:
        return PlainTextResponse(content="")

    for v in data['proxies']:
        if v['name'] == "校外使用【直连】":
            v.pop('cipher')
            v.pop('password')
            v['type'] = 'socks5'

    groups = yaml.safe_load(file_get("./template/groups.template"))
    for group in groups['groups']:
        new_proxies = list()
        want_proxies = group['proxies']
        for id in range(0, len(want_proxies)):
            if want_proxies[id].find("regex") != -1:
                patt = want_proxies[id].replace('regex', '')
                for proxy in data['proxies']:
                    if re.search(patt, proxy['name']) != None:
                        new_proxies.append(proxy['name'])
            else:
                new_proxies.append(want_proxies[id])
        group['proxies'] = new_proxies

    rules = yaml.safe_load(file_get("./rule/clash.list"))
    data['proxy-groups'] = groups['groups']
    data['rules'] = rules['rules']
    data.pop('rule-providers')
    resp = yaml.safe_dump(data, allow_unicode=True)

    return PlainTextResponse(content=resp, headers={"subscription-userinfo": rawhead['subscription-userinfo'], "Content-Disposition": "attachment;filename*=UTF-8''%E5%BE%80%E6%9C%88%E9%97%A8"})


@app.head("/api/v2/client/subscribe")
async def read_root(token: str, custom: str):
    url = f"https://board6.cquluna.top/api/v1/client/subscribe?token={token}"
    rawinfo = await httpGet(url, {"user-agent": "Stash/2.4.6 Clash/1.9.0"}, 1)
    rawhead = rawinfo['header']
    resp = Response()
    resp.headers['subscription-userinfo'] = rawhead['subscription-userinfo']
    resp.headers['Content-Disposition'] = rawhead['Content-Disposition']
    return resp


@app.get("/api/v2/client/subscribe")
async def read_root(token: str, custom: str):
    # 获取自购机场的节点信息
    url = base64.b64decode(custom).decode("utf-8")
    rawinfo = await httpGet(url, {"user-agent": "Stash/2.4.6 Clash/1.9.0"}, 1)
    rawhead = rawinfo['header']
    data: dict = yaml.safe_load(rawinfo['data'])
    if len(data['proxies']) == 0:
        print("自购机场节点获取失败")
        return PlainTextResponse(content="")
    else:
        selfProxies = data['proxies']

    # 获取往月门节点信息
    url = f"https://board6.cquluna.top/api/v1/client/subscribe?token={token}"
    rawinfo = await httpGet(url, {"user-agent": "Stash/2.4.6 Clash/1.9.0"}, 1)
    rawhead = rawinfo['header']
    data: dict = yaml.safe_load(rawinfo['data'])
    if len(data['proxies']) == 0:
        # 获取往月门节点信息失败
        return PlainTextResponse(content="")

    for v in data['proxies']:
        if v['name'] == "校外使用【直连】":
            v.pop('cipher')
            v.pop('password')
            v['type'] = 'socks5'

    groups = yaml.safe_load(file_get("./template/custom.template"))
    for group in groups['groups']:
        new_proxies = list()
        want_proxies = group['proxies']
        for id in range(0, len(want_proxies)):
            if want_proxies[id].find("regex") != -1:
                patt = want_proxies[id].replace('regex', '')
                for proxy in data['proxies']:
                    if re.search(patt, proxy['name']) != None:
                        new_proxies.append(proxy['name'])
            elif want_proxies[id].find("custom") != -1:
                patt = want_proxies[id].replace('custom', '')
                for proxy in selfProxies:
                    if re.search(patt, proxy['name']) != None:
                        new_proxies.append(proxy['name'])
            else:
                new_proxies.append(want_proxies[id])
        group['proxies'] = new_proxies

    # 将所有的自购机场节点加入到节点列表中
    for v in selfProxies:
        v["skip-cert-verify"] = True
        data['proxies'].append(v)

    rules = yaml.safe_load(file_get("./rule/clash.list"))
    data['proxy-groups'] = groups['groups']
    data['rules'] = rules['rules']
    data.pop('rule-providers')
    resp = yaml.safe_dump(data, allow_unicode=True)

    return PlainTextResponse(content=resp, headers={"subscription-userinfo": rawhead['subscription-userinfo'], "Content-Disposition": "attachment;filename*=UTF-8''%E5%BE%80%E6%9C%88%E9%97%A8"})
