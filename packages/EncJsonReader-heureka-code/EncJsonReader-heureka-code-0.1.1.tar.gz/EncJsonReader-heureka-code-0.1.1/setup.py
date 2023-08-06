import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="EncJsonReader-heureka-code",
    version="0.1.1",
    install_requires=["AESEncryptor-heureka-code"],
    author="heureka-code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    description="Mit Passwort gesicherter Json-Manager",
    url="https://github.com/heureka-code/EncJsonReader-heureka-code",
    packages=setuptools.find_packages()
    )
