import subprocess

import pkg_resources
from pkg_resources import DistributionNotFound
from pkg_resources import VersionConflict

DEPENENCIES = ['SoundFile>=0.10.2',
               'sounddevice>=0.3.0',
               'opencv-python>=3.4.4.0',
               'snvf']
BINARIES = ["abc"]
CHECK_MSG = " --help"

def module_checker():
    not_installed_modules = []
    for dependency in DEPENENCIES:
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
