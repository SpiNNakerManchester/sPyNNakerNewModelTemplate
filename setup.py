from setuptools import setup

setup(
    name="sPyNNaker8NewModelTemplate",
    version="1!4.0.0a5",
    packages=['python_models8',],
    package_data={'python_models8.model_binaries': ['*.aplx']},
    install_requires=['sPyNNaker8 >= 1!4.0.0a5, < 1!5.0.0']
)
