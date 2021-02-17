import os
import sys
from subprocess import run, PIPE
from collections import OrderedDict
from shutil import rmtree

components = OrderedDict()
components['core'] = {
    'folder': 'Core',
    'name': 'core'
}
components['first-loader'] = {
    'folder': 'LoaderFirst',
    'name': 'expressivness-loader-first'
}
components['second-loader'] = {
    'folder': 'SecondDataLoader',
    'name': 'expressivness-loader-second'
}
components['third-loader'] = {
    'folder': 'ThirdDataLoader',
    'name': 'expressivness-loader-third'
}
components['simple-vis'] = {
    'folder': 'VisualizationSimple',
    'name': 'expressivness-visualization-simple'
}
components['complex-vix'] = {
    'folder': 'VisualizationComplex',
    'name': 'expressivness-visualization-complex'
}

def execute_command(command, std_input=None):
    # Execute os command
    print(command)
    result = run(command.split(' '), stdout=PIPE, input=std_input, encoding='ascii')
    print(result.stdout)

def remove_folder(folder_path):
    print(f'Removing: {folder_path}')
    try:
        rmtree(folder_path)
    except FileNotFoundError:
        pass

def clean_install_component(component, python_path, pip_path):
    # Change working directory
    os.chdir(f"./{component['folder']}")
    cwd = os.getcwd()

    # Uninstall component
    execute_command(f"{pip_path} uninstall {component['name']}", std_input="y")

    # Remove build files
    remove_folder(os.path.join(cwd, 'build'))
    remove_folder(os.path.join(cwd, 'dist'))
    remove_folder(os.path.join(cwd, f"{component['name'].replace('-', '_')}.egg-info"))

    # Install the component
    execute_command(f"{python_path} setup.py install")

    # Get back to the project root
    os.chdir("..")


def get_python_paths():
    if os.name == 'nt':
        venv_prefix = os.path.join(f"{os.environ['VIRTUAL_ENV']}", "Scripts")
        python_path = os.path.join(venv_prefix, "python")
        pip_path = os.path.join(venv_prefix, "pip")
    else:
        venv_prefix = os.path.join(f"{os.environ['VIRTUAL_ENV']}", "bin")
        python_path = os.path.join(venv_prefix, "python3")
        pip_path = os.path.join(venv_prefix, "pip3")
    return python_path, pip_path


def build_project():
    # Get venv paths
    python_path, pip_path = get_python_paths()

    # Clean install all the components
    for key, component_data in components.items():
            clean_install_component(component_data, python_path, pip_path)

    os.chdir("ExPreSsiVeNess")

    # Apply migrations
    execute_command(f"{python_path} manage.py migrate")

    # Start the server
    execute_command(f"{python_path} manage.py runserver")


if __name__ == "__main__":
    if 'VIRTUAL_ENV' not in os.environ:
        print("You have to activate virtual environment before running this script.")
        exit(-1)
    else:
        build_project()