# ======================================================================================
#  Header
# ======================================================================================

import os
import sys
import typer
import importlib
from pathlib import Path
from tabulate import tabulate
from .iotproj_lib import Project

cpm_cmake_text = """
# ==============================================================================
#  CPM Configuration (readonly)
# ==============================================================================

set(CPM_DOWNLOAD_VERSION 0.35.0)

if(CPM_SOURCE_CACHE)
  # Expand relative path. This is important if the provided path contains a tilde (~)
  get_filename_component(CPM_SOURCE_CACHE ${CPM_SOURCE_CACHE} ABSOLUTE)
  set(CPM_DOWNLOAD_LOCATION "${CPM_SOURCE_CACHE}/cpm/CPM_${CPM_DOWNLOAD_VERSION}.cmake")
elseif(DEFINED ENV{CPM_SOURCE_CACHE})
  set(CPM_DOWNLOAD_LOCATION "$ENV{CPM_SOURCE_CACHE}/cpm/CPM_${CPM_DOWNLOAD_VERSION}.cmake")
else()
  set(CPM_DOWNLOAD_LOCATION "${CMAKE_BINARY_DIR}/cmake/CPM_${CPM_DOWNLOAD_VERSION}.cmake")
endif()

if(NOT (EXISTS ${CPM_DOWNLOAD_LOCATION}))
  message(STATUS "Downloading CPM.cmake to ${CPM_DOWNLOAD_LOCATION}")
  file(DOWNLOAD
    https://github.com/cpm-cmake/CPM.cmake/releases/download/v${CPM_DOWNLOAD_VERSION}/CPM.cmake ${CPM_DOWNLOAD_LOCATION}
    )
endif()

include(${CPM_DOWNLOAD_LOCATION})
"""

main_text = """
#include <stdio.h>

int main() {
    return 0;
}
"""

cmake_text = """
cmake_minimum_required(VERSION 3.1)
project(teste C ASM)

include(cmake/cpm.cmake)

add_executable(firmware
    objs/main.c
    )
"""




app = typer.Typer()


# ======================================================================================
#  Autocomplete Functions
# ======================================================================================

# For the autocomplete functions
def filterOptions(incomplete: str, optionlist: [str]):
    retval = []
    for name in optionlist:
        if name.startswith(incomplete):
            retval.append(name)
    return retval

def listAllClassesToInstall(incomplete: str):
    options = []
    scripts_url = Path.home()/'iotworld/scripts'
    for node in scripts_url.iterdir():
        if node.is_file():
            options.append(node.stem)
    return filterOptions(incomplete, options)

def listAllClassesFromProj(incomplete: str):
    proj = Project.openFromPwd()
    options = []
    scripts_url = proj.home / "src"
    for node in scripts_url.iterdir():
        if node.is_dir():
            options.append(node.name)
    return filterOptions(incomplete, options)



# ======================================================================================
#  Public Commands
# ======================================================================================

@app.command()
def start():
    home = str( Path.home() / "iotworld" )
    os.system("git clone https://github.com/bombark/iotworld "+home)

@app.command()
def new(name: str):
    proj_dir = Path(name)
    proj = Project(proj_dir)
    proj.new()

@app.command()
def install(
        module_name: str = typer.Argument(
            "",
            help="libraries in Iot World",
            autocompletion=listAllClassesToInstall
        )
    ):
    proj = Project.openFromPwd()
    os.chdir(str(proj.home))
    proj.src.install(module_name)

@app.command()
def mkobj(
    klass_name: str = typer.Argument("", help="libraries in Iot World",
        autocompletion=listAllClassesFromProj),
    obj_name: str = typer.Argument("", help="name of object") ):

    proj = Project.openFromPwd()
    os.chdir(proj.home)
    proj.src[klass_name].mkobj(obj_name)




@app.command()
def lsclass():
    proj = Project.openFromPwd()
    for module in proj.src.list():
        print(module.name)

@app.command()
def lsobj():
    proj = Project.openFromPwd()
    table = []
    for obj in proj.src.listObjects():
        table += [[obj.module.name, obj.name]]
    print(tabulate(table))

@app.command()
def update(name: str):
    print("Hello")

@app.command()
def make():
    proj = Project.openFromPwd()
    proj.make()

# ======================================================================================
#  Main
# ======================================================================================

if __name__ == "__main__":
    app()
