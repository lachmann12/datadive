import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datadive",
    version="0.0.1",
    author="Alexander Lachmann",
    author_email="alexander.lachmann@gmail.com",
    description="Dive nose first into data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lachmann12/datadive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "datadive": ["data/*"]
    },
    include_package_data=True,
    install_requires=list(map(str.strip, open('requirements.txt', 'r').readlines())),
    python_requires='>=3.6',
)