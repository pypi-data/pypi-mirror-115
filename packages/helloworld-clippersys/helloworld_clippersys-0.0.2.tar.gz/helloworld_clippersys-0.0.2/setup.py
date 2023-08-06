from setuptools import setup

with open("README.md","r") as f:
    long_description = f.read()

setup(
    name="helloworld_clippersys",
    version="0.0.2",
    description="Hello World!",
    py_modules=["helloworld_clippersys"],
    package_dir={"":"src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://clippersys.eu",
    author="Chris",
    author_email="info@clippersys.eu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires = [
        "blessings ~= 1.7", 
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
            "twine>=3.4"
        ]
    }
)
