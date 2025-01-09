from setuptools import setup, find_packages

setup(
    name="py2notebook-ai",
    version="0.1.0",
    description="A Python library to convert scripts into Jupyter Notebooks with AI-generated comments.",
    author="Thomas Bale",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "openai",
        "nbformat",
    ],
    entry_points={
        "console_scripts": [
            "py2notebook-ai=py2notebook_ai.cli:main",
        ],
    },
)
