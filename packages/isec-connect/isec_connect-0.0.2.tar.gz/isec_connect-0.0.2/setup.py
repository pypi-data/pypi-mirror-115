import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="isec_connect",
    version="0.0.2",
    author="Aayush Shah",
    author_email="author@example.com",
    description="Testing isec ws sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['python-socketio[client]','requests'],
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
