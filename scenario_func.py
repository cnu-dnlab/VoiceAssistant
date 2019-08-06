import os
import time
import subprocess
import shlex


def device_call(data):
    dcname = '{0}.mp3'.format(data[data['arg']])
    dcpath = os.path.join(data['mroot'], dcname)
    cmd = 'mpv --loop-playlist=no --keep-open=no {0}'.format(dcpath)
    subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)


def sleep_for(data):
    time.sleep(int(data['arg']))


def command_call(data):
    cc = '-'.join([data['cat'], data['com']])
    ccname = '{0}.mp3'.format(cc)
    ccpath = os.path.join(data['mroot'], ccname)
    cmd = 'mpv --loop-playlist=no --keep-open=no {0}'.format(ccpath)
    subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)


def get_scenario(sroot, sce):
    spath = os.path.join(sroot, sce)
    if os.path.exists(spath):
        return spath
    else:
        return os.path.join(sroot, 'default')


def play_scenario(scene, data):
    with open(scene, 'r') as f:
        for line in f:
            func, arg = line.split(',')
            func = eval(func)
            data['arg'] = arg.strip()
            func(data)

