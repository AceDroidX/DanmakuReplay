import json
import asyncio
import aiohttp
import time

# init
with open('config.json', encoding='utf-8') as f:
    config = json.loads(f.read())
with open('cookie.txt', encoding='utf-8') as f:
    cookie_txt = f.read()
with open(config['danmu_file_name'], encoding='utf-8') as f:
    rawjson = json.loads(f.read())
headers = {"content-type": "application/x-www-form-urlencoded",
           "referrer": "https://live.bilibili.com/",
           'cookie': cookie_txt}
template_body = 'bubble=0&msg={msg}&color={color}&mode=1&fontsize=25&rnd={ts}&roomid={roomid}&csrf={csrf}&csrf_token={csrf}'


def cookieStrToJson(source):
    cookies = {}
    for line in source.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    return cookies


danlist = rawjson['full_comments']
cookie_json = cookieStrToJson(cookie_txt)


async def send_danmu(roomid, msg):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post('https://api.live.bilibili.com/msg/send', data=template_body.format(msg=msg, color=config['danmu_color'], ts=int(time.time()), roomid=roomid, csrf=cookie_json['bili_jct'])) as resp:
            if resp.status != 200:
                print(resp.status)
                print(await resp.text())


# def custom_exception_handler(loop, context):
#     # first, handle with default handler
#     print(context)
#     loop.default_exception_handler(context)
#     loop.stop()


async def send_list(roomid, start_time=0):
    if start_time == 0:
        start_time = danlist[0]['time']
    first_time = danlist[0]['time']
    sleep_time = 0
    first_ts = time.time()*1000
    next_ts = first_ts
    for dan in danlist:
        if not 'text' in dan:
            continue
        if dan['time'] < start_time:
            continue
        next_ts = first_ts + (dan['time'] - start_time)
        sleep_time = next_ts - time.time()*1000
        if sleep_time < 0:
            print(
                f"pass({sleep_time}):{(dan['time']-first_time)/1000}:{dan['text']}")
            continue
        elif 0 < sleep_time < config['danmu_interval']:
            print(f"sleep:{config['danmu_interval']}({sleep_time})")
            await asyncio.sleep(config['danmu_interval']/1000)
        else:
            print(f'sleep:{sleep_time}')
            await asyncio.sleep(sleep_time/1000)
        print(f"{(dan['time']-first_time)/1000}:{dan['text']}")
        await send_danmu(roomid=roomid, msg=dan['text'])


async def main():
    await send_list(config['roomid'], config['danmu_start_time'])
    # await send_list(config['roomid'], 0)


if __name__ == '__main__':
    # print(cookie_json)
    # loop = asyncio.get_event_loop()
    # loop.set_exception_handler(custom_exception_handler)
    # loop.run_until_complete(main())
    asyncio.run(main())
