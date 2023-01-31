import setuptools


setuptools.setup(
    name="synthetic_data_generator",
    version="1.0.0",
    description="Synthetic Data Generator - generates CSV, JSON data using Faker",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    zip_safe=False,
    install_requires=[
        "boto3>=1.21.23",
        "Faker>=13.3.2",
        "pyaml>=21.10.1",
        "alive-progress>=2.4.0"
    ],
)