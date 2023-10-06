import aiohttp
import asyncio
import yaml
import re
import json


def file_get(path):
    fs = open(path,"r")
    res = fs.read()
    fs.close()
    return res

def text_mid(text: str, start_text: str, end_text: str):
    start_index = text.find(start_text)
    end_index = text.find(end_text)
    if start_index != -1 and end_index != -1:
        extracted_text = text[start_index + len(start_text):end_index]
        return extracted_text
    return ""


async def httpGet(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:  # Check if the response status is OK
                data = await resp.text()  # Parse JSON from the response
                return data
            else:
                return None


def makeMap(data: str) -> dict:
    res = dict()
    matches = re.finditer(r'\[(.*?)\]\((http.*?)\)', data)
    for match in matches:

        # https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Clash/AnTianKeJi
        url = match.group(2).replace("https://github.com/blackmatrix7/ios_rule_script/tree/master/",
                                     "")
        name = url[url.rfind("/"):]
        url = f"./store/{url}{name}.list"
        res[match.group(1)] = url
    return res


async def main():
    data = file_get("./store/rule/Clash/README.md")

    gb = text_mid(data, "|🌏Global|", "|🌏GlobalMedia| ")
    fs = open("./maps/global.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data, "|🌏GlobalMedia|", "|🇨🇳Mainland|")
    fs = open("./maps/globalmedia.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data, "|🇨🇳Mainland|","|🇨🇳MainlandMedia|")
    fs = open("./maps/mainland.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data,"|🇨🇳MainlandMedia|","|📺Media|")
    fs = open("./maps/mainlandmedia.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data,"|📺Media|","|🎮Game|")
    fs = open("./maps/media.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data,"|🎮Game|","|🍎Apple|")
    fs = open("./maps/game.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data,"|🍎Apple|","|🗄️Microsoft|")
    fs = open("./maps/apple.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data,"|🗄️Microsoft|","|📟Google|")
    fs = open("./maps/Microsoft.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data,"|📟Google|","|🚫Reject|")
    fs = open("./maps/Google.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close

    gb = text_mid(data+"*speical_flag*","|🖥️Other|","*speical_flag*")
    fs = open("./maps/other.map", "w")
    fs.write(json.dumps(makeMap(gb), ensure_ascii=False))
    fs.close


asyncio.run(main())
