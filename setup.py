from setuptools import setup, find_packages

setup(
    name="EcoWatch",
    version="0.0.6",
    description="Visualisation d'indicateurs économiques",
    author="Matteo Bernard",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "datetime"
        "typing",
        "scipy",
        "matplotlib",
        "requests",
        "selenium",
        "bs4"
    ],
    include_package_data=True,
)
