import setuptools

with open("README.md", "r", encoding="utf8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="new_tools",
    version="0.0.4",
    author="Overcomer",
    author_email="michael31703@gmail.com",
    description="Multiple tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Michael07220823/new_tools.git",
    keywords="tools",
    install_requires=[''],
    license="MIT License",
    packages=setuptools.find_packages(include=["new_tools", "new_tools.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)