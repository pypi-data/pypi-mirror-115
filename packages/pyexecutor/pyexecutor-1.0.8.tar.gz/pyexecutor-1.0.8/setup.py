import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyexecutor",
    version="1.0.8",
    author="WANG ZIJIAN",
    author_email="actini@outlook.com",
    description=
    """
        A light-weight module to run shell / commander commands and get output with Python, compatible with Windows, Linux and MacOS.
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/actini/pyexecutor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
