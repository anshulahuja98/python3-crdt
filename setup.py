import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python3-crdt",
    version="1.0.1",
    author="Geetesh Gupta",
    author_email="ggguitarg31@gmail.com",
    description="A python library for CRDTs (Conflict-free Replicated Data types)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geetesh-gupta/python3-crdt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)