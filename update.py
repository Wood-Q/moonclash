import os
import aiohttp
import asyncio
import yaml


async def httpGet(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:  # Check if the response status is OK
                data = await resp.read()  # Parse JSON from the response
                return data
            else:
                return None


async def httpPost(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            if resp.status == 200:  # Check if the response status is OK
                data = await resp.json()  # Parse JSON from the response
                return data
            else:
                return None


async def update():
    rdata = await httpGet("https://fastly.jsdelivr.net/gh/Dreamacro/maxmind-geoip@release/Country.mmdb")
    directory = "./"
    subdirectories = [d for d in os.listdir(
        directory) if os.path.isdir(os.path.join(directory, d))]
    for sd in subdirectories:
        if sd == 'ui':
            continue
        fs = open(f"./{sd}/Country.mmdb", "wb")
        fs.write(rdata)
        fs.close()
        print(f"{sd} GEOIP更新完成")


async def select_worker_ip():
    rdata = await httpPost("https://api.hostmonit.com/get_optimization_ip", {"key": "iDetkOys"})
    if rdata != None:
        ip = ''
        for v in rdata['info']:
            if v['line'] == 'CT':
                ip = v['ip']
                break
        print(f"更新选择的IP为{ip}")
        raw = yaml.safe_load(open('./worker/config.yaml','r').read())
        if ip != "":
            raw['proxies'][0]['server'] = ip
            yaml.safe_dump(raw,open('./worker/config.yaml','w'))


async def main():
    await update()
    await select_worker_ip()


asyncio.run(main())
