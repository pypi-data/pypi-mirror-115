from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Generic code for processing and execution for OMD EMEA'

# Setting up
setup(
    name="omd_emea",
    version=VERSION,
    author="Aniruddha Sengupta",
    author_email="aniruddha.sengupta@omd.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'facebook-business', 'google', 'sqlalchemy', 'selenium'],
    keywords=['python', 'omd', 'general', 'generic'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)