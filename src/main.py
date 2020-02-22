import asyncio
from src.agents.FileParsers.VSProjectFileParser import VSProjectFileParser
from src.agents.NugetFeedParser.ProgetFeedParser import ProgetFeedParser


async def __main():
    feed_agent = ProgetFeedParser("http://proget.aeroclub.int/nuget/AeroclubRelease/Packages?$format=json&$orderby=Id,Version")
    digraph = await feed_agent.build_digraph()

    # await for nuget packages graph
    file_parser = VSProjectFileParser("C:\\Repo")
    #digraph_file = await file_parser.build_digraph()

    #digraph.update(digraph_file)

    return digraph


if __name__ == "__main__":
    result = asyncio.run(__main())
    print(result)
