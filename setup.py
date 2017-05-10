from setuptools import setup

setup(
    name="sPyNNaker8NewModelTemplate",
    version="1.0.0",
    packages=['python_models8',],
    package_data={'python_models8.model_binaries': ['*.aplx']},
    install_requires=['SpyNNaker >= 3.0.0, < 4.0.0']
)
