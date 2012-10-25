from fabric.api import env, local
from fabric.contrib.project import rsync_project
from fabric.api import env


env['use_ssh_config'] = True

env['hosts'] = ['redcoat']

REMOTE_PATH = '/home/alexm/sites/lista.grep.ro'


def deploy():
    local('python lista.py build')
    rsync_project(REMOTE_PATH, 'build/', delete=True)
