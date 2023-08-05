import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyexecutor",
    version="1.0.1",
    author="WANG ZIJIAN",
    author_email="actini@outlook.com",
    description=
    """
        A light-weight command executor to run commands and return stdout and stderr.
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/actini/pyexecutor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
)
