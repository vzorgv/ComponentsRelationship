import asyncio
from src.agents.FileParsers.VSProjectFileParser import VSProjectFileParser


if __name__ == "__main__":
    file_parser = VSProjectFileParser("C:\\Repo")
    digraph = asyncio.run(file_parser.build_digraph())
    print(digraph)
