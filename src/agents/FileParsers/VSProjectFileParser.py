import asyncio
import os

from typing import Dict
from src.agents import Agent
from src.agents.FileParsers import VSProjectConstants
from xml.etree.ElementTree import parse


class VSProjectFileParser(Agent):
    __digraph: Dict[str, list]

    def __init__(self, root_directory: str):
        self.__digraph = dict()
        self.__root_directory = root_directory

    async def build_digraph(self) -> dict:
        tasks = []
        files = self.__get_file_names(self.__root_directory)

        for file_name in files:
            task = asyncio.create_task(self.__parse_file(file_name, self.__append_package))
            tasks.append(task)

        await asyncio.gather(*tasks, )

        return self.__digraph

    def __get_file_names(self, root_dir):
        return [os.path.join(d, x)
                for d, dirs, files in os.walk(root_dir)
                for x in files if x.endswith(VSProjectConstants.PROJ_FILE_EXT)]

    async def __parse_file(self, file_name: str, dict_handle):
        tree = parse(file_name)
        root = tree.getroot()

        root_package_name = self.__get_package_name(root, file_name)

        items = [reference
                 for items in root if items.tag == self.__get_tag_name(root, VSProjectConstants.ITEMGROUP_TAG_NAME)
                 for reference in items
                 if reference.tag == self.__get_tag_name(root, VSProjectConstants.PACKAGEREFERENCE_TAG_NAME)
                 or reference.tag == self.__get_tag_name(root, VSProjectConstants.REFERENCE_TAG_NAME)]

        packages_used = []
        for elem in items:
            package_name_used = elem.attrib.get(VSProjectConstants.REFERENCE_INCLUDE_ATTRIBUTE_NAME)
            packages_used.append(package_name_used)

        dict_handle(root_package_name, packages_used)

    def __get_tag_name(self, root, tag_name):
        result = tag_name
        if VSProjectConstants.DEFAULT_NAMESPACE_OLDVERSION in root.tag:
            result = VSProjectConstants.DEFAULT_NAMESPACE_OLDVERSION + tag_name

        return result

    def __get_package_name(self, root, file_name: str):

        package_list = [package.text
                        for group in root
                        if group.tag == self.__get_tag_name(root, VSProjectConstants.PROPERTYGROUP_TAG_NAME)
                        for package in group
                        if package.tag == self.__get_tag_name(root, VSProjectConstants.PACKAGEID_TAG_NAME)]

        if not package_list:
            package_list = [assembly.text
                            for group in root if
                            group.tag == self.__get_tag_name(root, VSProjectConstants.PROPERTYGROUP_TAG_NAME)
                            for assembly in group if
                            assembly.tag == self.__get_tag_name(root, VSProjectConstants.ASSEMBLY_GROUP_TAG_NAME)]
        else:
            pass

        if not package_list:
            file_parts = os.path.split(file_name)
            package = file_parts[1].replace(VSProjectConstants.PROJ_FILE_EXT, '')
        else:
            package = package_list[0]

        return "UNKNOWN" if not package else package

    def __append_package(self, package_name: str, packages_used: list):
        list_exist = []

        if package_name in self.__digraph:
            list_exist = self.__digraph.get(package_name)

        list_exist.extend(packages_used)
        self.__digraph[package_name] = list_exist
