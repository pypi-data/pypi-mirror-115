import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

# get version
env = {}
with open("callable_cli/version.py") as f:
	exec(f.read(), env)
version = env["__version__"]

# get requirements
with open("requirements.txt") as f:
	install_requires = f.readlines()

setuptools.setup(
	name = "callable-cli",
	version = version,
	author = "Chris Pyles",
	description = "A wrapper for building click CLIs that retains callable functions",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/chrispyles/callable-cli",
	license = "BSD-3-Clause",
	packages = setuptools.find_packages(exclude=["test"]),
	classifiers = [
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
	],
	install_requires=install_requires,
)
