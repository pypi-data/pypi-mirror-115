from setuptools import setup

# Version
version = None
with open("veba/__init__.py", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith("__version__"):
            version = line.split("=")[-1].strip().strip('"')
assert version is not None, "Check version in veba/__init__.py"

setup(
name='veba',
    version=version,
    description='Virus Eukaryote Bacteria Archaea',
    author='Josh L. Espinoza',
    author_email='jespinoz@jcvi.org',
    license='BSD-3',
    packages=["veba"],
    install_requires=[

      ],
)
