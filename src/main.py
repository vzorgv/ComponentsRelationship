import asyncio
from src.agents.FileParsers.VSProjectFileParser import VSProjectFileParser
from src.agents.NugetFeedParser.ProgetFeedParser import ProgetFeedParser


async def __main():
    repository_agent = VSProjectFileParser("C:\\Repo")
    digraph_result = await repository_agent.build_digraph()

    # awaiting for repository result as a baseline for packages
    # information from feeds considered as actual and will rewrite data from repository
    feed_agent = ProgetFeedParser(
        "http://proget.aeroclub.int/nuget/AeroclubRelease/Packages?$format=json&$orderby=Id,Version")
    digraph_feed = await feed_agent.build_digraph()

    digraph_result.update(digraph_feed)

    return digraph_result


if __name__ == "__main__":
    result = asyncio.run(__main())
    print(result)
