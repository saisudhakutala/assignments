from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in assignments/__init__.py
from assignments import __version__ as version

setup(
	name="assignments",
	version=version,
	description="to solve assignments",
	author="Saisudha",
	author_email="asignments.sudha@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
