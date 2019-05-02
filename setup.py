from setuptools import setup

INSTALL_REQUIREMENTS = [
    'pytest-runner == 4.4',
    'networkx == 2.3',
    'sympy == 1.4',
    'Matplotlib == 3.0.3',
    'scipy == 1.2.1'
]

TESTS_REQUIREMENTS = [
    'jsondiff == 1.1.2',
    'pylint == 2.3.1',
    'pytest == 4.4.1'
]

EXTRAS = {
    'testing': TESTS_REQUIREMENTS
}

setup(
    name='graph_flow',
    version='0.1',
    description='Graph flow core',
    author="Group-4B",
    packages=['graphflow'],
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=INSTALL_REQUIREMENTS,
    tests_require=TESTS_REQUIREMENTS,
    extras_require=EXTRAS,
    test_suite="tests",
    zip_safe=False
)
