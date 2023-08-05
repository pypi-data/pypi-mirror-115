import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

try:
    requirementsFilePath = os.path.dirname(os.path.abspath(__file__)) + "/requirements.txt"
    requirements = open(requirementsFilePath, "r").read().splitlines()
except Exception:
    requirements = []

setuptools.setup(
    name="python-simple-caching",
    version="0.12",
    author="Mihai Cristian Pîrvu",
    author_email="mihaicristianpirvu@gmail.com",
    description="Simple caching library for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mihaicristianpirvu/simple-caching/",
    keywords = ["caching", "cache"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    license="WTFPL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
