from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

install_requires = [
    'requests==2.25.1',
    'certifi==2020.12.5',
    'chardet==4.0.0',
    'idna==2.10',
    'urllib3==1.26.4'
]

setup(
    name='python_orange_sms',
    version='0.1.3',
    description='Sending sms to orange api with python',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Ged-flod',
    # contributors=[{'name': 'Samuel Nde', 'email': 'ndesamuelmbah@gmail.com', 'github': 'ndesamuelmbah'}], This line return's error on twine building
    author_email='gedeon@comptelab.com',
    keywords=['orange sms', 'python orange sms', 'python-orange-sms', 'python-orange'],
    url='https://github.com/ged-flod/python_orange_sms',
    download_url='https://pypi.org/project/python_orange_sms/',

    install_requires=install_requires,
    include_package_data=True
)