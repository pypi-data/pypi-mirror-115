from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'A Hand Tracking Module which can detect hands'
LONG_DESCRIPTION = 'Hand Tracking Module uses Mediapipe and Open-cv to find and Detect Hands.'

# Setting up
setup(
    name="tanay",
    version=VERSION,
    author="Tanay Baviskar",
    author_email="tanaybaviskar@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'mediapipe', 'numpy'],
    keywords=['tanay', 'tanay baviskar', 'hand tracking module', 'handtrackingmodule', 'mediapipe', 'python', 'opencv', 'ai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
