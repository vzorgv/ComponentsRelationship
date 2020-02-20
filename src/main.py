import asyncio
from src.agents.file_parsers import VSProjectFileParser


if __name__ == "__main__":
    file_parser = VSProjectFileParser.VSProjectFileParser("C:\\Repo")
    digraph = asyncio.run(file_parser.build_digraph())
    print(digraph)
