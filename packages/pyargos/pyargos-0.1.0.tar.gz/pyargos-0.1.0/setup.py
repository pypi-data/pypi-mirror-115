import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyargos",
    version="0.1.0",
    author="Nuno Anselmo",
    author_email="pyargos@nunoanselmo.me",
    description="A Python library for easier interfacing with Argos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/naanselmo/pyargos",
    project_urls={
        "Bug Tracker": "https://github.com/naanselmo/pyargos/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: X11 Applications :: Gnome",
        "Operating System :: POSIX"
    ],
    package_data={'': ['LICENSE']},
    package_dir={"pyargos": "pyargos"},
    packages=["pyargos"],
    python_requires=">=3.9"
)
