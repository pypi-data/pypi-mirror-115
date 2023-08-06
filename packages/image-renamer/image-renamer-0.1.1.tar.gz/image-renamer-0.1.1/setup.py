from setuptools import setup
from setuptools import find_packages

version = "0.1.1"

install_requires = [
    "Pillow"
]

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="image-renamer",
    version=version,
    description="Simple bulk image timestamps renamer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JozefGalbicka/image-renamer.git",
    author="Jozef Galbicka",
    author_email="alerts.cryp@gmail.com",
    license="MIT",
    scripts=['image_renamer.py'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Topic :: Multimedia",
        "Topic :: System :: Filesystems",
    ],
    packages=[],
    include_package_data=True,
    install_requires=install_requires,
)
