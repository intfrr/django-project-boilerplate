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
    print "Copy enviroment.py.txt to enviroment.py in django settings folder"
    sys.exit(0)


env.user = 'vagrant'
env.hosts = ['127.0.0.1:2222']
result = cuisine.run_local('vagrant ssh-config | grep IdentityFile')
env.key_filename = result.split()[1].replace("\"", "")
env.project_path = '/home/vagrant/src/'
env.virtualenv = 'django-project'


##
## Utils
##
def virtualenv(command):
    """ Run virtualenv commands """

    return "source /usr/local/bin/virtualenvwrapper.sh &&" + command + " " + env.virtualenv


##
## Tasks
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

    puts(green('-> Installing python virtualenv wrapper'))
    cuisine.sudo('pip install virtualenvwrapper')

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

    puts(green('-> Creating python env'))
    cuisine.run('echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc')
    cuisine.run(virtualenv('mkvirtualenv'))

    puts(green('-> Installing requirements for django'))
    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + \
            ' && pip install -r requirements.txt')

    puts(green('-> Installing nodejs'))
    cuisine.package_ensure('nodejs-legacy')
    cuisine.sudo('curl https://npmjs.org/install.sh | sh ')

    puts(green('-> Installing yuglify'))
    cuisine.sudo('npm -g install yuglify')

    puts(green('-> Installing bower'))
    cuisine.sudo('npm -g install bower')

    puts(green('-> Creating directories'))
    cuisine.dir_ensure(env.project_path + 'assets/components')
    cuisine.dir_ensure(env.project_path + 'assets/images')
    cuisine.dir_ensure(env.project_path + 'assets/stylesheets')
    cuisine.dir_ensure(env.project_path + 'assets/scripts')

    puts(red('###############################'))
    puts(red('### Host setup completed'))
    puts(red('###############################'))


@task
def pip():
    """ Run pip install -r """

    puts(red('###############################'))
    puts(red('### Pip'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + \
            ' && pip install -r requirements.txt')


@task
def syncdb():
    """ Run python manage.py syncdb """

    puts(red('###############################'))
    puts(red('### Syncdb'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + " && python manage.py syncdb")


@task
def migrate():
    """ Run python manage.py migrate """

    puts(red('###############################'))
    puts(red('### Migrate'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + " && python manage.py migrate")


@task
def initial_migration(app):
    """ Run python manage.py schemamigration --initial app """

    puts(red('###############################'))
    puts(red('### Initial Schemamigration'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + " && python manage.py schemamigration --initial %s" % app)


@task
def auto_migration(app):
    """ Run python manage.py schemamigration --auto app """

    puts(red('###############################'))
    puts(red('### Auto Schemamigration'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + " && python manage.py schemamigration --auto %s" % app)


@task
def runserver():
    """ Run python manage.py runserver 0.0.0.0:8000  """

    puts(red('###############################'))
    puts(red('### Runserver'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + " && python manage.py runserver 0.0.0.0:8000")


@task
def shell():
    """ Run python manage.py shell """

    puts(red('###############################'))
    puts(red('### Shell'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + " && python manage.py shell")


@task
def debugsqlshell():
    """ Run python manage.py debugsqlshell """

    puts(red('###############################'))
    puts(red('### Debugsqlshell'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run(virtualenv('workon') + " && python manage.py debugsqlshell")


@task
def startapp(app_name):
    """ Run python manage.py startapp name """

    puts(red('###############################'))
    puts(red('### Startapp'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        path = 'applications/%s' % app_name
        cuisine.run('mkdir %s' % path)
        cuisine.run(virtualenv('workon') + " && python manage.py startapp %s %s" %(app_name, path))


@task
def bower_search(package):
    """ Run bower search package """

    puts(red('###############################'))
    puts(red('### Bower search'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run("bower search " + package)


@task
def bower_install(package):
    """ Run bower install package """

    puts(red('###############################'))
    puts(red('### Bower install'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run("bower install " + package)

@task
def bower_uninstall(package):
    """ Run bower uninstall package """

    puts(red('###############################'))
    puts(red('### Bower uninstall'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run("bower uninstall " + package)


@task
def bower_list():
    """ Run bower list packages"""

    puts(red('###############################'))
    puts(red('### Bower list'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run("bower list ")


@task
def bower():
    """ Run bower install from bower.json"""

    puts(red('###############################'))
    puts(red('### Bower install'))
    puts(red('###############################'))

    with cuisine.cd(env.project_path):
        cuisine.run("bower install ")
