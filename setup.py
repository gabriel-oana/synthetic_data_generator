import setuptools

requires = [line.strip() for line in open("requirements.txt").readlines()]


setuptools.setup(
    name="synthetic_data_generator",
    version="0.0.1",
    description="Synthetic Data Generator - generates CSV, JSON data using Faker",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    zip_safe=False,
    install_requires=requires,
)