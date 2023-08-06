# ======================================================================================
#  Header
# ======================================================================================

import sh
import os
import sys
import glob
import shutil
import yaml
from pathlib import Path
from jinja2 import Template
import importlib
from colorama import Fore, Style
import hashlib

# ======================================================================================
#  Utils
# ======================================================================================

def printError(text, *args):
    print(Fore.RED + text + Fore.RESET, *args)
    exit(-1)

def printNew(text, *args):
    print(Fore.GREEN + "[NEW]: " + Fore.RESET + text, *args)

def printUpdate(text, *args):
    print(Fore.GREEN + "[UPDATE]: " + Fore.RESET + text, *args)

def printGenerate(text, *args):
    print(Fore.GREEN + "[GENERATE]: " + Fore.RESET + text, *args)

def printAlert(text, *args):
    print(Fore.YELLOW + text, *args, Fore.RESET)

def md5FromFile(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5FromText(text):
    hash_md5 = hashlib.md5()
    hash_md5.update(text.encode())
    return hash_md5.hexdigest()

def generateFileFromText(template_text, dst_url, params):
    # Read the template and generate the code
    template = Template(template_text)
    code = template.render( params )

    # Write the code in the destiny
    if dst_url.exists():
        md5_code = md5FromText(code)
        md5_orig = md5FromFile(str(dst_url))
        # print(md5_code, md5_orig)
        if md5_code != md5_orig:
            printAlert("File was modified"+str(dst_url))
    else:
        printGenerate("file "+str(dst_url))
        with open( dst_url, 'w') as fd:
            fd.write(code)
        # with open( str(dst_url)+".yml", 'w') as fd:
        #    fd.write( yaml.dump(params) )

def generateFile(src_url: str, dst_url: str, params):
    # Read the template
    with open(src_url) as fd:
        template = Template(fd.read())

    # Generate the code
    code = template.render( params )

    # Write the code in the destiny
    # if not Path(dst_url).exists():
    printGenerate("file "+dst_url)
    with open(dst_url, 'w') as fd:
        fd.write(code)
        # with open(dst_url+".yml", 'w') as fd:
        #    fd.write( yaml.dump(params) )
    # else:
    #    printAlert("File generated was modified")


# ======================================================================================
#  Branch
# ======================================================================================

class Branch:
    def __init__(self, home_path=""):
        self.root = None
        self.home = Path(home_path)

    def setHome(self, home_path=""):
        self.home = Path(home_path)

    def rootFromGit(self, url):
        module_id = url.replace("http://", "")
        module_id = module_id.replace("https://", "")
        module_id = module_id.replace("git@", "")
        module_id = module_id.replace("/", "-")
        root_cache = Path.home() / "iotworld/cache" / module_id

        if not root_cache.is_dir():
            # sh.git.clone(url, str(root_cache))
            print("Downloading the repository "+url)
            os.system("git clone '{}' '{}'".format(url, str(root_cache)))
        self.root = Branch(root_cache)
        return self

    def rootFromDir(self, dir_path):
        self.root = Branch(dir_path)
        return self

    def findFiles(self, pattern, recursive=False):
        previous_dir = os.getcwd()
        os.chdir(self.home)
        files = glob.glob(pattern, recursive=recursive)
        os.chdir(previous_dir)
        return files

    def copyTreeFromRoot(self, src, dst):
        if self.root == None:
            raise Exception("Root module not define, use the functions rootFromGit or rootFromDir")
        # Path(dst).mkdir(parents=True, exist_ok=True)
        # print(self.root.home/src, dst)
        shutil.copytree( self.root.home/src, self.home/dst, copy_function = shutil.copy )

    def copyFilesFromRoot(self, pattern, dest="./"):
        retval = []
        dst_path = self.home / dest
        dst_path.mkdir(parents=True, exist_ok=True)
        files_found = self.root.findFiles(pattern)

        # manifest_path = self.home / '.manifest.yml'
        # if not manifest_path.exists():
        #    fd = open( self.home / '.manifest.yml' )

        # copy filesdest_path
        for file_path_relative in files_found:
            # prepare the absolute path from source and destiny
            file_path = Path(file_path_relative)
            file_name = file_path.name
            file_src = self.root.home / file_path
            file_src_str = str(file_src)
            file_dst = dst_path / file_name
            file_dst_str = str(file_dst)

            if file_src.is_dir():
                printAlert("Node is a directory: '{}'".format(file_path))
                continue

            if not file_dst.exists():
                printNew("file "+str(file_dst_str))
                shutil.copy( file_src_str, file_dst_str )
            else:
                src_md5 = md5FromFile(file_src_str)
                dst_md5 = md5FromFile(file_dst_str)
                if dst_md5 != src_md5:
                    printAlert("file was modified "+str(file_dst_str))
                    # shutil.copy( file_src_str, file_dst_str )

        return retval


    def generateFileFromRoot(self, file_src: str, file_dst: str, params: {}):
        # Read the template
        src_url = self.root.home / file_src
        dst_url = self.home / file_dst
        generateFile(str(src_url), str(dst_url), params)


    def generateFile(self, template_text: str, file_dst: str, params):
        dst_url = self.home / file_dst
        generateFileFromText(template_text, dst_url, params)



# ======================================================================================
#  Project
# ======================================================================================

class Project:
    def __init__(self, home: Path):
        if type(home) == str:
            self.home = Path(home)
        else:
            self.home = home
        self.name = self.home.absolute().name
        self.src = Package(self.home / "src")

    def openFromPwd():
        cur = Path().absolute()
        for i in range(0,10):
            proj_py = cur / "proj.py"
            if proj_py.exists():
                break

            if str(cur) == '/':
                raise BaseException("root of project not found")
            cur = cur.parent
        return Project(cur)

    def new(self):
        proj_dir = self.home
        proj_dir.mkdir(parents=True, exist_ok=True)
        generateFileFromText(example_text, proj_dir/"proj.py", {})

    def install(self, module_name: str):
        self.src.install(module_name)

    def mkobj(self, klass_name: str, obj_name="", **args):
        self.src[klass_name].mkobj(obj_name, **args)

    def generateCMake(self, cmakelist_jj_path: str):
        objects = self.src.listObjects()
        cmakelist_jj = self.home/cmakelist_jj_path
        if cmakelist_jj.is_file():
            generateFile(str(cmakelist_jj), str(self.home/'CMakeLists.txt'), {'project': self})
        else:
            raise FileNotFoundError("cmakelists.jj.txt")

    def make(self):
        build_dir = self.home / 'build'
        if not build_dir.exists():
            build_dir.mkdir(parents=True, exist_ok=True)
            os.system("cd '{}'; cmake ..".format(build_dir))
        os.system("cd '{}'; make".format(build_dir))


# ======================================================================================
#  Package
# ======================================================================================

class Package:
    def __init__(self, home: Path):
        if type(home) == str:
            self.home = Path(home)
        else:
            self.home = home

    def install(self, module_name: str):
        print("Installing {}".format(module_name))
        sys.path.append( str(Path.home()/'iotworld/scripts') )
        klass_path = self.home / module_name

        if not klass_path.exists():
            #raise Exception("This class already exists")
            pass
        else:
            klass_path.mkdir(parents=True, exist_ok=True)

        # execute the script
        klass_script = importlib.import_module(module_name)
        klass_install_func = getattr(klass_script, "install")
        klass_install_func( str(klass_path) )

    def list(self):
        retval = []
        nodes = os.listdir(str(self.home))
        for node_name in nodes:
            module_path = self.home / node_name
            klass_path = module_path # / 'class'
            if klass_path.exists():
                retval.append(Module(module_path))
        return retval

    def listObjects(self):
        retval = []
        modules = self.list()
        for module in modules:
            retval += module.list()
        return retval

    def generateCMake(self):
        objects = self.listObjects()
        cmakelist_jj = self.home/'cmakelists.jj.txt'
        if cmakelist_jj.is_file():
            generateFile(str(cmakelist_jj), str(self.home/'CMakeLists.txt'), {'objects': objects})
        else:
            raise FileNotFound("Missing cmakelists.jj.txt")

    def __getitem__(self, name):
        return Module( self.home/name )


# ======================================================================================
#  Module
# ======================================================================================

class Module:
    def __init__(self, home: Path):
        if type(home) == str:
            self.home = Path(home)
        else:
            self.home = home
        self.name = self.home.name

    def list(self):
        retval = []
        nodes = os.listdir(str(self.home))
        for node_name in nodes:
            if node_name == "class":
                continue
            if node_name == "main":
                continue
            node_path = self.home / node_name
            if node_path.is_dir():
                retval.append( Object(node_path, self) )
        return retval

    def mkobj(self, obj_name="", **args):
        if obj_name == "":
            obj_name = self.name

        sys.path.append( str(Path.home()/'iotworld/scripts') )
        print("Making {} from {}".format(obj_name, self.name))
        try:
            # create the klass directory
            obj_path = self.home / obj_name
            if obj_path.exists():
                #raise Exception("The object already exists")
                pass
            else:
                obj_path.mkdir(parents=True, exist_ok=True)

            # load the script
            klass_script = importlib.import_module(self.name)
            klass_mkobj_func = getattr(klass_script, "mkobj")

            # execute the script
            klass_mkobj_func( str(self.home), obj_name, **args )
        except ModuleNotFoundError as e:
            print("Error: "+str(e))
            exit(1)
        except AttributeError as e:
            print("Error: "+str(e))
            exit(1)


# ======================================================================================
#  Object
# ======================================================================================

class Object:
    def __init__(self, home: Path, module: Module):
        if type(home) == str:
            self.home = Path(home)
        else:
            self.home = home
        self.name = self.home.name
        self.module = module


example_text = """
from iotproj import Branch, Project, Package

hwlib = Project("./")
hwlib.cmake = Branch("./cmake").rootFromGit("https://github.com/bombark/stm32u5_devices.git")
hwlib.cmake.copyFilesFromRoot("etc/*")

# # Install the Modules
hwlib.install("stm32u5")
hwlib.install("freertos")
hwlib.install("stm32u5_led")
hwlib.install("stm32u5_uart")
hwlib.install("stm32u5_button")
hwlib.install("stm32u5_main")

# Instance the Objects
hwlib.mkobj("stm32u5")
hwlib.mkobj("freertos")
hwlib.mkobj("stm32u5_uart", "uart", rx='PA10', tx='PA9', mode='poll')
hwlib.mkobj("stm32u5_led", "led_red", pin='PH6')
hwlib.mkobj("stm32u5_led", "led_green", pin='PH7')
hwlib.mkobj("stm32u5_button", "btn_user", pin='PC13')
hwlib.mkobj("stm32u5_main", "main", devices=["uart", "led_red", "led_green"])

# Generate the CMakeLists
hwlib.generateCMake("./cmake/cmakelists.jj.txt")
# hwlib.make()
"""
