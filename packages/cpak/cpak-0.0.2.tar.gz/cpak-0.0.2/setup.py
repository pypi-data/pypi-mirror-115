from distutils import dist
import os
import setuptools

NAME = "cpak"
VERSION = "0.0.2"


class uploadCommand(setuptools.Command):
    description = 'upload dist file to PyPI'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system(f'twine upload dist/{NAME}-{VERSION}.tar.gz')


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author="yhl1219",
    author_email="yhliu2000@outlook.com",
    description="A package manager and build system for c/c++ using python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yhl1219/cpak",
    project_urls={
        "Bug Tracker": "https://github.com/yhl1219/cpak/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    cmdclass={'upload': uploadCommand}
)
