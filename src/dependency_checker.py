import subprocess


def dependency_checker():
    check_module_list = ['SoundFile', 'sounddevice', 'opencv-python']
    subprocess.run("pip freeze > requirements.txt", shell=True)
    with open('./requirements.txt') as pip_list_file:
        installed_module_list = pip_list_file.read()
        for module in check_module_list:
            if not module in installed_module_list:
                raise ImportError
