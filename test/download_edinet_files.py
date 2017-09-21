import requests
import asyncio
import xml.etree.ElementTree as ET

async def getget(url):
    loop = asyncio.get_event_loop()
    print("get-1")
    response = requests.get(url)
    print("get-2")
    return response


def main():
    loop = asyncio.get_event_loop()
    print("main-1")
    response = loop.run_until_complete(getget('http://resource.ufocatch.com/atom/edinetx/query/6094'))
    print("main-2")
    return response

if __name__ == '__main__':
    response = main()

    with open('data2.xml', 'w') as f:
        f.write(response.text)
