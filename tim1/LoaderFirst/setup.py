from setuptools import setup, find_packages

setup(
    name="expressivness-loader-first",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1', 'requests', 'bs4'],
    namespace_packages=['loader', 'loader.code'],
    entry_points={
        'core.data_source':
            ['loader_first=loader.code.first_loader:FirstDataLoader'],
    },
    zip_safe=False
)
