"""
Setup para o Sistema de Monitoramento Rocks
"""

from setuptools import setup, find_packages
import os

# Ler o README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Ler requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rocks-monitoramento-desktop",
    version="1.0.0",
    author="Equipe Rocks",
    author_email="contato@rocks.com",
    description="Sistema de monitoramento de máquinas com interface gráfica moderna",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rocks/rocks-monitoramento-desktop",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "black>=22.0.0",
            "flake8>=4.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rocks-monitor=main:main",
            "rocks-monitor-bg=scripts.background_monitor:main",
        ],
    },
    include_package_data=True,
    package_data={
        "interface": ["image/*.png"],
    },
    zip_safe=False,
)

