"""Setup configuration for VimGym."""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from __init__.py
version = {}
with open(Path(__file__).parent / "vimgym" / "__init__.py") as f:
    exec(f.read(), version)

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vimgym",
    version=version["__version__"],
    author=version["__author__"],
    author_email=version["__email__"],
    description=version["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marekmajer/vimgym",
    project_urls={
        "Bug Tracker": "https://github.com/marekmajer/vimgym/issues",
        "Source Code": "https://github.com/marekmajer/vimgym",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Topic :: Text Editors",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "vimgym=vimgym.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "vimgym": [
            "data/lessons/*.yaml",
            "data/challenges/*.yaml", 
            "data/achievements/*.yaml",
            "data/templates/*",
        ],
    },
    zip_safe=False,
)