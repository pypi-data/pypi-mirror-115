
from setuptools import find_packages, setup

with open('README.md') as readme_file:
    README = readme_file.read()

install_requires = [
    'requests==2.25.1',
    'certifi==2020.12.5',
    'chardet==4.0.0',
    'idna==2.10',
    'urllib3==1.26.4'
]

setup(
    name='python_orange_sms',
    packages=find_packages(),
    version='0.1.4',
    description='Sending sms to orange api with python',
    author='Ged Flod',
    author_email='gedeon@comptelab.com',
    # contributors=[{'name': 'Samuel Nde', 'email': 'ndesamuelmbah@gmail.com', 'github': 'ndesamuelmbah'}], This line return's error on twine building
    license='MIT',
    long_description_content_type="text/markdown",
    long_description=README,
    keywords=['orange sms', 'python orange sms', 'python-orange-sms', 'python-orange'],
    install_requires=install_requires,
    setup_requires=['pytest-runner'],   
    url='https://github.com/ged-flod/python_orange_sms',
    download_url='https://pypi.org/project/python_orange_sms/',
    tests_requires=['pytest'],
    test_suite='tests',
    python_requires='>=3.6',
    
    include_package_data=True
)