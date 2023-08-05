from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1'
DESCRIPTION = 'A package to play the google chrome dino game'
LONG_DESCRIPTION = """
# Dino Chrome
## A package to play the google chrome dino game.
## Steps:
### Open chrome:\\dino
### In python file
### from dino import main
### main.run()
"""

setup(
    name="Dino Chrome",
    version=VERSION,
    author = "Shourya Vardhan Goyal",
    description = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ['pyautogui','keyboard'],
    keywords = ['dino','chrome','automate','play','game','shourya vardhan goyal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
