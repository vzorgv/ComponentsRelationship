import asyncio
import os

from graphviz import Digraph
from src import constants
from xml.etree.ElementTree import parse
from pathlib import Path

__package_graph = dict()


def get_package_name(root, file_name: str):
    package = ""

    package_list = [package.text
                    for group in root if group.tag == constants.PROPERTYGROUP_TAG_NAME
                    for package in group if package.tag == constants.PACKAGEID_TAG_NAME]

    if not package_list:
        package_list = [assembly.text
                        for group in root if group.tag == constants.PROPERTYGROUP_TAG_NAME
                        for assembly in group if assembly.tag == constants.ASSEMBLY_GROUP_TAG_NAME]
    else:
        package = package_list[0]

    if not package_list:
        file_parts = os.path.split(file_name)
        package = file_parts[1].replace(constants.PROJ_FILE_EXT, '')
    else:
        package = package_list[0]

    return "UNKNOWN" if not package else package


async def parse_agent(file_name: str, dict_handle):
    tree = parse(file_name)
    root = tree.getroot()

    root_package_name = get_package_name(root, file_name)

    items = [reference
             for items in root if items.tag == constants.ITEMGROUP_TAG_NAME
             for reference in items if reference.tag == constants.PACKAGEREFERENCE_TAG_NAME]

    packages_used = []
    for elem in items:
        package_name_used = elem.attrib.get(constants.REFERENCE_INCLUDE_ATTRIBUTE_NAME)
        packages_used.append(package_name_used)

    dict_handle(root_package_name, packages_used)


def get_files(root_dir: str):
    proj_files = [os.path.join(d, x)
                  for d, dirs, files in os.walk(root_dir)
                  for x in files if x.endswith(constants.PROJ_FILE_EXT)]
    return proj_files


def append_package(package_name: str, packages_used: list):
    list_exist = []

    if package_name in __package_graph:
        list_exist = __package_graph.get(package_name)

    list_exist.extend(packages_used)
    __package_graph[package_name] = list_exist


def build_graph() -> object:
    graph = Digraph('Components', node_attr={'color': 'lightblue2', 'style': 'filled'})

    for vertex in __package_graph:
        used_list = __package_graph[vertex]
        for used in used_list:
            if used is not None:
                graph.edge(vertex, used)
    home_dir = Path.home()
    graph.save(filename='components.graph', directory=home_dir)
    print(f"File saved in {home_dir}")


async def main(root_dir: str):
    tasks = []
    files = get_files(root_dir)

    for file in files:
        task = asyncio.create_task(parse_agent(file, append_package))
        tasks.append(task)

    await asyncio.gather(*tasks, )
    build_graph()


if __name__ == "__main__":
    asyncio.run(main("C:\\Repo"))
