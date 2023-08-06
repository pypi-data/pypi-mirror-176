import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto-feature-engineering", 
    version="0.0.2",
    author="Xinlin Wang",
    author_email="xinlin.wang.stats@gmail.com",
    install_requires=[
    'pandas==1.3.5',
    'numpy==1.20.0',
    'lightgbm==3.3.2',
    'scikit-learn==1.0.1',
    'multiprocess==0.70.14'
    ],
    description="A package for automatically generating features",
    long_description=long_description,
    long_description_content_type="text/markdown",#
    url="https://github.com/LeylaWong/autoFE",#
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)