from setuptools import setup, find_packages

setup(
    name="expressivness-loader-third",
    version="0.1",
    packages=find_packages(),
    package_data={'loader': ['data/*.json']},
    install_requires=['core>=0.1'],
    namespace_packages=['loader', 'loader.code'],
    entry_points={
        'core.data_source':
            ['loader_third=loader.code.third_loader:ThirdDataLoader'],
    },
    zip_safe=False
)