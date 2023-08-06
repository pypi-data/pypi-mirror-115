from setuptools import setup, find_packages
setup(name='pycomlib',
version='2.0.0',
packages=find_packages(),
# package_data = {
#     'providers' : ['providers/config.json'],
#     'slack' : ['providers/config.json'],
#     'email':['providers/config.json']
# },
# data_files = 'providers/config.json',
install_requires=['requests', 'flatten_dict' ]
)
# 'abc',
