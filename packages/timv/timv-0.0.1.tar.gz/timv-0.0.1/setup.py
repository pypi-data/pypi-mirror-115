from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()
setup(
name='timv',
version='0.0.1',
description='Say hello!',
py_modules=['timv'],
install_requires = [
        'numpy>=1.19.5',
        'pandas>=1.1.5',
        'info_gain>=1.0.1',
    ],
package_dir={'':'src'},
long_description=long_description,
long_description_content_type='text/markdown',
author = "Valter Eduardo da Silva Junior",
author_email = "valteresj2@gmail.com",
url = 'https://github.com/valteresj2/Tree-Imput-Missing-Values',

)