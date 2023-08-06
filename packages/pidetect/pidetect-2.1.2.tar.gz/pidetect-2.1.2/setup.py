import setuptools

setuptools.setup(
    name="pidetect",
    version="2.1.2",
    description="python image detect lib",
    packages=['pidetect'],
    package_data={'pidetect': ['so/*']},
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)

