import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edit-json-file",
    version="0.0.1",
    author="Hexye",
    author_email="dragonsale22@gmail.com",
    description="An api wrapper to edit json files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HexyeDEV/edit-json-file",
    download_url="https://github.com/HexyeDEV/edit-json-file/releases",
    project_urls={
        "Bug Tracker": "https://github.com/HexyeDEV/edit-json-file/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
