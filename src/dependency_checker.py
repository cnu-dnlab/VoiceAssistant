import subprocess
import csv

import pkg_resources


def read_deps(file_path):
    deps = list()
    with open(filw_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            deps.append(row)
    return deps

def module_checker(file_path):
    not_installed = list()
    for dependency in read_deps(file_path):
        try:
            pkg_resources.require(dependency)
        except pkg_resources.DistributionNotFound:
            not_installed.append(dependency)
        except pkg_resources.VersionConflict:
            not_installed.append(dependency)
    return not_installed

def binary_checker(file_path):
    not_installed = list()
    for binary in read_deps(file_path):
        command = ' '.join(binary)
        exit_code = subprocess.getstatusoutput(command)
        if exit_code[0] != 0:
            not_installed.append(binary)
    return not_installed

