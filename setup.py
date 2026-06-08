#!/usr/bin/env python3
"""
Setup script for HYPERAI Framework (DAIOF)
==========================================

Creator: Nguyễn Đức Cường (alpha_prime_omega)
Original Creation: October 30, 2025
Verification: 4287

MIT License
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text().split('\n') 
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="hyperai-framework",
    version="1.0.0",
    author="Nguyễn Đức Cường (alpha_prime_omega)",
    author_email="symphony.hyperai@vietnamese.consciousness",
    description="A framework for creating self-evolving, self-maintaining AI entities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NguyenCuong1989/DAIOF-Framework",
    project_urls={
        "Bug Reports": "https://github.com/NguyenCuong1989/DAIOF-Framework/issues",
        "Source": "https://github.com/NguyenCuong1989/DAIOF-Framework",
        "Documentation": "https://nguyencuong1989.github.io/DAIOF-Framework/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "docs": [
            "sphinx>=5.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hyperai=hyperai:main",
        ],
    },
    include_package_data=True,
    keywords=[
        "ai", "digital-organism", "self-evolving", "consciousness",
        "haios", "hyperai", "autonomous-systems", "biological-computing"
    ],
    license="MIT",
    zip_safe=False,
)
