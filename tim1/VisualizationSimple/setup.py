from setuptools import setup, find_packages

setup(
    name="expressivness-visualization-simple",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1', 'jinja2'],
    entry_points={
        'core.visualization':
            ['visualize_simple=visualize.code.visualization_simple:VisualizeGraphSimple'],
    },
    package_data={'visualize': ['static/*.css', 'static/*.js', 'static/*.html', 'templates/*.html']},
    namespace_packages=['visualize', 'visualize.code'],
    zip_safe=False
)
