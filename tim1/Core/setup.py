from setuptools import setup, find_packages

setup(
    name="core",
    version="0.1",
    packages=find_packages(),
    install_requires=['Django>=2.1'],

    package_data={'core': ['static/*.css', 'static/*.js', 'static/*.html', 'templates/*.html', 'static/bootstrap/css/*',
                           'static/bootstrap/js/*', 'static/jquery/*', 'static/d3/*',
                           'static/jstree/*', 'static/jstree/themes/*', 'static/jstree/themes/default/*', 'static/jstree/themes/proton/*']},
    zip_safe=False
)
