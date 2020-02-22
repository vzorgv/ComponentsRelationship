import aiohttp
import json

from src.agents import Agent
from src.agents.NugetFeedParser.PackageDescriptor import PackageDescriptor


class ProgetFeedParser(Agent):

    def __init__(self, url):
        self.__url = url

    async def build_digraph(self) -> dict:
        json = await self.__send_request()

        return await self.__parse_json(json)

    async def __parse_json(self, json):
        raw_list = json["d"]["results"]
        result = dict()
        for item in raw_list:
            package_id = item["Id"]
            result[package_id] = [item["Dependencies"]]
            x = PackageDescriptor(package_id, item["Dependencies"])
        return result

    async def __send_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__url) as response:
                if response.status == 200:
                    json_body = await response.json()
                else:
                    json_body = ""

        return json_body
