import subprocess
import csv

import pkg_resources
from pkg_resources import DistributionNotFound
from pkg_resources import VersionConflict

def make_binary_list(binaries_file_path):
    binaries = list()
    with open(binaries_file_path, 'r') as bin_list_file:
        reader = csv.reader(bin_list_file, delimiter=',')
        for _, row in enumerate(reader):
            binaries.append(row)
    return binaries

def make_dependencies_list(modules_file_path):
    dependencies = list()
    with open(modules_file_path, 'r') as require_file:
        while True:
            line = require_file.readline()
            if not line:
                break
            line = line.replace('\n', '')
            dependencies.append(line)
    return dependencies

def module_checker(modules_file_path):
    not_installed_modules = []
    for dependency in make_dependencies_list(modules_file_path):
        try:
            pkg_resources.require(dependency)
        except DistributionNotFound:
            not_installed_modules.append(dependency)
        except VersionConflict:
            not_installed_modules.append(dependency)
    return not_installed_modules

def binary_checker(binaries_file_path):
    not_installed_binaries = []
    binaries = make_binary_list(binaries_file_path)
    for binary in binaries:
        binary_check_msg = binary[0] +" "+binary[1]
        exit_code = subprocess.getstatusoutput(binary_check_msg)
        if exit_code[0] != 0:
            not_installed_binaries.append(binary)
    return not_installed_binaries

