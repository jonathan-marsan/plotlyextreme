import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotly-extreme",
    version="0.0.1",
    author="Jonathan",
    description="Simple wrapper functions for plotly visualization package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathan-marsan/plotly-extreme",
    packages=setuptools.find_packages(),
    install_requires=[
          'pandas',
          'plotly',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)