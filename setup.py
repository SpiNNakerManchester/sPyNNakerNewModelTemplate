from setuptools import setup

setup(
    name="sPyNNaker8NewModelTemplate",
    version="1!4.0.0a5",
    packages=['python_models8'],
    package_data={'python_models8.model_binaries': ['*.aplx']},
    dependency_links=['http://github.com/python-quantities/python-quantities/'
                      'tarball/master#egg=quantities'],
    install_requires=['quantities', 'sPyNNaker8 >= 1!4.0.0a5, < 1!5.0.0']
)
