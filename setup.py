#!/usr/bin/python3
from setuptools import setup
#from cx_Freeze import setup, Executable

setup(
    name='smvtools',
    version='0.2',
    packages=['smvtools'],
    url='http://github.com/areku/smvtools',
    include_package_data=True,
    license='gpl-v3',
    author='Alexander Weigl',
    author_email='Alexander.Weigl@student.kit.edu',
    description='Visualize the Traces of NuSMV and NuXMV',
    requires=['Jinja2', 'Flask', 'svgwrite', 'click'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
    entry_points={
        "console_scripts": [
            'smvtools-ceviz = smvtools.main:ceviz',
            'tdviz = smvtools.main:drawtd',
            'invtbl2smv = smvtools.main:invtbl2smv'
        ],
    },
    #executables=[Executable("guifoo.py", base="win32")]
)