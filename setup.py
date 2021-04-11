from setuptools import setup, find_packages

setup(
    name="monkey",
    packages = find_packages(
        where="src",
        include=["monkey"]
    ),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": ["monkey=monkey.command_line:main"]
    }
)