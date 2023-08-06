import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syscolors",
    version="0.0.5",
    author="Batuhan Olgac",
    author_email="mares4l@hotmail.com",
    description="Color your Python terminal screen as you wish.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IMaresaLI/syscolors",
    project_urls={
        "Bug Tracker": "https://github.com/IMaresaLI/syscolors/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=2.7",
)