from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Django management command to upload directory to s3 bucket'
LONG_DESCRIPTION = 'Python package used as Django management command to upload directory to s3 bucket'

# Setting up
setup(
    name="upload_directory",
    version=VERSION,
    author="Souradeep Sengupta",
    author_email="souradeepsengupta95@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['django-storages', 'boto3'],
    keywords=['python', 's3', 'directory upload'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)