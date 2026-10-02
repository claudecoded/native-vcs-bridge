from setuptools import setup, find_packages

setup(
    name="native-vcs-bridge",
    version="1.0.0",
    author="VCS Core Architecture Engineers",
    description="A production-grade translation daemon bridge linking SVN, Mercurial, and Perforce into Git interfaces.",
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "vcs-bridge=main:main",
        ],
    },
)
