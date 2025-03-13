from setuptools import setup, find_packages

setup(
    name="humancursor-botasaurus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "botasaurus-driver>=0.3.0",
        "numpy>=1.19.0",
        "pytweening>=1.0.4",
    ],
    author="HumanCursor Fork",
    author_email="example@example.com",
    description="A fork of HumanCursor that uses Botasaurus driver for human-like mouse movements",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/humancursor-botasaurus",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 