import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description=fh.read()

setuptools.setup(
    name="EthCod",
    version="0.0.1",
    author="notcod",
    author_email="nostupar@gmail.com",
    description="A light weight ethereum private key and address generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/notcod/ethereum-brute-force-python3",
    project_urls={
        "Bug Tracker": "https://github.com/notcod/ethereum-brute-force-python3/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)