import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mxmul_FL",
    version="0.1.1",
    author="Feng Le",
    author_email="201130933@qq.com",
    description="An example for teaching how to publish a Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['mxmul']
)