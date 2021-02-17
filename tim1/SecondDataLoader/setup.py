from setuptools import setup, find_packages

setup(
    name="expressivness-loader-second",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1', 'requests', 'bs4'],
    namespace_packages=['loader', 'loader.code'],
    entry_points={
        'core.data_source':
            ['loader_second=loader.code.second_loader:SecondDataLoader'],
    },
    zip_safe=False
)
