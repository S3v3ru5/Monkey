from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read() 

setup(
    name="monkey",
    version="0.1.0",
    author="Vara prasad(S3v3ru5)",
    author_email="vara10110@gmail.com",
    description="Interpreter for Monkey Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(
        where="src",
        include=["monkey", "monkey.*"]
    ),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": ["monkey=monkey.command_line:main"]
    }
)
