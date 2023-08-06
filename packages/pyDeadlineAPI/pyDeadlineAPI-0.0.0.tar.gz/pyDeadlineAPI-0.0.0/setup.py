import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyDeadlineAPI",
    version="0.0.0",
    description="Access DeadlineAPI directories or endpoint directly",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/DeadlineAPI/pyDeadlineAPI",
    author="Maximilian Noppel",
    author_email="max@noppelmax.online",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["deadlineapi"],
    include_package_data=True,
    install_requires=["jsonschema==3.0.1", "requests==2.21.0"],
    entry_points={
        "console_scripts": [
            "pyDeadlineAPI=deadlineapi.__main__:main",
        ]
    },
)
