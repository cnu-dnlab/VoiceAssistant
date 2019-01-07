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
    for dep in read_deps(file_path):
        try:
            pkg_resources.require(dep)
        except pkg_resources.DistributionNotFound:
            not_installed.append(dep)
        except pkg_resources.VersionConflict:
            not_installed.append(dep)
    return not_installed

def binary_checker(file_path):
    not_installed = list()
    for dep in read_deps(file_path):
        command = ' '.join(dep)
        exit_code = subprocess.getstatusoutput(command)
        if exit_code[0] != 0:
            not_installed.append(dep[0])
    return not_installed

