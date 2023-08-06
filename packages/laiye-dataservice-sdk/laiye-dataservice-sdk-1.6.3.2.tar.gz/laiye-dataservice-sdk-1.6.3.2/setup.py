import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="laiye-dataservice-sdk",
    version="1.6.3.2",
    author="kangyongsheng",
    author_email="kangyongsheng@laiye.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.laiye.com/laiye-dataservice/laiye-dataservice-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
    ],
    install_requires=["requests"],
    python_requires='>=3.6',
)
