import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="YAPI-heureka-code",
    version="1.1.1",
    author="heureka-code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    description="Moeglichkeit eine kleine API mit Lexer zu erstellen",
    url="https://github.com/heureka-code/YAPI-heureka-code",
    download_url="https://github.com/heureka-code/YAPI-heureka-code/archive/refs/tags/1.1.1.tar.gz",
    packages=setuptools.find_packages()
    )
