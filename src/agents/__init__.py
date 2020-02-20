from abc import abstractmethod


class Agent:
    """The base abstract class for agents."""

    @abstractmethod
    async def build_digraph(self) -> dict:
        """
        Gets the directed graph.
        return: The dictionary where key is a source vertex, and value is a list of destination vertices.
        """
        pass
