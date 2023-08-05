from setuptools import setup, find_namespace_packages
from pathlib import Path

setup(
    name="autodocx",
    author="Juan Cerezo",
    description="A tool for automating Microsoft Word Documents generation",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/juancerezo/python-autodocx",
    keywords=[
        "docx",
        "word",
        "doc",
        "automation",
        "automated",
        "microsoft",
        "office",
        "document",
        "generator",
        "generation",
        "build",
        "excel",
    ],
    python_requires=">=3.10.*",
    version="0.1.0",
    packages=find_namespace_packages(exclude=["build", "build.*"]),
    install_requires=["click==8.1.3", "python-docx==0.8.11", "openpyxl==3.0.10"],
    entry_points={
        "console_scripts": [
            "autodocx = autodocx:cli",
        ],
    },
)
