import subprocess

import pkg_resources
from pkg_resources import DistributionNotFound
from pkg_resources import VersionConflict

BINARIES = ["abc"]
CHECK_MSG = " --help"

def make_dependencies_list():
    dependencies = list()
    with open('requirements.txt') as require_file:
        while True:
            line = require_file.readline()
            if not line:
                break
            line = line.replace('\n', '')
            dependencies.append(line)
    return dependencies

def module_checker():
    not_installed_modules = []
    for dependency in make_dependencies_list():
        try:
            pkg_resources.require(dependency)
        except DistributionNotFound:
            not_installed_modules.append(dependency)
        except VersionConflict:
            not_installed_modules.append(dependency)
    return not_installed_modules

def binary_checker():
    not_installed_binaries = []
    for binary in BINARIES:
        binary_check_msg = binary + CHECK_MSG
        exit_code = subprocess.getstatusoutput(binary_check_msg)
        if exit_code[0] != 0:
            not_installed_binaries.append(binary)
    return not_installed_binaries
