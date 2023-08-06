from os import path
from shutil import copyfile
from subprocess import Popen, PIPE, STDOUT

def build():

    rootdir = path.dirname(__file__)

    try:
        copyfile(path.join(rootdir, 'config', 'gnu.cfg'), path.join(rootdir, 'build.cfg'))
    except FileExistsError:
        pass

    p = Popen([path.join(rootdir, 'build.sh'), '-lpy'], stdout=PIPE, stderr=STDOUT, bufsize=0)

    for line in iter(p.stdout.readline, b''):
        print(">>> " + line.rstrip())

    p.stdout.close()
    p.wait()

