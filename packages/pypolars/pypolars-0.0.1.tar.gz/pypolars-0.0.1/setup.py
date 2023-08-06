from setuptools import setup, find_packages

packages = find_packages()
setup(
    name="pypolars",
    packages=packages,
    include_package_data=True,
    install_requires=["polars"],
    version="0.0.1",
    url="https://www.xdss.io",
    description="A tool for deploying machine learning",
    author="Yonatan Alexander",
    author_email="jonathan@xdss.io",
    python_requires='>=3',
)
