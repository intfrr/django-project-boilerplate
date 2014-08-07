# Boilerplate para proyectos con Django 1.7 y PostgreSQL #

NOTA: Esta versión contiene el RC2 de Django 1.7

## ¿Que contiene?

Contiene un maquina virtual con debian 7.4 con python, postgres y nodejs lista para correr django.

El proyecto de django ya tiene una estructura y una configuracion inicial bastante facil de entender y contiene los siguientes modulos:

- PsycoPG2 como driver de postgres http://initd.org/psycopg/
- Django Debug Toolbar para un facil debug http://django-debug-toolbar.readthedocs.org/
- Django Pipeline para el manejo de assets y compresion de assets y html en producción http://django-pipeline.readthedocs.org/
- Pillow para manipulacion de imagenes https://pypi.python.org/pypi/Pillow/

La maquina virtual ya viene lista y preconfigurada com bower para el manejo de librerias para el front end, estas se guardar en src/media/components y fabric ya tiene los comandos para usarlo sin entrar a la vm.

## Dependencias ##

### Configurar Python y git con bash en Windows 7 ###

Instalar los siguientes paquetes

- Python 2.7 http://www.python.org/ftp/python/2.7.5/python-2.7.5.msi
- SetupTools para Python 2.7 http://www.lfd.uci.edu/~gohlke/pythonlibs/bnrm5n67/setuptools-1.1.6.win32-py2.7.exe
- Pip para Python 2.7 http://www.lfd.uci.edu/~gohlke/pythonlibs/bnrm5n67/pip-1.4.1.win32-py2.7.exe
- Pycrypto para Python 2.7 http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe
- Git con bash (decir que instale todo) http://msysgit.github.io/

Al terminar modificar en: Panel de Control > Sistema > Configuracion avanzada de Sistema
Despues en la pestaña de opciones avanzadas, dar click en variables de entorno.

Desplazarce hasta la variable "Path" hacer doble click y sin modificar la ruta solo le añadimos al final ;C:\Python27\Scripts
incluyendo el punto y coma, aceptamos todo.

NOTA: Todos los comandos que van a continuación se ejecutando dentro de la consola de git en si es una consola bash, es necesario para poder usar ssh con vagrant y conectar a la maquina virtual.


### Instalar Vagrant y Cuisine ###

Vagrant y virtualbox se puede descargar de sus sitios para cualquier plataforma, si su sistema operativo (linux) tiene repositorios
se pueden usar tambien.

- Virtual box: https://www.virtualbox.org
- Vagrant: http://www.vagrantup.com

Para instalar cuisine lo podemos hacer desde el gestor de paquetes de python.
En nuestra consola ponemos lo siguiente, si estamos en osx o linux podemos instaladorlo como root usando sudo.

    pip install cuisine

o

    easy_install cuisine


## Como usarlo ##

### Creando el entorno de desarrollo para el proyecto ###

- Copiar __src/settings/enviroment.py.txt__ a __src/settings/enviroment.py__.
- Ejecutar __vagrant up__ para crear la maquina virtual.
- Ejecutar __fab bootstrap__ para provisionar la maquina virtual. NOTA: Si pide password se debe poner "vagrant".
- Ejecutar __fab migrate__ para crear las tablas principales.
- Ejecutar __fab createsuperuser__ para crear el usuario de administración.
- Ejecutar __fab bower__ para instalar las dependencias del frontend.
- Ejecutar __fab runserver__ para correr el servidor de desarrollo.
- Para para poder acceder a la aplicación se hace por http://127.0.0.1:8000.

### Retomando el desarrollo (Ejemplo) ###

- Ejecutar __vagrant up__ para encender la maquina virtual.
- Ejecutar __fab migrate__ para actualizar la base de datos en caso de usar migraciones.
- Ejecutar __fab runserver__ para correr el servidor de desarrollo.

### Modificando el proyecto ###

- Modificar el __src/bower.json__ para agregar nuevos paquetes para el desarrollo de frontend.
- Modificar el __src/requirements.txt__ para agregar nuevos paquetes de python.
- Editar el __src/settings/enviroment.py__ para configurar variables del entorno de la aplicación, por ejemplo: credenciales de correo.
- Modificar los settings principales de django necesarios en __src/settings/default.py__, por ejemplo: agregar nuevas apliaciones u opciones de localización .
- Editar el __fabfile.py__ para instalar mas paquetes o configurar la maquina virtual de forma personalizada.

### Manejando maquinas virtuales ###

- Ejecutar __vagrant up__ para encender la maquina virtual.
- Ejecutar __vagrant ssh__ para entrar a la maquina virtual.
- Ejecutar __vagrant halt__ para apagar la maquina virtual.
- Ejecutar __vagrant reload__ para resetear la maquina virtual.
- Ejecutar __vagrant destroy__ para borrar la maquina virtual.

## Comandos de fabric ##

- fab shell
- fab runserver
- fab migrate
- fab migrate:app-name
- fab makemigrations:app-name
- fab startapp:app-name
- fab pip
- fab debugsqlshell
- fab bower
- fab bower\_list
- fab bower\_search:package
- fab bower\_install:package
- fab bower\_uninstall:package
