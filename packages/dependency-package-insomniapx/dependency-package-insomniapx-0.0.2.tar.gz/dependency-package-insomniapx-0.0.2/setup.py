import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dependency-package-insomniapx",
    # version="0.0.1",
    version="0.0.2",
    author="insomniapx",
    author_email="insomniapx@gmail.com",
    description="A package used for dependency for insomniapx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/insomniapx-python-projects/py_package.git",
    package_dir={"": "px_src_name"},
    packages=setuptools.find_packages(where="px_src_name"),
    python_requires=">=3.6",
    install_requires=['pytest==6.2.4', 'numpy==1.20.3']
)
