import pathlib
from setuptools import setup, find_packages

parent_dir = pathlib.Path(__file__).parent
readme_file = (parent_dir / 'README.md').read_text()
required_packages = [
    'pandas',
    'numpy',
    'requests',
    'dataclasses',
    'sqlalchemy',
    'joblib',
    'psycopg2-binary',
    'boto3>=1.17',
    'pyarrow>=3.0.0',
    'fsspec>=0.8.7'
]

setup(
    name="accelo",
    version="0.0.1",
    descrption="Accelo MLOps thin client to log ML Models and Data. ",
    long_description=readme_file,
    long_description_content_type="text/markdown",
    url="https://acceldata.io",
    author="Acceldata",
    author_email="support@acceldata.io",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=['assets', 'build', 'configs', 'tests']),
    include_package_data=True,
    keywords='accelo',
    install_requires=required_packages,
)
