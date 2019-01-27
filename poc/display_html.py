"""
Display the IOMMU current mapping on a very visual HTML file.
"""
import os
import platform
import subprocess
import shutil

from db_schema import Device
from hole_calculator import calc_all_holes, get_all_mappings
from db import create_session


def generate_html_frieze(type, value):
    """
    Gets the data to be able to generate the frieze.
    Calls the function to actually generate HTML.

    Input:
        - Type (session or dataset) of the second input
        - A SQLAlchemy DB session or a dataset (list of mappings)
    Output:
        - The HTML to be displayed
    """
    if type == "session":
        session = value
        mappings = list(get_all_mappings(session))
    elif type == "dataset":
        mappings = value

    holes_raw = calc_all_holes("dataset", mappings)
    holes = []
    for hole in holes_raw:
        holes.append(
            {
                'devices_id': -1000,
                'id': -1000,
                'iova': None,
                'phys_addr': hole[0],
                'size': hole[1]
            }
        )

    for hole in holes:
        hole['devices_id'] = -1
    
    try:
        mappings = add_device_info(mappings, session)
    except:
        session = create_session()
        mappings = add_device_info(mappings, session)

    mappings_as_dict = []
    for m in mappings:
        mappings_as_dict.append(m.__dict__)
    memory_state = sorted(mappings_as_dict + holes, key=lambda mapping: mapping['phys_addr'])
    memory_state = unify_common_space(memory_state)
    html_frieze = create_html_from_memory_state(memory_state)
    return html_frieze


def unify_common_space(memory_state):
    """
    Merges the common space for various devices.
    Each one may not have the same size in the shared space whereas they seem to all have access to the whole space.
    Input:
        - memory_state : the state in which the memory is with all its fragments.
    Output:
        The memory with common space merged.
    """
    new_memory_state = [memory_state[0]]
    for i in range(1, len(memory_state)):
        if memory_state[i]['devices_id'] == 0 and new_memory_state[-1]['devices_id'] == 0:
            new_memory_state[-1]['size'] += memory_state[i]['size']
        else:
            new_memory_state.append(memory_state[i])
    return new_memory_state


def add_device_info(mappings, session):
    """
    Adds the informations about the device for each mapping.
        - If the mapping is related to a device, gives the device id.
        - If it is common space, takes the id 0
        - ! Not used here ! If it is part of a "memory hole", id is -1
    
    Input :
        - mappings : the list of mappings you want to sort
        - session : the database session
    """
    for mapping in mappings:
        mapping_device = (
            session.query(Device)
            .filter(Device.mapping == mapping)
            .one_or_none()
        )
        if mapping_device != None:
            # Devices map exactly one segment for them specifically
            mapping.devices_id = Device.id
        else:
            # If the mapping is in the mapping table and not related to a Device,
            # it's part of the common space to be used
            mapping.devices_id = 0
    return mappings


def create_html_from_memory_state(memory_state):
    """
    Generates the "frieze" for the html output
    The frieze is an html table

    Input:
        - memory_state : the list of memory states : holes and device mappings
    """
    i = 0
    frieze_text = ""
    for memory_part in memory_state:
        hole = ' hole' if memory_part['devices_id'] == -1 else ''
        domain_shared = ' domain-shared' if memory_part['devices_id'] == 0 else ''
        if hole != ' hole' and domain_shared != ' domain-shared' :
            color_id = (i % 3) + 1
            dev_name = 'Temporary Name'
        elif hole != ' hole':
            dev_name = 'Domain shared space'
            color_id = ''
        elif domain_shared != ' domain-shared':
            dev_name = 'Hole'
            color_id = ''

        frieze_text += (
            "<td "
            + 'class="memory-range color'
            + str(color_id)
            + hole + domain_shared + '"'
            + 'data-device-id="'
            + str(memory_part['devices_id'])
            + '"'
            + "onmouseover=\"displayDeviceInformation('"
            + str(memory_part['devices_id'])
            + "', '" + dev_name + "', '"
            + str(memory_part['iova'])
            + "','"
            + str(memory_part['phys_addr'])
            + "->"
            #+ str(hex(int(memory_part['phys_addr'], 16) + memory_part['size']))
            + "')\", onmouseout=\"revertToNormalOpacityAndText();\""
            +  ">" + "</td>"
        )
        i += 1

    return frieze_text


def write_html_file(type=None, value=None):
    """
    Creates a new html file with the content of the IOMMU mapping on a visual way.
    The output is located in ./out/

    Input :
        - Type (session or dataset) of the second input
        - A SQLAlchemy DB session or a dataset (list of mappings)
    """

    filenames = ["./html/top_template.html", "./html/bottom_template.html"]

    with open(filenames[0], "r") as file:
        top_content = file.read()

    if type == "session":
        core_content = generate_html_frieze("session", value)
    elif type == "dataset":
        core_content = generate_html_frieze("dataset", value)
    else:
        session = create_session()
        mappings = list(get_all_mappings(session))
        core_content = generate_html_frieze("dataset", mappings)

    with open(filenames[1], "r") as file:
        bottom_content = file.read()

    if not os.path.exists("./out/"):
        try:
            os.mkdir("./out/", 0o755)
        except OSError:
            print("Something happened at file generation, check your permissions")

    with open("./out/iommu_config_display.html", "w+") as file:
        file.write(top_content + core_content + bottom_content)

    # copy style files into output
    shutil.copy2("./html/style.css", "./out/")
    shutil.copy2("./html/normalize.css", "./out/")

    open_file("./out/iommu_config_display.html")


def open_file(path):
    """
    Open a file in its standard application for Unix Based systems.
    Will do nothing on Windows.
    Input :
        - path : The path of the file you want to open.
    """
    if platform.system() == "Windows":
        pass
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


# ----------------------------------------------------------------------------

if __name__ == "__main__":
    write_html_file()
