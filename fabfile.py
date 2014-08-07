# -*- coding: utf-8 -*-

"""
    Provisioning and deploy in remote servers
    Author  :   Alvaro Lizama Molina <nekrox@gmail.com>
"""

import sys
import cuisine
from fabric.api import env
from fabric.colors import green, red
from fabric.utils import puts
from fabric.decorators import task
try:
    from src.settings.enviroment import DATABASES
except ImportError:
    print "Copy src/settings/enviroment.py.txt to src/settings/enviroment.py"
    sys.exit(0)


env.user = 'vagrant'
env.hosts = ['127.0.0.1:2222']
result = cuisine.run_local('vagrant ssh-config | grep IdentityFile')
env.key_filename = result.split()[1].replace("\"", "")
env.project_path = '/home/vagrant/src/'


##
## Bootstrap
##

@task
def bootstrap():
    """ Bootstrap vagrant enviroment """

    puts(red('###############################'))
    puts(red('### Setup host'))
    puts(red('###############################'))

    puts(green('-> Add backports'))
    cuisine.sudo('echo "deb http://ftp.us.debian.org/debian wheezy-backports main" >> /etc/apt/sources.list')

    puts(green('-> Update repositories'))
    cuisine.package_update()

    puts(green('-> Installing gettext'))
    cuisine.package_ensure("gettext")

    puts(green('-> Installing curl'))
    cuisine.package_ensure("curl")

    puts(green('-> Installing git'))
    cuisine.package_ensure("git")

    puts(green('-> Installing nano'))
    cuisine.package_ensure("nano")

    puts(green('-> Installing build-essential'))
    cuisine.package_ensure("build-essential")

    puts(green('-> Installing libxml2-dev'))
    cuisine.package_ensure("libxml2-dev")

    puts(green('-> Installing libjpeg8-dev'))
    cuisine.package_ensure("libjpeg8-dev")

    puts(green('-> Installing libpng12-dev'))
    cuisine.package_ensure("libpng12-dev")

    puts(green('-> Installing python'))
    cuisine.package_ensure("python")

    puts(green('-> Installing python-dev'))
    cuisine.package_ensure("python-dev")

    puts(green('-> Installing python-pip'))
    cuisine.package_ensure("python-pip")

    puts(green('-> Installing postgres'))
    if not cuisine.dir_exists('/etc/postgresql'):
        cuisine.sudo('echo "deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main" > /etc/apt/sources.list.d/pgdg.list')
        cuisine.sudo('wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -')
        cuisine.package_update()
    cuisine.package_ensure('postgresql')
    cuisine.package_ensure('postgresql-server-dev-9.3')

    puts(green('-> Configuring postgres user login'))
    old_srt = "local   all             all                                     peer"
    new_srt = "local   all             all                                     trust"
    cuisine.sudo('sed -i "s/%s/%s/g" /etc/postgresql/9.3/main/pg_hba.conf' % (old_srt, new_srt))
    cuisine.sudo('/etc/init.d/postgresql restart')

    puts(green('-> Creating database'))
    db_name = DATABASES['default']['NAME']
    db_user = DATABASES['default']['USER']
    db_pass = DATABASES['default']['PASSWORD']

    puts(green('-> Creating postgres username'))
    cuisine.sudo('psql -c "CREATE USER %s WITH PASSWORD \'%s\';"' % (db_user, db_pass), user='postgres')

    puts(green('-> Creating postgres database'))
    cuisine.sudo('psql -c "CREATE DATABASE %s;"' % db_name, user='postgres')

    puts(green('-> Installing requirements for django'))
    with cuisine.cd(env.project_path):
        cuisine.run('pip install --user https://www.djangoproject.com/download/1.7c2/tarball/')
        cuisine.run('pip install --user -r requirements.txt')

    puts(green('-> Installing nodejs'))
    cuisine.package_ensure('nodejs-legacy')
    cuisine.sudo('curl https://www.npmjs.org/install.sh | sh ')

    puts(green('-> Installing yuglify'))
    cuisine.sudo('npm -g install yuglify')

    puts(green('-> Installing bower'))
    cuisine.sudo('npm -g install bower')

    puts(green('-> Creating directories'))
    cuisine.dir_ensure(env.project_path + 'assets/components')
    cuisine.dir_ensure(env.project_path + 'assets/images')
    cuisine.dir_ensure(env.project_path + 'assets/stylesheets')
    cuisine.dir_ensure(env.project_path + 'assets/scripts')
    cuisine.dir_ensure(env.project_path + 'locale/')

    puts(red('###############################'))
    puts(red('### Host setup completed'))
    puts(red('###############################'))


##
## Development tasks
##

@task
def pip():
    """ Run pip install --user -r """

    puts(red('###############################'))
    puts(red('### Pip'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run('pip install --user -r requirements.txt')


@task
def migrate(app=None):
    """ Run python manage.py migrate """

    puts(red('###############################'))
    puts(red('### Migrate'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        if app is not None:
            cuisine.run('python manage.py migrate %s' % app)
        else:
            cuisine.run('python manage.py migrate')


@task
def makemigrations(app=None):
    """ Run python manage.py makemigrations"""

    puts(red('###############################'))
    puts(red('### Makemigrations'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        if app is not None:
            cuisine.run('python manage.py makemigrations %s' % app)
        else:
            cuisine.run('python manage.py makemigrations')


@task
def createsuperuser():
    """ Run python manage.py makemigrations"""

    puts(red('###############################'))
    puts(red('### Createsuperuser'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run('python manage.py createsuperuser')


@task
def runserver():
    """ Run python manage.py runserver 0.0.0.0:8000  """

    puts(red('###############################'))
    puts(red('### Runserver'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run('python manage.py runserver 0.0.0.0:8000')


@task
def shell():
    """ Run python manage.py shell """

    puts(red('###############################'))
    puts(red('### Shell'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run('python manage.py shell')


@task
def debugsqlshell():
    """ Run python manage.py debugsqlshell """

    puts(red('###############################'))
    puts(red('### Debugsqlshell'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run('python manage.py debugsqlshell')


@task
def makemessages(lang=None):
    """ Run python manage.py makemessages """

    puts(red('###############################'))
    puts(red('### Makemessages'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        if lang is not None:
            cuisine.run('python manage.py makemessages -l %s' % lang)
        else:
            cuisine.run('python manage.py makemessages -a')


@task
def compilemessages():
    """ Run python manage.py compilemessages """

    puts(red('###############################'))
    puts(red('### Compilemessages'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run('python manage.py compilemessages')

@task
def startapp(app_name):
    """ Run python manage.py startapp name """

    puts(red('###############################'))
    puts(red('### Startapp'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        path = 'applications/%s' % app_name
        cuisine.run('mkdir %s' % path)
        cuisine.run('python manage.py startapp %s %s' % (app_name, path))


@task
def bower():
    """ Run bower install from bower.json"""

    puts(red('###############################'))
    puts(red('### Bower install'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run('bower install')
