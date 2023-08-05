import os

import setuptools

MIN_PYTHON_VERSION = "3.6"

DISTNAME = "cmdstan_builder"
DESCRIPTION = "A package to build the cmdstan binary and use it as an extension to EvalML"
LICENSE = "BSD-3-Clause"
VERSION = "0.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

def setup_package():
    # Install in a directory called stan
    import cmdstanpy

    cmdstanpy.install_cmdstan(dir=f"./{DISTNAME}/stan/")

    # Find all the build files and set them as package_data
    files = []
    for r, _, f in os.walk(f"./{DISTNAME}/stan/"):
        for file_ in f:
            files.append(os.path.join(r, file_))
    files = [f.split(f"./{DISTNAME}/")[1] for f in files]

    metadata = dict(
        name=DISTNAME,
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Alteryx, Inc.',
        author_email='support@featurelabs.com',
        license=LICENSE,
        version=VERSION,
        url='https://github.com/alteryx/cmdstan_ext/',
        python_requires=">={}".format(MIN_PYTHON_VERSION),
        install_requires=open("requirements.txt").readlines(),
        packages=setuptools.find_packages(),
        include_package_data=True,
        package_data={DISTNAME: files}
    )

    from setuptools import setup
    setup(**metadata)


if __name__ == "__main__":
    setup_package()
