from setuptools import setup, find_packages

setup(
    name="py2notebook-ai",
    version="0.1.1",  # Update for each release
    description="A Python library to convert scripts into Jupyter Notebooks with AI-generated comments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Thomas Bale",
    author_email="tokbale@outlook.com",  # Replace with your email
    url="https://github.com/TumCucTom/py2notebook-ai",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "openai",
        "nbformat",
    ],
    entry_points={
        "console_scripts": [
            "py2notebook-ai=py2notebook_ai.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
