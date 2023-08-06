from setuptools import setup

setup(
    name='nolk-dwh',
    version='0.0.7',
    packages=['dwhlogs'],
    install_requires=[
        'requests',
        'importlib; python_version == "3.8"',
    ],
)