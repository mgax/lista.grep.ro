from fabric.api import local
from fabric.contrib.project import rsync_project
from local_fabfile import *


def deploy():
    local('python lista.py build')
    rsync_project(REMOTE_PATH, 'build/', delete=True)
