import setuptools

with open("README.md", "r") as f:
    long_description  = f.read()

setuptools.setup(
    name="I Am Sidd", #name of package
    version="0.0.1",
    author="Siddhartha Purwar",
    description="Hello Siddhartha Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(), #all python module to be install to use this package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    py_modules=["sidd"], #name of python module
    package_dir={'':'hello/src'},
    install_requires=[]
)