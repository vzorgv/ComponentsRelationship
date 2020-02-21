import asyncio
from src.agents.FileParsers.VSProjectFileParser import VSProjectFileParser
from src.agents.NugetFeedParser.ProgetFeedParser import ProgetFeedParser


async def __main():
    tasks = []


    feed_agent = ProgetFeedParser("http://proget.aeroclub.int/nuget/AeroclubRelease/Packages?$format=json")
    task = asyncio.create_task(feed_agent.build_digraph())
    tasks.append(task)

    file_parser = VSProjectFileParser("C:\\Repo")
    task = asyncio.create_task(file_parser.build_digraph())
    tasks.append(task)

    await asyncio.gather(*tasks, )

    digraph = tasks[0].result()
    digraph.update(tasks[1].result())

    return digraph


if __name__ == "__main__":
    result = asyncio.run(__main())
    print(result)
