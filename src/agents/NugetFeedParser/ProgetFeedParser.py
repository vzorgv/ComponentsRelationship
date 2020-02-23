import aiohttp

from src.agents import Agent


class ProgetFeedParser(Agent):

    def __init__(self, url):
        self.__url = url

    async def build_digraph(self) -> dict:
        json = await self.__send_request()

        return await self.__parse_json(json)

    async def __parse_json(self, json):
        result = dict()
        raw_list = json.get("d")

        if raw_list is not None:
            raw_list = raw_list.get("results")
            if raw_list:
                for item in raw_list:
                    package_id = item.get("Id")
                    dependencies = item.get("Dependencies")
                    dep_list = self.__parse_dependencies(dependencies)
                    result[package_id] = dep_list
        return result

    def __parse_dependencies(self, dependencies: str):
        if dependencies == "":
            return []

        dep_names = set()
        dep_by_platform = dependencies.split('|')
        for dep in dep_by_platform:
            idx = dep.find(':')
            if dep[:idx] != "":
                dep_names.add(dep[:idx])

        return list(dep_names)

    async def __send_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__url) as response:
                if response.status == 200:
                    json_body = await response.json()
                else:
                    json_body = ""

        return json_body
