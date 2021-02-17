from setuptools import setup, find_packages

setup(
    name="expressivness-visualization-complex",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1', 'jinja2'],
    entry_points={
        'core.visualization':
            ['visualize_complex=visualize.code.visualization_complex:VisualizeGraphComplex'],
    },
    package_data={
        'visualize': ['templates/*.html']},
    namespace_packages=['visualize', 'visualize.code'],
    zip_safe=False
)
