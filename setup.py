from setuptools import setup, find_packages

# Read dependencies from requirements.txt file
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='devtools',
    version='1.0.2',
    author='Jeremy Parkinson',
    author_email='jeremy.parkinson@powersystemservices.com.au',
    description='Description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=required_packages,  # Set dependencies from requirements.txt
    url='http://192.168.1.12:8080/all-users/dev-tools/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)