from setuptools import setup


setup(
    name="dictjson",
    version="1.0.2",
    description="Create a dictionary from your json data",
    long_description="Creates a dictionary from the json data extracting the six labels used in source system value mapping",
    url="https://github.com/prakhar33",
    author="Prakhar Rai",
    author_email="prakhar98.rai@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["dictjson"],
    include_package_data=True,
    install_requires=["setuptools", "pathlib","simplejson","numpy","pandas"],
)

