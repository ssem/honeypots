from setuptools import setup

setup(name='assault',
    version='0.1',
    author='ssem',
    requires=[],
    scripts=['bin/FTPAssault_clone',
             'bin/FTPAssault_server',
             'bin/FTPAssault_shell'],
    packages=['ftpassault'],)
