import aiohttp
import json

from src.agents import Agent


class ProgetFeedParser(Agent):

    def __init__(self, url):
        self.__url = url

    async def build_digraph(self) -> dict:
        json = await self.__send_request()

        return await self.__parse_json(json)

    async def __parse_json(self, json):
        return dict()

    async def __send_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__url) as response:
                json_body = await response.json()

        return json_body
