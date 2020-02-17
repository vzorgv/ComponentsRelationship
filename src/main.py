import asyncio
import os
from src import constants

from xml.etree.ElementTree import parse


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

    return "Not a package" if not package else package


async def parse_agent(file_name: str):
    tree = parse(file_name)
    root = tree.getroot()

    root_package_name = get_package_name(root, file_name)

    items = [reference
             for items in root if items.tag == constants.ITEMGROUP_TAG_NAME
             for reference in items if reference.tag == constants.PACKAGEREFERENCE_TAG_NAME]

    #print(f"{root_package_name} - {file_name}")

    for elem in items:
        package_name_used = elem.attrib.get(constants.REFERENCE_INCLUDE_ATTRIBUTE_NAME)
        #print(package_name_used)

    return root_package_name


def get_files(root_dir: str):
    proj_files = [os.path.join(d, x)
                  for d, dirs, files in os.walk(root_dir)
                  for x in files if x.endswith(constants.PROJ_FILE_EXT)]
    return proj_files


async def main(root_dir: str):
    tasks = []
    files = get_files(root_dir)
    '''
    for file in files:
        task = asyncio.create_task(parse_agent(file))
        tasks.append(task)
    
    await asyncio.gather(*tasks, )
    '''

    for file in files:
        value = await parse_agent(file)
        print(value)
        #task = asyncio.create_task(parse_agent(file))
        #tasks.append(task)


if __name__ == "__main__":
    asyncio.run(main("C:\\NetProjects"))
