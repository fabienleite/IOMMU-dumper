"""
Display the IOMMU current mapping on a very visual HTML file.
"""
import os
import platform
import subprocess
import shutil


def generate_html_frieze():
    """
    Generates the "frieze" for the html output
    The frieze is an html table
    """
    return ""


def write_html_file():
    """
    Creates a new html file with the content of the IOMMU mapping on a visual way.
    The output is located in ./out/
    """

    filenames = ["./html/top_template.html", "./html/bottom_template.html"]

    with open(filenames[0], "r") as file:
        top_content = file.read()

    core_content = generate_html_frieze()

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
