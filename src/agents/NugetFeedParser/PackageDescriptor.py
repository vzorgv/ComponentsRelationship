from dataclasses import dataclass


@dataclass
class PackageDescriptor:
    id: str
    dependencies: list
