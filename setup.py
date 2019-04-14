from setuptools import setup

setup(
    name='graph_flow',
    version='0.1',
    description='Graph flow core',
    author="Group-4B",
    packages=['gf'],
    install_requires=['networkx == 2.3', 'pytest == 4.4.0'],
    zip_safe=False
)
