from typing import List


class PackageDescriptor:
    @property
    def id(self) -> str:
        return ""

    @id.setter
    def id(self, value: str):
        pass

    @property
    def dependencies(self) -> List[str]:
        return []

    @dependencies.setter
    def dependencies(self, value: List[str]):
        pass
