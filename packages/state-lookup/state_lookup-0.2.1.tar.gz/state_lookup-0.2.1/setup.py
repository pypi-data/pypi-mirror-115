
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="state_lookup",                     # This is the name of the package
    version="0.2.1",                        # The initial release version
    author="Deepak Sharma",                     # Full name of the author
    data_files = ["state_lookup/src/city_state_map.txt"],
    include_package_data=True,
    description="Find the state in which the city is",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["state_lookup","data_file"],             # Name of the python package
    package_dir={'':'state_lookup/src'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)