import asyncio
from src.agents.FileParsers.VSProjectFileParser import VSProjectFileParser
from src.agents.NugetFeedParser.ProgetFeedParser import ProgetFeedParser


async def __main():
    tasks = []

    file_parser = VSProjectFileParser("C:\\Repo")
    task = asyncio.create_task(file_parser.build_digraph())
    tasks.append(task)

    feed_agent = ProgetFeedParser("http://proget.aeroclub.int/nuget/AeroclubRelease/Packages?$format=json")
    task = asyncio.create_task(feed_agent.build_digraph())
    tasks.append(task)

    await asyncio.gather(*tasks, )


if __name__ == "__main__":
    asyncio.run(__main())
