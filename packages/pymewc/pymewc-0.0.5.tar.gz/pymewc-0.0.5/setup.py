from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'Microcontroller and python interface'
LONG_DESCRIPTION = 'A package that allows to build a Microcontroller and python interface to stream data from the serial monitor '

# Setting up
setup(
    name="pymewc",
    version=VERSION,
    author="Rithic Hariharan (Rithic C H)",
    author_email="<gr8rithic@gmail.com>",
    description=DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyserial', 'pyttsx3', 'setuptools'],
    keywords=['python', 'IoT', 'microcontroller', 'Arduino', 'Text-to-speech'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
