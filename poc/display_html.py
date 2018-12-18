"""
Display the IOMMU current mapping on a very visual HTML file.
"""
import os
import platform
import subprocess
import shutil

from hole_calculator import calc_all_holes, get_all_mappings
from db import create_session


def generate_html_frieze(type, value):
    """
    Gets the data to be able to generate the frieze.
    Calls the function to actually generate HTML.

    Input :
        - Type (session or dataset) of the second input
        - A SQLAlchemy DB session or a dataset (list of mappings)
    """
    if type == "session":
        session = value
        mappings = get_all_mappings(session)
    elif type == "dataset":
        mappings = value

    holes = calc_all_holes("dataset", mappings)
    memory_state = sorted(mappings + holes, key=lambda mapping: mapping.phys_addr)
    html_frieze = create_html_from_memory_state(memory_state)
    return html_frieze


def create_html_from_memory_state(memory_state):
    """
    Generates the "frieze" for the html output
    The frieze is an html table

    Input:
        - memory_state : the list of memory states : holes and device mappings
    """
    return "<tr>mdr</tr>"


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
        mappings = get_all_mappings(session)
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
	