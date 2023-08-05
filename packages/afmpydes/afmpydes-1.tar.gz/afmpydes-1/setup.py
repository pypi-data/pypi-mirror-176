import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '1'     # Version de la Libreria
PACKAGE_NAME = 'afmpydes'   # Nombre de la carpeta
AUTHOR = 'Alberto Fernandez Maya'   # Autor de la Libreria
AUTHOR_EMAIL = 'afernandezm@gmail.com'  # EMail del Autor
URL = 'https://github.com/'     # Pagina Web del Autor

LICENSE = 'MIT'     # Tipo de licencia
DESCRIPTION = 'Calculos de Suma, Resta, Multiplicacion, Division'    # Descripción corta explicando la Librería

#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
    'pandas'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)