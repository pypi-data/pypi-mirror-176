from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="radiotrace",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.17.0",
        "matplotlib>=3.1.3",
        "scikit-learn>=0.23.2",
        "scipy>=1.5.2",
        "pydicom>=1.4.1",
        "SimpleITK>=1.2.4",
        "torch>=1.10.0",
        "monai>=0.8.0",
        "rpy2>=3.5.6"
    ],
    author="Jiaqi Li",
    author_email="li-jq18@mails.tsinghua.edu.cn",
    description="package for quantify early-stage LUAD progression from CT image",
    license="MIT",
    url="https://github.com/LiJiaqi96/radiotrace",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
