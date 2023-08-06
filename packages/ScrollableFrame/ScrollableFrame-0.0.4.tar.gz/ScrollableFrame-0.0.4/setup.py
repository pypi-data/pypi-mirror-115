import setuptools

setuptools.setup(
    name="ScrollableFrame",
    version='0.0.4',
    author="larryw3i",
    author_email="",
    description="Your tkinter ScrollableFrame",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/larryw3i/ScrollableFrame",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data = True,
)
