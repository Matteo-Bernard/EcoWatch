from setuptools import setup, find_packages

setup(
    name="EcoWatch",
    version="0.0.8",
    description="Visualisation d'indicateurs économiques",
    author="Matteo Bernard",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "typing",
        "scipy",
        "matplotlib",
        "requests",
        "selenium",
        "bs4"
    ],
    include_package_data=True,
)
