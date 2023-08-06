import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='pubspec',
    version='0.1.7',
    scripts=['pubspec'],
    author="Preetam",
    author_email="contact@preetam.dev",
    description="Python script to update pubspec.yaml in flutter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prtm/pubspec",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests>=2.24.0',
        'ruamel.yaml>=0.16.10',
        'lxml>=4.5.1',
        'pyyaml>=6.0',
    ]
)
