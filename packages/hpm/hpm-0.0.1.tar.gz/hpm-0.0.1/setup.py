import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hpm",
    version="0.0.1",
    author="Tanguy Cavagna",
    author_email="tanguy.cvgn@gmail.com",
    description="HEPIA Project Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitedu.hesge.ch/tanguy.cavagna/hpm",
    project_urls={
        "Bug Tracker": "https://gitedu.hesge.ch/tanguy.cavagna/hpm/-/issues",
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