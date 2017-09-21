import requests
import asyncio
import xml.etree.ElementTree as ET
import re
import os

def get_save_dir_path(dir_name=""):
    APP_ROOT = os.path.dirname(os.path.abspath( __file__ ))
    save_dir_path = APP_ROOT+ dir_name
    if not os.path.exists(save_dir_path):
        os.makedirs(save_dir_path)
    return save_dir_path

async def download_first_file(url):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    response.encode = 'utf-8'
    save_dir_path = get_save_dir_path("/data")
    file_path = save_dir_path + "/" + "data.xml"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    return response

async def download_file(url, dir_name, file_name, redownload=False):
    save_dir_path = get_save_dir_path(dir_name)
    if not os.path.exists(save_dir_path):
        os.makedirs(save_dir_path)
    file_path = save_dir_path + "/" + file_name
    if ((not os.path.exists(file_path)) or redownload):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.get, url)
        response.encode = 'utf-8'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

async def download_files(report, redownload=False):
    dir_name = "/data/" + report["title"]

    for url in report["link"]:
        file_name = url.split("/")[-1]
        await download_file(url, dir_name, file_name, redownload)

def extract_report_link(file_name):
    ET.register_namespace('', 'http://www.w3.org/2005/Atom')
    xml_content = ET.parse(file_name)
    namespaces = {'ns':'http://www.w3.org/2005/Atom'}
    root = xml_content.getroot()
    iterator = root.iterfind('ns:entry', namespaces=namespaces)
    reports = []
    for entry in iterator:
        title = entry.findtext('ns:title', namespaces=namespaces)
        links = entry.findall('ns:link[@type="text/xml"]', namespaces=namespaces)
        report = {'link':list()}
        for link in links:
            if '/PublicDoc/' in link.attrib["href"]:
                report["link"].append(link.attrib["href"])
        if len(report["link"]) > 0:
            report["title"] = title
            reports.append(report)

    return reports

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    company_id = 6094
    url = 'http://resource.ufocatch.com/atom/edinetx/query/' + str(company_id)
    dir_name = "/data"
    file_name = "data.xml"
    loop.run_until_complete(download_file(url, dir_name, file_name, True))

    reports = extract_report_link('./data/data.xml')
    for report in reports:
        loop.run_until_complete(download_files(report))
    loop.close()
