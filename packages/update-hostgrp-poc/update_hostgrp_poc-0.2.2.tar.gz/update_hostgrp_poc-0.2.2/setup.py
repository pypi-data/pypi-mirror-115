import os
from setuptools import setup

with open("requirements.txt") as reqs_file:
    reqs = reqs_file.readlines() 

setup(
    name ="update_hostgrp_poc",
    version ="0.2.2",
    packages = ['src'],
    include_package_data=True,
    zip_safe=True,              
    install_requires = reqs,
 
    entry_points={
        'console_scripts':[
            'update-hostgrp-poc = src.update_hostgrp_poc:main'
        ],
    },
)
