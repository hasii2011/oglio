import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="xmlio",
    version="0.1",
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='External Pyut Persistence',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/xmlio",
    packages=[
        'xmlio',
    ],
    package_data={
        'xmlio': ['py.typed'],
    },
    install_requires=[
        'ogl==0.54.9',
        'pyutmodel==1.1.0',
        'untanglepyut==0.2.55',
    ],
)
