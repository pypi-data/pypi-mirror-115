import setuptools
from pathlib import Path

setuptools.setup(
    name="ginapdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=['tests', 'data'])
)

# message = 'Hello world'
# print(message)
