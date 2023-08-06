from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ediss",
    version="1.0.0",
    author="origamizyt",
    author_email="zhaoyitong18@163.com",
    description="Integrated security scheme for curve25519.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/origamizyt/ediss",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['ediss'],
    python_requires=">=3",
    install_requires=['cryptography']
)