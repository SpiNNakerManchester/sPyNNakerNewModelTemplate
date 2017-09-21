import os
from setuptools import setup
from collections import defaultdict

__version__ = None
exec(open("python_models8/_version.py").read())
assert __version__


# Build a list of all project modules, as well as supplementary files
main_package = "python_models8"
data_extensions = {".aplx", ".xml", ".json", ".xsd"}
config_extensions = {".cfg", ".template"}
main_package_dir = os.path.join(os.path.dirname(__file__), main_package)
start = len(main_package_dir)
packages = []
package_data = defaultdict(list)
for dirname, dirnames, filenames in os.walk(main_package_dir):
    if '__init__.py' in filenames:
        package = "{}{}".format(
            main_package, dirname[start:].replace(os.sep, '.'))
        packages.append(package)
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext in data_extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append("*{}".format(ext))
            break
        if ext in config_extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append(filename)

url = "https://github.com/SpiNNakerManchester/sPyNNaker8NewModelTemplate"

setup(
    name="sPyNNaker8NewModelTemplate",
    version=__version__,
    description="Spinnaker 8 Template for New Models",
    url=url,
    packages=packages,
    package_data=package_data,
    install_requires=[
        'SpiNNUtilities >= 1!4.0.0, < 1!5.0.0',
        'SpiNNStorageHandlers >= 1!4.0.0, < 1!5.0.0',
        'SpiNNMachine >= 1!4.0.0, < 1!5.0.0',
        'SpiNNMan >= 1!4.0.0, < 1!5.0.0',
        'SpiNNaker_PACMAN >= 1!4.0.0, < 1!5.0.0',
        'SpiNNaker_DataSpecification >= 1!4.0.0, < 1!5.0.0',
        'spalloc >= 1.0.0, < 2.0.0',
        'SpiNNFrontEndCommon >= 1!4.0.0, < 1!5.0.0',
        'sPyNNaker >= 1!4.0.0, < 1!5.0.0',
        'sPyNNaker8 >= 1!4.0.0, < 1!5.0.0']
)
