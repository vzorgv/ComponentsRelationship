import aiohttp

from src.agents import Agent


class ProgetFeedParser(Agent):

    def __init__(self, url):
        self.__url = url

    async def build_digraph(self) -> dict:
        await self.__send_request()
        return dict()

    async def __send_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__url) as response:
                json_body = await response.json()
                print(json_body)