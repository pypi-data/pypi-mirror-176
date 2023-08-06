"""Python setup.py for qojpca package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("qojpca", "VERSION")
    '0.1.1'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="qojpca",
    version=read("qojpca", "VERSION"),
    description="qojpca package",
    url="https://github.com/florentjousse/qojpca/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="florentjousse",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=['numpy','scikit-learn'
    ],
    entry_points={
        "console_scripts": ["qojpca = qojpca.__main__:main"]
    },
    extras_require={
        "test": ['pytest','coverage','flake8','black','isort','pytest-cov','codecov','mypy','gitchangelog','mkdocs'],
        "gpu": ['cupy-cuda11x']
        },
)
