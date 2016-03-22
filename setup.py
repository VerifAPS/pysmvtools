#!/usr/bin/python3
from setuptools import setup


setup(
    name='smvtools',
    version='0.2',
    packages=['smvtools', 'smvtools.invtbl', 'smvtools.ceviz', 'smvtools.web'],
    url='http://github.com/areku/smvtools',
    include_package_data=True,
    license='gpl-v3',
    author='Alexander Weigl',
    author_email='Alexander.Weigl@student.kit.edu',
    description='Visualize the Traces of NuSMV and NuXMV',
    install_requires=['Jinja2', 'Flask', 'svgwrite', 'click', 'pyyaml', 'Flask-Bootstrap'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
    entry_points={
        "console_scripts": [
            'ceviz = smvtools.main:ceviz',
            'tdviz = smvtools.main:drawtd',
            'invtbl2smv = smvtools.invtbl:invtbl2smv'
        ],
    },
)
