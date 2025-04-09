from setuptools import setup, find_packages

setup(
    name="EcoWatch",
    version="0.0.1",
    description="Visualisation d'indicateurs économiques",
    author="Matteo Bernard",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "typing",
        "scipy",
        "matplotlib"
    ],
    include_package_data=True,
)
